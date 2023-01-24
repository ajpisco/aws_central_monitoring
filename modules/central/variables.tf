variable "region" {
  description = "Region to be used"
  type        = string
}

variable "quicksight_user_arn" {
  description = "(Mandatory) User ARN to grant access to Quicksight"
  type        = string
}