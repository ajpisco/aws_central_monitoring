variable "region" {
  description = "Region to be used"
  type        = string
}

variable "account_ids" {
  description = "List of account IDs to allow sending the logs to the S3 bucket"
  type        = list(string)
}

variable "quicksight_user_arn" {
  description = "(Mandatory) User ARN to grant access to Quicksight"
  type        = string
}