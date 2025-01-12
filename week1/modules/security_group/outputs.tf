output "security_group_id" {
  value       = aws_security_group.this.id
  description = "The ID of the security group."
  
}

output "security_group_name" {
  value       = aws_security_group.this.name
  description = "The name of the security group."
  
}

