locals {
  tags = {
    owner       = "pietrobolcato@gmail.com"
    project     = "ai-module-template"
    environment = "${var.environment}"
    toolkit     = "terraform"
  }

  key_name = var.key_name != null ? var.key_name : "key-${var.namespace}-${var.postfix}-${var.environment}"
}