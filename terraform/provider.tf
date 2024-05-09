provider "google" {
  project = var.project
  region  = var.region
}

terraform {
  required_version = "1.8.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.57.0"
    }
  }
  backend "gcs" {}
}