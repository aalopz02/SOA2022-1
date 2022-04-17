provider "google" {
  credentials = file("/home/aalopz/sharedFolder/keyAdmin.json")
  project = var.project_id
  region  = var.region
} 