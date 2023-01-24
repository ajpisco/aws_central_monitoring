variable "s3_bucket" {
  description = "S3 bucket name to send the VPC flow logs"
}

variable "vpc_id" {
  description = "VPC ID which will have the logs sent"
}