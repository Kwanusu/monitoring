# AWS Region
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

# VPC CIDR block
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# Public subnet CIDR block
variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

# Private subnet CIDR block
variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

# SSH Key Pair Name
variable "key_name" {
  description = "AWS key pair name for SSH access"
  type        = string
}

# Instance type for Master Node
variable "master_instance_type" {
  description = "EC2 instance type for the Master node"
  type        = string
  default     = "t3.micro"
}

# Instance type for Worker Node
variable "worker_instance_type" {
  description = "EC2 instance type for the Worker node"
  type        = string
  default     = "t3.micro"
}

# Project Name (for tagging)
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "flask-monitoring"
}

# Allow SSH (optional for security group)
variable "allow_ssh_cidr" {
  description = "CIDR blocks allowed to SSH (port 22)"
  type        = string
  default     = "0.0.0.0/0"
}

# Allow HTTP access (for Flask)
variable "allow_http_cidr" {
  description = "CIDR blocks allowed to access Flask app (port 5000)"
  type        = string
  default     = "0.0.0.0/0"
}
