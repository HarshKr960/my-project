# Load necessary libraries
library(openxlsx)
library(future.apply)

# Set a reproducible random seed
set.seed(42)

# Define the parent directory containing input files
parent_dir <- "/home/omicslogic/Test_Filtered_Data_NP"

# Define the directory for storing output files
output_dir <- "/home/omicslogic/Variant_Allele_Filtered_Data_NP"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Function to filter rows and apply replacements
filter_file <- function(input_file, output_file) {
  # Read input file
  raw_data <- read.xlsx(input_file, sheet = 1)

  # Replace values > 1 with a dot (.) but keep 0 and . unchanged
  raw_data$Allele.Frequencies[raw_data$Allele.Frequencies > 1] <- "."

  # Convert Allele.Frequencies to numeric (if needed, after replacement)
  raw_data$Allele.Frequencies <- suppressWarnings(as.numeric(raw_data$Allele.Frequencies))

  # Filter out rows with Allele.Frequencies > 0.05 but retain 0 and .
  filtered_rows <- raw_data[raw_data$Allele.Frequencies <= 0.05 | raw_data$Allele.Frequencies == 0 | raw_data$Allele.Frequencies == ".", ]

  # Write filtered data to output file
  write.xlsx(filtered_rows, file = output_file, rowNames = FALSE)
}

# Function to process individual files and maintain directory structure
process_single_file <- function(file_path) {
  tryCatch({
    # Maintain subdirectory structure
    relative_path <- gsub(parent_dir, "", dirname(file_path))
    output_subdir <- file.path(output_dir, relative_path)
    dir.create(output_subdir, showWarnings = FALSE, recursive = TRUE)

    # Define output file path
    output_file <- file.path(output_subdir, basename(file_path))

    # Skip processing if file already exists
    if (file.exists(output_file)) {
      message("Skipped (already processed): ", file_path)
      return(NULL)
    }

    # Process and filter file
    filter_file(file_path, output_file)
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

message("Filtering complete. Filtered files saved to: ", output_dir)
