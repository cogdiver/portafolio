# ETL (Cloud Build / Workflows / Cloud Functions / Cloud Run / GCS / PubSub / Dataflow / Bigquery)

Proof of concept for event handling with Pub/Sub and Dataflow, generated with Cloud Run and Bigquery as Data Warehouse, with Cloud Functions, Workflows, and Cloud SDK as triggers for test event generation.

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

## Cloud Build
Connecting a repository to Cloud Build in Google Cloud Platform involves the following steps:

1. Open the Cloud Build console in the Google Cloud Platform console.
2. In the menu on the left, select "Source connections".
3. Click on "Add connection".
4. Select the type of repository you want to connect. Cloud Build supports several types of repositories, such as Git, GitHub, Bitbucket, Cloud Source Repositories, and more.
5. Follow the instructions to authenticate your repository account and authorize Cloud Build to access your repositories.
6. Once you have connected your repository, you can create a new Cloud Build trigger that is connected to that repository.


To create a trigger, you can follow these steps:

1. Check that you have the necessary variables in `.env` file.
```bash
# Cloud Build
TRIGGER_NAME=<TRIGGER_NAME>
GITHUB_REPO_NAME=<GITHUB_REPO_NAME>
GITHUB_REPO_OWNER=<GITHUB_REPO_OWNER>
BRANCH_PATTERN=<BRANCH_PATTERN>
BUILD_CONFIG_FILE=<BUILD_CONFIG_FILE>
```

2. Execute the script.
```bash
sh scripts/create_trigger.sh
```
