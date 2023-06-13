data "aws_region" "current" {}

resource "aws_vpc" "vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name = "vpc-${var.namespace}-${var.postfix}-${var.environment}"
  }
}

resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_subnet" "subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = aws_vpc.vpc.cidr_block
  availability_zone = "${data.aws_region.current.name}a"
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gateway.id
  }
}

resource "aws_route_table_association" "route_table_association" {
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH traffic"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
  }
}

resource "aws_security_group" "allow_http" {
  name        = "allow_http"
  description = "Allow HTTP traffic"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 0
    protocol    = "-1"
    to_port     = 0
  }
}

# create keypair if set in the config variables
resource "aws_key_pair" "aws_key" {
  count = var.public_key_path != null ? 1 : 0

  key_name   = local.key_name
  public_key = file(var.public_key_path)

  tags = local.tags
}

# create aws instance
resource "aws_instance" "instance" {
  ami                         = var.ami
  instance_type               = var.instance_type
  key_name                    = local.key_name
  associate_public_ip_address = true
  subnet_id                   = aws_subnet.subnet.id
  vpc_security_group_ids      = [aws_security_group.allow_ssh.id, aws_security_group.allow_http.id]

  root_block_device {
    delete_on_termination = var.root_block_delete_on_termination
    volume_size           = var.root_block_volume_size
    volume_type           = "gp3"
  }

  tags = merge(local.tags, {
    Name = "ec-${var.namespace}-${var.postfix}-${var.environment}"
  })
}

# elastic ip
resource "aws_eip" "instance_eip" {
  domain = "vpc"
}

resource "aws_eip_association" "instance_eip_association" {
  instance_id   = aws_instance.instance.id
  allocation_id = aws_eip.instance_eip.id
}