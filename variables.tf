variable "accounts_data" {
  type = map(any)
  default = {
    "sub_account1" : {
      "id" : "021862572004",
      "vpc_id" : "vpc-067832271f47df002"
    }
  }
}

variable "quicksight_user_arn" {
  description = "(Mandatory) User ARN to grant access to Quicksight"
  type        = string
}