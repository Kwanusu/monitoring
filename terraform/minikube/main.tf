provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

resource "kubernetes_namespace" "flask" {
  metadata {
    name = "flask-app"
  }
}

resource "helm_release" "monitoring" {
  name       = "monitoring"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = "monitoring"
  create_namespace = true
}

resource "kubernetes_deployment" "flask" {
  # Deployment definition (same as previous)
}

resource "kubernetes_service" "flask" {
  # LoadBalancer service or ClusterIP with port-forward
}
