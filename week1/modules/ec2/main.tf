provider "aws" {
  region = var.default_region
}


resource "aws_instance" "app" {

  ami = var.ami_id
  instance_type = var.instance_size
  key_name = var.key_name
  vpc_security_group_ids = [var.security_group_id]
  subnet_id = var.subnet_id
  tags = {
    Name = "app-instance"
    Environment = var.infra_env
    Role = var.infra_role
    owner = "hcong"
  }
  root_block_device {
    volume_size = var.instance_root_device_size
  }
  # 安装docker
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              sudo chkconfig docker on
              EOF
 
}

