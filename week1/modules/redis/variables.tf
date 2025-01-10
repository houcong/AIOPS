variable "region" {
  type        = string
  description = "AWS region to deploy the ElastiCache Redis cluster."
  default = "us-east-1"
}

variable "replication_group_id" {
  type        = string
  description = "ID of the replication group."
  default = "my-redis-cluster"
}

variable "replication_group_description" {
  type        = string
  description = "Description of the replication group."
  default     = "My Redis cluster"
}

variable "node_type" {
  type        = string
  description = "Node type for the Redis nodes."
  default = "cache.t2.micro"
}

variable "num_cache_nodes" {
  type        = number
  description = "Number of cache nodes in the replication group."
  default = 0
}

variable "engine_version" {
  type        = string
  description = "Version of the Redis engine."
  default = "5.0.6"
}

variable "parameter_group_family" {
  type        = string
  description = "Parameter group family for ElastiCache."
  default = "redis5.0"
}

variable "automatic_failover_enabled" {
  type        = bool
  description = "Enable automatic failover."
  default = false
}

variable "multi_az_enabled" {
  type        = bool
  description = "Enable Multi-AZ support."
  default = false
}

variable "maintenance_window" {
  type        = string
  description = "Maintenance window for the ElastiCache cluster."
  default = "sun:05:00-sun:06:00"
}

variable "apply_immediately" {
  type        = bool
  description = "Apply changes immediately."
  default = false
}

variable "tags" {
  type        = map(string)
  default     = {}
}
