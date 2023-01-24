resource "aws_s3_bucket" "central_flow_logs" {
  bucket_prefix = "vpc-central-flow-logs-"

}

resource "aws_s3_bucket_policy" "central_flow_logs" {
  bucket = aws_s3_bucket.central_flow_logs.id
  policy = data.aws_iam_policy_document.central_flow_logs.json
}

data "aws_iam_policy_document" "central_flow_logs" {
  statement {
    principals {
      type        = "AWS"
      identifiers = var.account_ids
    }

    actions = [
      "s3:PutObject",
    ]

    resources = [
      aws_s3_bucket.central_flow_logs.arn,
      "${aws_s3_bucket.central_flow_logs.arn}/*",
    ]
  }
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