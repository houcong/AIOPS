# 创建 security group
module "security_group" {
  source = "./modules/security_group"
}


# 创建EC2
module "ec2_app_with_docker" {
  source                 = "./modules/ec2"
}
