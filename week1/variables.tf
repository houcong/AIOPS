variable "aws_region" {
  description = "The AWS region to deploy resources."
  default     = "us-west-1"
  
}

variable "infra_env" {
  type        = string
  description = "Infrastructure environment (e.g., dev, prod)"
  default = "dev"
}

variable "infra_role" {
  type        = string
  description = "Infrastructure purpose (e.g., app, worker)"
  default     = "app"
}

variable "instance_size" {
  type        = string
  description = "EC2 instance size"
  default     = "t2.medium"
}

variable "instance_root_device_size" {
  type        = number
  description = "Root block device size in GB"
  default     = 40
}

variable "default_region" {
  type        = string
  description = "The region this infrastructure is in"
  default     = "us-east-2"
}

variable "vpc_id" {
  type        = string
  description = "The VPC ID to deploy resources."
  default = "vpc-0a82a61659c629a5a"
}

variable "subnet_id" {
  type        = string
  description = "The subnet ID to deploy resources."
  default = "subnet-02926446e59c50c1d"
}

variable "security_group_id" {
  type        = string
  description = "The security group ID to deploy resources."
  default = "sg-0336bf78eae562f7f"
}

variable "key_name" {
  type        = string
  description = "The key pair name to deploy resources"
  default = "rocher"
}

variable "ami_id" {
  type        = string
  description = "The AMI ID to deploy resources."
  default = "ami-0938c2c0d02d50fe1"
}