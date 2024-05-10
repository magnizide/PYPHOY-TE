module "compute" {
  source = "./modules/compute"

  app_name               = var.app_name
  pyphoy_container_image = var.pyphoy_container_image
  pyphoy_container_tag   = var.pyphoy_container_tag
  tg_bot_token           = var.tg_bot_token
}