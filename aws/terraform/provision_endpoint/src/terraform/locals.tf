locals {
  tags = {
    owner       = "pietrobolcato@gmail.com"
    project     = "ex02"
    environment = "${var.environment}"
    toolkit     = "terraform"
    name        = "${var.namespace}-${var.postfix}-${var.environment}"
  }
}