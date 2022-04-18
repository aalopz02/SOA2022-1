resource "google_storage_bucket" "function_bucket" {
  name = "${var.project_id}-function"
  location = var.region
}

data "google_iam_policy" "writer" {
  binding {
    role = "roles/storage.objectAdmin"
    members = [
        "allUsers",
    ] 
  }
}

resource "google_storage_bucket_iam_policy" "editor" {
  bucket = "${google_storage_bucket.input_bucket.name}"
  policy_data = "${data.google_iam_policy.writer.policy_data}"
}

resource "google_storage_bucket" "input_bucket" {
  name = "${var.project_id}-input"
  location = var.region
  force_destroy=true
  cors {
    origin          = ["http://201.206.66.59:5000"]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
  }
}