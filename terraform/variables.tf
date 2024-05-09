variable "region" {
  default     = "us-east1"
  description = "Region to which connect in GCP"
  type        = string
}

variable "project" {
  description = "Project to which connect in GCP"
  type    = string
}

variable "zone" {
  default = "us-east1-a"
  description = "Zone to which connect in GCP"
  type    = string
}

variable "app_name" {
  default     = "pyphoy-te"
  description = "Name of the application to deploy"
  type        = string
}

variable "pyphoy_container_image" {
  default     = "magnizide/pyphoy-te:latest"
  description = "Image path for pulling in vm metadata."
  type        = string
}

variable "tg_bot_token" {
  description = "Telegram secret token for the application to authenticate"
  type        = string
}
