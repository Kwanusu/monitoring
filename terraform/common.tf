resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "${var.app_name}-config"
    namespace = var.namespace
  }

  data = {
    FLASK_ENV = "production"
    DEBUG     = "False"
  }
}

resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "${var.app_name}-secret"
    namespace = var.namespace
  }

  data = {
    DB_PASSWORD = base64encode("changeme")
  }
}

resource "kubernetes_horizontal_pod_autoscaler_v2" "app_hpa" {
  metadata {
    name      = "${var.app_name}-hpa"
    namespace = var.namespace
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = var.app_name
    }

    min_replicas = 2
    max_replicas = 5

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 70
        }
      }
    }
  }
}
