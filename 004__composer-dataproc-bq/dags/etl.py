# """ETL workflow"""

# Airflow dependencies
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup

# Google Cloud Storage
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.gcs import GCSDeleteBucketOperator

# Bigquery
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

# Dataproc
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocDeleteClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitPySparkJobOperator


from datetime import datetime


PROJECT_ID = "<PROJECT_ID>"

default_args = {
    "owner": "Airflow",
    "start_date": days_ago(2),
}

with DAG(
    dag_id="composer_dataproc",
    catchup=False,
    schedule_interval="0 0 * * *",
    default_args=default_args,
) as dag:

    create_temp_bucket = GCSCreateBucketOperator(
        task_id = "create_temp_bucket",
        bucket_name = "<BUCKET_2>",
        storage_class = "STANDARD",
        location = "us-east1",
    )

    move_objects_to_temp_bucket = GCSToGCSOperator(
        task_id = "move_objects_to_temp_bucket",
        source_bucket = "<BUCKET_1>",
        source_object = "*.txt",
        destination_bucket = "<BUCKET_2>",
        move_object=True,
        destination_object = datetime.now().strftime('%Y/%m/%d/'),
        # gcp_conn_id='google_cloud_default',
    )

    copy_objects_to_datalake = GCSToGCSOperator(
        task_id = "copy_objects_to_datalake",
        source_bucket = "<BUCKET_2>",
        source_object = "*.txt",
        destination_bucket = "<BUCKET_3>",
        # gcp_conn_id='google_cloud_default',
    )

    with TaskGroup(group_id='execute_dataproc_job') as execute_dataproc_job:
        create_cluster = DataprocCreateClusterOperator(
            task_id = "create_cluster",
            project_id = PROJECT_ID,
            cluster_name = "cluster-1-composer",
            region = "us-central1",
            zone="us-central1-a",
            num_workers = 2,
            image_version="2.0",
            master_machine_type="n1-standard-2",
            worker_machine_type="n1-standard-2",
            use_if_exists = True,
        )

        submit_job = DummyOperator(
        # DataprocSubmitPySparkJobOperator(
            task_id = "submit_job",
            # main = "gs://<BUCKET_1>/job.py",
            # cluster_name = "cluster-1-composer",
            # job_name = f"job-{datetime.now().strftime('%Y%m%d-%M%s')}",
            # region = "us-central1",
            # dataproc_jars = ['gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar'],
            # # job_type = "pyspark_job",
        )

        delete_cluster = DataprocDeleteClusterOperator(
            task_id = "delete_cluster",
            project_id = PROJECT_ID,
            cluster_name = "cluster-1-composer",
            region = "us-central1",
        )

#         create_cluster >> submit_job >> delete_cluster

    delete_temp_bucket = GCSDeleteBucketOperator(
        task_id = "delete_temp_bucket",
        bucket_name = "<BUCKET_2>",
    )

    with TaskGroup(group_id='execute_bigquery_sp') as execute_bigquery:
        execute_bigquery_sp1 = BigQueryExecuteQueryOperator(
            task_id = "execute_bigquery_sp1",
            sql = f"CALL `{PROJECT_ID}.<DATASET>.SP1`();",
            use_legacy_sql = False,
        )

        execute_bigquery_sp2 = BigQueryExecuteQueryOperator(
            task_id = "execute_bigquery_sp2",
            sql = f"CALL `{PROJECT_ID}.<DATASET>.SP2`();",
            use_legacy_sql = False,
        )

        execute_bigquery_sp3 = BigQueryExecuteQueryOperator(
            task_id = "execute_bigquery_sp3",
            sql = f"CALL `{PROJECT_ID}.<DATASET>.SP3`();",
            use_legacy_sql = False,
        )

    # tasks dependencies
    create_temp_bucket >> move_objects_to_temp_bucket
    move_objects_to_temp_bucket >> [copy_objects_to_datalake, submit_job] >> delete_temp_bucket
    submit_job >> [execute_bigquery_sp1 , execute_bigquery_sp2] >> execute_bigquery_sp3
