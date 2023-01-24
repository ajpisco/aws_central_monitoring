module "central" {
  source = "./modules/central"

  region      = "eu-west-1"
  account_ids = [for r in var.accounts_data : "${r.id}"]
  quicksight_user_arn = var.quicksight_user_arn
  providers = {
    aws.main = aws.main
  }
}

module "account1" {
  source = "./modules/sub_accounts"

  s3_bucket = module.central.s3_bucket
  vpc_id    = var.accounts_data.sub_account1.vpc_id

  providers = {
    aws.account = aws.sub_account1
  }
}
