provider "google" {
  credentials = file("/home/aalopz/sharedFolder/key.json")
  project = var.project_id
  region  = var.region
} 