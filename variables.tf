variable "accounts_data" {
  type = map(any)
  default = {
    "sub_account1" : {
      "id" : "012345678901",
      "vpc_id" : "vpc-131091071074"
    }
  }
}

variable "quicksight_user_arn" {
  description = "(Mandatory) User ARN to grant access to Quicksight"
  type        = string
}