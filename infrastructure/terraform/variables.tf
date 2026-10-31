variable "aws_region" {
  description = "Region de AWS para el despliegue"
  type        = string
  default     = "eu-west-1"
}

variable "environment" {
  description = "Entorno de despliegue (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Nombre identificador del proyecto"
  type        = string
  default     = "damm-knowledgeops"
}
