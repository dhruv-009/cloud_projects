provider "google" {
  credentials = "../assignment-k8-e0987f9a4341.json"
  project     = "assignment-k8"
  region      = "us-central1"
}

resource "google_cloudbuild_trigger" "container1_trigger" {
  name        = "container1-trigger"
  description = "Build trigger for Container 1"
  project     = "assignment-k8"
  location = "us-central1"
  
  trigger_template {
    branch_name = "main"
    repo_name   = "container1-csci5409"
  }
  substitutions = {
    "_IMAGE_NAME" = "gcr.io/assignment-k8/container1-image"
  }
  build {
    timeout = "600s"

    options {
      logging  = "CLOUD_LOGGING_ONLY"
    }

    step {
      name = "gcr.io/cloud-builders/docker"
      args = ["build", "-t", "gcr.io/assignment-k8/container1-image:latest", "."]
    }

    images = ["gcr.io/assignment-k8/container1-image:latest"]

    step {
      name = "gcr.io/cloud-builders/gcloud"
      entrypoint = "bash"
      env = ["KUBECONFIG=/kube/config"]
      args = [
        "-c",
        "gcloud container clusters get-credentials assignment-k8 --zone us-central1 --project assignment-k8; kubectl get ns production || kubectl create ns production; kubectl apply --namespace production --recursive -f k8s/deployments;"
      ]
    }
  }
}