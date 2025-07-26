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

output "service_ip" {
  value       = kubernetes_service.app.status[0].load_balancer.ingress[0].ip
  description = "LoadBalancer IP (if available)"
  sensitive   = false
}