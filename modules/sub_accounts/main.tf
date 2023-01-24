resource "aws_flow_log" "accounts" {
  log_destination      = var.s3_bucket.arn
  log_destination_type = "s3"
  traffic_type         = "ALL"
  vpc_id               = var.vpc_id
  destination_options {
    file_format        = "parquet"
    per_hour_partition = false
  }
}