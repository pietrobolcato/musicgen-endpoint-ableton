terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0.0" # 4.67.0
    }
  }

  backend "s3" {
    bucket         = "pbolcato-tf-state-dev"
    key            = "ai-module/ec2/terraform.tfstate" # change this
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-dev"
  }
}

provider "aws" {
  region = "us-east-1"
}