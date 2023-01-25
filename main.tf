module "central" {
  source = "./modules/central"

  region      = "eu-west-1"
  s3_bucket_name = var.s3_bucket_name
  quicksight_user_arn = var.quicksight_user_arn
}
