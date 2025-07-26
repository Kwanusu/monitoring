output "namespace" {
  value = var.namespace
}

output "app_name" {
  value = var.app_name
}

output "deployment_status" {
  value       = kubernetes_deployment.app.status[0].ready_replicas
  description = "Number of ready replicas"
}

output "node_port" {
  value       = kubernetes_service.app.spec[0].ports[0].node_port
  description = "NodePort for the application"
}
