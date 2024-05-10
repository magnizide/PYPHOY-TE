module "gce-container" {
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 3.0"

  cos_image_family = "stable"

  container = {
    image = var.pyphoy_container_image
    env = [
      {
        name  = "TG_BOT_TOKEN"
        value = "${var.tg_bot_token}"
      }
    ]
  }

  restart_policy = "Always"
}

resource "google_compute_instance" "instance" {
  name         = var.app_name
  machine_type = "e2-micro"

  network_interface {
    network = "default"
    access_config {}
  }

  boot_disk {
    initialize_params {
      image = module.gce-container.source_image
    }
  }

  metadata = {
    gce-container-declaration = module.gce-container.metadata_value
    google-logging-enabled    = "true"
    google-monitoring-enabled = "true"
  }

  labels = {
    container-vm = module.gce-container.vm_container_label
  }

  service_account {
    email = "magni-bot@magniops-dev.iam.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }
}
