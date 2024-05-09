module "gce-container" {
  source  = "terraform-google-modules/container-vm/google"
  version = "~> 3.0"

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
  }

  boot_disk {
    initialize_params {
      image = module.gce-container.source_image
    }
  }

  metadata = {
    gce-container-declarations = module.gce-container.metadata_value
    google-logging-enabled     = "true"
    google-monitoring-enabled  = "true"
  }

  labels = {
    container-vm = module.gce-container.vm_container_label
  }
}