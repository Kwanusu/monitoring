variable "namespace" {
  description = "Kubernetes namespace to deploy into"
  type        = string
  default     = "default"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "flask-app"
}

variable "image" {
  description = "Docker image with tag"
  type        = string
}

variable "replicas" {
  description = "Number of replicas for the deployment"
  type        = number
  default     = 1
}

variable "container_port" {
  description = "Container port the app listens on"
  type        = number
  default     = 5000
}

variable "use_minikube" {
  description = "Flag to indicate Minikube environment"
  type        = bool
  default     = true
}