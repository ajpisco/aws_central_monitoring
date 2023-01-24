terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "~> 4.4"
      configuration_aliases = [aws.account]
    }
  }
  required_version = ">= 1.0.5"
}
