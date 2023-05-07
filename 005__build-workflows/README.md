# ETL (Cloud Build / Workflows / Cloud Functions / Cloud Run / GCS / PubSub / Dataflow / Bigquery)

Proof of concept for event handling with Pub/Sub and Dataflow, generated with Cloud Run and Bigquery as Data Warehouse, with Cloud Functions, Workflows and Cloud SDK as triggers for test event generation.

![architecture](./docs/architecture.png)


## Configure enviroment

Create .env file
```bash
cp .env.sample .env
```

Replace values for GCP information
```
ACCOUNT=<ACCOUNT>
PROJECT=<PROJECT_ID>
```