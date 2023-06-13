terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.3.0"
    }
  }

  backend "s3" {
    bucket         = "pbolcato-tf-state-dev"
    key            = "<NAMESPACE>/sagemaker/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-dev"
  }
}

provider "aws" {
  region = "us-east-1"
}