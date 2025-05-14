# Load necessary libraries
library(openxlsx)
library(future.apply)

# Set a reproducible random seed
set.seed(42)

# Define the parent directory containing input files
parent_dir <- "/home/superadmin/Filtered_Data"

# Define the directory for storing output files
output_dir <- "/home/superadmin/Benign_Filtered_Data"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Define the filtering criteria (looking for either "VUS" or "Pathogenic")
criteria <- c("VUS", "Pathogenic")

# Function to filter rows and write to an output file
filter_file <- function(input_file, output_file, criteria) {
  raw_data <- read.xlsx(input_file, sheet = 1)
  filtered_rows <- raw_data[!grepl(paste(criteria, collapse = "|"), raw_data$Classification, ignore.case = TRUE), ]
  write.xlsx(filtered_rows, file = output_file, rowNames = FALSE)
}

# Function to process individual files and maintain directory structure
process_single_file <- function(file_path) {
  tryCatch({
    relative_path <- gsub(parent_dir, "", dirname(file_path))
    output_subdir <- file.path(output_dir, relative_path)
    dir.create(output_subdir, showWarnings = FALSE, recursive = TRUE)

    output_file <- file.path(output_subdir, basename(file_path))
    if (file.exists(output_file)) {
      message("Skipped (already processed): ", file_path)
      return(NULL)
    }

    filter_file(file_path, output_file, criteria)
    message("Processed: ", file_path)
  }, error = function(e) {
    message("Error processing file: ", file_path, " - ", e$message)
  })
}

# Get a list of all xlsx files in subdirectories
xlsx_files <- list.files(path = parent_dir, pattern = "\\.xlsx$", recursive = TRUE, full.names = TRUE)

# Clean up old clusters and start multi-threaded plan
future:::ClusterRegistry("stop")
gc()
plan(multisession, workers = 4)

# Process files in parallel
future_lapply(xlsx_files, process_single_file)

message("Processing complete. Filtered files saved to: ", output_dir)
