terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }

    backend "s3" {
        bucket = "hcong-s3-aiops-tf-state"
        key    = "terraform.tfstate"
        region = "us-west-1"
        dynamodb_table = "hcong-aiops-dynamodb-terraform-lock-state"
        encrypt = true
    }
}

provider "aws" {
  region = var.aws_region
}
