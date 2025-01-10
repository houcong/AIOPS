provider "aws" {
  region = var.region
}

resource "aws_elasticache_replication_group" "this" {
  replication_group_id          = var.replication_group_id
  replication_group_description = var.replication_group_description
  node_type                     = var.node_type
  number_cache_clusters         = var.num_cache_nodes
  engine                        = "redis"
  engine_version                = var.engine_version
  parameter_group_name          = aws_elasticache_parameter_group.this.name
  automatic_failover_enabled    = var.automatic_failover_enabled
  multi_az_enabled              = var.multi_az_enabled
  maintenance_window            = var.maintenance_window
  apply_immediately             = var.apply_immediately
  description                   = "ElastiCache replication group for ${var.replication_group_id}"

  tags = merge(
    {
      Name = var.replication_group_id
    },
    var.tags
  )
}

resource "aws_elasticache_parameter_group" "this" {
  name   = "${var.replication_group_id}-parameter-group"
  family = var.parameter_group_family

  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"
  }
}

output "replication_group_id" {
  value       = aws_elasticache_replication_group.this.id
  description = "The ID of the ElastiCache replication group."
}

output "primary_endpoint" {
  value       = aws_elasticache_replication_group.this.primary_endpoint_address
  description = "The primary endpoint address of the Redis cluster."
}
