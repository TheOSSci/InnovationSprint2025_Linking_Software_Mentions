# Data Lake for Software Mentions

This directory contains the code and configuration for building a data lake of software mentions from scientific literature and related sources. The approach leverages DuckDB, cloud object storage (R2), and automated extraction/loading scripts to create a scalable, reproducible pipeline for dataset ingestion and management.

The goal of this component is to get essentially raw data into the cloud data lake. Don't bother with complex transformations or cleaning at this stage. 

## Approach

- **Configuration**: Environment variables in `.env` specify R2 bucket credentials and base directory.
- **Extraction & Loading**: The `extract_load.py` script uses DuckDB to extract datasets from remote sources and load them into the R2 bucket as compressed Parquet files.
- **Automation**: Each dataset has a dedicated function for extraction and loading, making it easy to add new datasets.
- **Dependencies**: All required Python packages are listed in `requirements.txt`.

## Datasets

### CORD-19 Software Mentions
- **Source**: [CORD-19 software mentions CSV](https://zenodo.org/records/4582776/files/CORD19_software_mentions.csv?download=1)
- **Destination**: `r2://<bucket>/<base_directory>/czi/cord19_software_mentions.parquet`
- **Format**: Parquet (ZSTD compression)
- **Extraction Function**: `extract_and_load_cord_dataset(conn)`

### Softcite Dataset v2
- **Source**: [Softcite v2 JSON](https://raw.githubusercontent.com/softcite/softcite_dataset_v2/refs/heads/master/json/softcite_corpus-full.json)
- **Destination**: `r2://<bucket>/<base_directory>/softcite_v2/softcite_corpus-full.parquet`
- **Format**: Parquet (ZSTD compression)
- **Extraction Function**: `extract_and_load_softcite_v2(conn)`

## Contributor Guide: Adding New Datasets

1. **Add Extraction Function**: Create a new function in `extract_load.py` that:
    - Downloads the dataset (CSV, JSON, etc.) using DuckDB's `read_csv_auto` or `read_json`.
    - Writes the data to the R2 bucket in Parquet format.
2. **Update Main Script**: Call your new function in the `__main__` block.
3. **Document the Dataset**: Add a section to this README describing the new dataset (source, destination, format).
4. **Dependencies**: If new packages are needed, add them to `requirements.txt`.
5. **Testing**: Run the script to verify successful extraction and loading.

## Setup

1. Copy `.env.example` to `.env` and fill in your R2 credentials.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the extraction script:
   ```sh
   python extract_load.py
   ```

## License

See the main repository for license information.

## Contact

For questions or contributions, please open an issue or pull request.
