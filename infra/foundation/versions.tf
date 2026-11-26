terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 6.74.0"
    }
  }
}

provider "aws" {
  profile             = var.aws_profile
  region              = "eu-central-1"
  allowed_account_ids = [var.aws_account_id]
  default_tags {
    tags = { Project = var.name, ManagedBy = "Terraform", Ownership = "retained-foundation" }
  }
}
