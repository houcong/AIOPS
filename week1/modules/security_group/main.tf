module "ec2_app" {
  source                 = "./modules/ec2"
  infra_env             = var.infra_env
  infra_role            = "app"
  instance_size         = var.instance_size
  instance_root_device_size = var.instance_root_device_size
}
