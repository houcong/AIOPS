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
  default     = "us-east-1"
}

variable "vpc_id" {
  type        = string
  description = "The VPC ID to deploy resources."
  default = "vpc-0711ba9b734b968c7"
}

variable "subnet_id" {
  type        = string
  description = "The subnet ID to deploy resources."
  default = "subnet-0124bdfb371947be1"
}

variable "security_group_id" {
  type        = string
  description = "The security group ID to deploy resources."
  default = "sg-0406e05bf5ea1deef"
}

variable "key_name" {
  type        = string
  description = "The key pair name to deploy resources"
  default = "aos"
}

variable "ami_id" {
  type        = string
  description = "The AMI ID to deploy resources."
  default = "ami-05576a079321f21f8"
}