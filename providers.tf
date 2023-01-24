provider "aws" {
  alias  = "main"
  region = "eu-west-1"
}

provider "aws" {
  alias  = "sub_account1"
  region = "eu-west-1"
  assume_role {
    role_arn = "arn:aws:iam::${var.account_ids.sub_account1.id}:role/assumed_role"
  }

  default_tags {
    tags = {
      APMID = var.apm_id
    }
  }
}