terraform {
  required_version = ">= 1.8.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Project     = "DammKnowledgeOps"
      Environment = "dev"
      ManagedBy   = "Terraform"
      Challenge   = "MetropolisFPLab"
    }
  }
}
