module "central" {
  source = "./modules/central"

  region      = "eu-west-1"
  quicksight_user_arn = var.quicksight_user_arn
}
