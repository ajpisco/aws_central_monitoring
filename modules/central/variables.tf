variable "region" {
  description = "Region to be used"
  type        = string
}

variable "quicksight_user_arn" {
  description = "(Mandatory) User ARN to grant access to Quicksight"
  type        = string
}

variable "s3_bucket_name" {
  description = "(Mandatory) VPC flow logs bucket name"
  type        = string
}