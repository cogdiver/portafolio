locals {
  services = [
    "bigquery.googleapis.com",
    "pubsub.googleapis.com",
    "cloudfunctions.googleapis.com",
  ]
  datasets = [
    "ml",
    "operational",
    "presentation",
    "raw",
  ]
}
