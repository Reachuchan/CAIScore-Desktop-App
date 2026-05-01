args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 5) {
  stop("Usage: Rscript caiscore_predict_cli.R <base_dir> <expr_file> <age> <stage> <out_csv>")
}

base_dir <- normalizePath(args[1], winslash = "/", mustWork = TRUE)
expr_file <- normalizePath(args[2], winslash = "/", mustWork = TRUE)
age_value <- as.numeric(args[3])
stage_value <- args[4]
out_csv <- args[5]

# Make bundled CAIScore package discoverable (no algorithm change).
.libPaths(c(file.path(base_dir, "caiscore_source"), .libPaths()))

suppressPackageStartupMessages({
  library(CAIScore)
  library(rms)
  library(survival)
})

target_genes <- readRDS(file.path(base_dir, "caiscore_source", "target_genes_list.rds"))
reference_mat <- readRDS(file.path(base_dir, "caiscore_source", "reference_matrix.rds"))
model_cph <- readRDS(file.path(base_dir, "caiscore_source", "final_model_cph.rds"))
saved_ddist <- readRDS(file.path(base_dir, "caiscore_source", "final_datadist.rds"))
options(datadist = "saved_ddist")

get_caiscore_for_user <- function(user_matrix) {
  common_genes <- intersect(rownames(reference_mat), rownames(user_matrix))
  if (length(common_genes) < 1000) {
    stop("Error: User data has too few overlapping genes with reference set. Check gene symbols.")
  }

  ref_subset <- reference_mat[common_genes, ]
  user_subset <- user_matrix[common_genes, , drop = FALSE]
  user_sample_names <- colnames(user_subset)
  combined_mat <- cbind(ref_subset, user_subset)

  score_result_all <- CAIScore(
    expr = combined_mat,
    geneset = target_genes,
    scaling = "minmax",
    summary_method = "sum",
    auc_nCores = 1,
    kcdf_type = "Gaussian",
    AMS_nbin = 10
  )

  user_scores <- score_result_all[user_sample_names, , drop = FALSE]
  final_data <- data.frame(
    SampleID = rownames(user_scores),
    CAIScore = user_scores$CAIScore
  )
  return(final_data)
}

# Same robust input reading strategy as your online code.
raw_data <- read.table(
  expr_file,
  header = TRUE,
  sep = "\t",
  quote = "",
  comment.char = "",
  check.names = FALSE,
  stringsAsFactors = FALSE,
  fill = TRUE
)

gene_col <- raw_data[, 1]
expr_data <- raw_data[, -1, drop = FALSE]

if (any(duplicated(gene_col))) {
  expr_data <- data.frame(lapply(expr_data, function(x) as.numeric(as.character(x))))
  expr_data <- aggregate(expr_data, by = list(Gene = gene_col), FUN = sum)
  rownames(expr_data) <- expr_data$Gene
  expr_data$Gene <- NULL
} else {
  rownames(expr_data) <- gene_col
}

user_expr_matrix <- expr_data
final_result <- get_caiscore_for_user(user_expr_matrix)

nom_obj <- nomogram(model_cph, lp = TRUE)
lp_to_points_func <- approxfun(x = nom_obj$lp$x.real, y = nom_obj$lp$x, rule = 2)
surv_estimator <- Survival(model_cph)

stage_factor <- factor(stage_value, levels = c("Stage I", "Stage II", "Stage III", "Stage IV"))
if (is.na(stage_factor)) {
  stop("Stage must be one of: Stage I, Stage II, Stage III, Stage IV")
}

out <- data.frame(
  SampleID = final_result$SampleID,
  CAIScore = as.numeric(final_result$CAIScore),
  Age = age_value,
  Stage = as.character(stage_factor),
  stringsAsFactors = FALSE
)

classify_escape <- function(total_points) {
  # Keep as a simple deterministic rule for local app output.
  # Thresholds can be replaced by your web production thresholds if needed.
  if (is.na(total_points)) return(NA_character_)
  if (total_points < 80) return("Low")
  if (total_points < 120) return("Medium")
  return("High")
}

for (i in seq_len(nrow(out))) {
  new_patient <- data.frame(
    CAIScore = out$CAIScore[i],
    Age = as.numeric(age_value),
    Stage = factor(as.character(stage_factor), levels = c("Stage I", "Stage II", "Stage III", "Stage IV"))
  )

  patient_lp <- predict(model_cph, newdata = new_patient, type = "lp")
  patient_points <- lp_to_points_func(patient_lp)

  out$Total_Points[i] <- round(patient_points, 2)
  out$OS_1_Year[i] <- round(surv_estimator(365, lp = patient_lp), 3)
  out$OS_2_Year[i] <- round(surv_estimator(730, lp = patient_lp), 3)
  out$OS_3_Year[i] <- round(surv_estimator(1095, lp = patient_lp), 3)
  out$OS_4_Year[i] <- round(surv_estimator(1460, lp = patient_lp), 3)
  out$OS_5_Year[i] <- round(surv_estimator(1825, lp = patient_lp), 3)
  out$Immune_Escape_Ability[i] <- classify_escape(out$Total_Points[i])
}

write.csv(out, out_csv, row.names = FALSE, fileEncoding = "UTF-8")
cat("OK\n")
