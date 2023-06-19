provider "google" {
  credentials = "./assignment-k8-e0987f9a4341.json"
  project     = "assignment-k8"
  region      = "us-central1"
}

resource "google_container_cluster" "my_cluster" {
  name               = "assignment-k8"
  location           = "us-central1"
  initial_node_count = 1

  master_auth {
    client_certificate_config {
      issue_client_certificate = false
    }
  }

  node_config {
    preemptible  = false
    machine_type = "e2-micro"
    disk_size_gb = 10

    image_type = "COS_CONTAINERD"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    service_account = "k8saccount@assignment-k8.iam.gserviceaccount.com"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
