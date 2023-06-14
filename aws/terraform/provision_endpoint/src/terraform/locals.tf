locals {
  tags = {
    owner       = "pietrobolcato@gmail.com"
    project     = "musicgen-project"
    environment = "${var.environment}"
    toolkit     = "terraform"
  }
}