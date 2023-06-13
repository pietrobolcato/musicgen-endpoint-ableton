# general settings
variable "namespace" {
  type        = string
  description = "The namespace, used as prefix for resources names"
}

variable "postfix" {
  type        = string
  description = "Postfix for module names"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment, defaults to `dev`"
}

# elastic ip settings
variable "create_elastic_ip" {
  type        = bool
  default     = false
  description = "If true, creates an elastic IP and associates it with the instance"
}

# ec2 settings
variable "ami" {
  type        = string
  description = "AMI of the instance"
}

variable "instance_type" {
  type        = string
  default     = "t2.micro"
  description = "The compute instance type"
}

variable "public_key_path" {
  type        = string
  description = "If set, uses the provided public key. If `null`, assumes that a keypair already exists in AWS, with the name in the format set in the variable `key_name`"

  validation {
    condition     = var.public_key_path == null || endswith(var.public_key_path == null ? "" : var.public_key_path, ".pub")
    error_message = "The public_key_path must be null or end with `.pub`"
  }
}

variable "key_name" {
  type        = string
  default     = null
  description = "The key pair name to access the ec2 instance via ssh. If left blank, the name is automatically set as defined in the `locals.tf` file"
}

variable "root_block_delete_on_termination" {
  type        = bool
  default     = true
  description = "If true, delete EBS when destroying the EC2 instance"
}

variable "root_block_volume_size" {
  type        = number
  default     = 45
  description = "The size (in gb) of the EBS volume"
}