# Streamline Notify: An Event-Driven ETL Pipeline

The project focuses on implementing a cloud-based data processing system for efficiently managing files from multiple clients. The main objective is to clean and store the received files using real-time streaming. The system utilizes Google Cloud Platform (GCP) services to achieve this functionality.

## Steps for File Processing

1. File Ingestion: Files are uploaded to a cloud storage bucket (`${BUCKET}_load`) as the entry point of the system. They can originate from multiple clients and be in different formats.

2. File Movement: To prevent modifications by clients, the files are moved to another bucket (`${BUCKET}_raw`) using a unique prefix generated from the insertion date and time. This ensures the integrity of the original files.

3. Insert File Information into BigQuery: After the file has been successfully moved, the Cloud Function retrieves the file's name and record count. Using the BigQuery client library, the function inserts a new row into the designated BigQuery table (`$INFO_TABLE`).
>The row includes the following information: File ID (the file name with the unique prefix), File Name (the original name of the file), and Record Count (the number of records in the file).

4. Insertion into Pub/Sub Queue: Through a Dataflow job (`$JOB_ROWS`), each file is processed, and each record is inserted into a Pub/Sub queue. This allows real-time and scalable processing of the data.

5. Cleaning and Storage in BigQuery: Another Dataflow job (`$JOB_CLEAN`) is responsible for cleaning the data and storing it in BigQuery. The records are inserted into a column named "records" as strings.

![architecture](./docs/architecture.png)


## Project Folder Structure

```
project/
├── docs/
│   └── ...
├── function/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── scripts/
│   ├── set_env_values.sh
│   ├── set_gcp_login.sh
│   ├── project_up.sh
│   ├── project_down.sh
│   └── ...
├── transforms/
│   ├── udf.js
│   └── ...
├── init_db.sql
├── .env.sample
└── README.md
```

The project folder structure is organized as follows:

- **function/**: Contains the code for the Cloud Function, including the `main.py` file and the `requirements.txt` file specifying the dependencies.

- **scripts/**: Contains various shell scripts for project setup and teardown, including:
  - **set_env_values.sh**: Bash script to replace placeholder values in files with provided environment variables.
  - **set_gcp_login.sh**: Bash script to set the GCP login and project configurations.
  - **project_up.sh**: Bash script to set up the project infrastructure, including creating BigQuery datasets, Cloud Storage buckets, Pub/Sub topics and subscriptions, running Dataflow jobs and deploying the Cloud Function.
  - **project_down.sh**: Bash script to tear down the project infrastructure, including deleting BigQuery datasets, Cloud Storage buckets, Pub/Sub topics and subscriptions, canceling Dataflow jobs and removing the Cloud Function.

- **transforms/**: Contains the JavaScript UDF (User-Defined Function) file for data transformation.

- **init_db.sql**: SQL script to initialize the BigQuery tables.
- **.env.sample**: Sample environment file containing placeholders for configuration values.
- **README.md**: Project documentation and instructions.

The folder structure provides an organized layout for the project files and scripts, making it easier to manage and maintain the different components of the project.

## Usage

1. Copy `.env.sample` to `.env` and provide the necessary configuration values.
2. Run `./set_env_values.sh` to replace placeholders in files with provided values.
3. Run `./project_up.sh` to set up the project and deploy resources.
4. Copy local files to the load bucket using the following command:

```bash
./set_gcp_login.sh
# Replace filename with the actual name of the file you want to copy.
gsutil cp filename gs://${BUCKET}_load/
```
5. Run `./project_down.sh` to tear down the project and remove resources.
