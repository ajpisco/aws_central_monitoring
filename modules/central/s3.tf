resource "aws_s3_bucket" "central_flow_logs" {
  bucket_prefix = "vpc-central-flow-logs-"

}

resource "aws_s3_bucket_acl" "central_flow_logs" {
  bucket = aws_s3_bucket.central_flow_logs.id
  acl    = "private"
}

resource "aws_s3_bucket_lifecycle_configuration" "central_flow_logs" {
  bucket = aws_s3_bucket.central_flow_logs.bucket

  rule {
    id = "delete"

    expiration {
      days = 90
    }

    status = "Enabled"
  }
}