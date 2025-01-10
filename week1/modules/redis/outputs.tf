output "replication_group_id" {
  value       = aws_elasticache_replication_group.this.id
  description = "The ID of the ElastiCache replication group."
}

output "primary_endpoint" {
  value       = aws_elasticache_replication_group.this.primary_endpoint_address
  description = "The primary endpoint address of the Redis cluster."
}
