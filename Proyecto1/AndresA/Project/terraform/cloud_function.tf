data "archive_file" "source"{
    type = "zip"
    source_dir = "${path.module}/cloud_function"
    output_path = "${path.module}/cloud_function/cloud_function.zip"
}

resource "google_storage_bucket_object" "zip" {
  source = data.archive_file.source.output_path
  content_type = "application/zip"
  name = "src-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  depends_on = [
    google_storage_bucket.function_bucket,
    data.archive_file.source
  ]
}

resource "google_cloudfunctions_function" "function" {
  name = "main"
  runtime = "python37"

  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  entry_point = "main"

  event_trigger{
      event_type="google.storage.object.finalize"
      resource = "${var.project_id}-input"
  }

  depends_on = [
        google_storage_bucket.function_bucket,  
        google_storage_bucket_object.zip
  ]
}