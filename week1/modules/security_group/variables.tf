variable "aws_region" {
  description = "The AWS region to launch the resources."
  type        = string
  default     = "us-east-1"
  
}

variable "vpc_id" {
  description = "The VPC ID to deploy resources."
  type        = string
  default     = "vpc-0711ba9b734b968c7"
  
}