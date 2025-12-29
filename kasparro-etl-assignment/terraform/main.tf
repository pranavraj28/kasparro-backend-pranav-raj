# Terraform configuration for AWS EC2 deployment
# Usage: terraform init && terraform plan && terraform apply

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Get latest Ubuntu 22.04 AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/host-ubuntu-22.04-jammy-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Security Group
resource "aws_security_group" "kasparro_etl" {
  name        = "kasparro-etl-sg"
  description = "Security group for Kasparro ETL system"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP (for nginx)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "kasparro-etl-sg"
  }
}

# EC2 Instance
resource "aws_instance" "kasparro_etl" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.kasparro_etl.id]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y curl git
              
              # Install Docker
              curl -fsSL https://get.docker.com -o get-docker.sh
              sh get-docker.sh
              
              # Install Docker Compose
              curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              
              # Clone repository (you'll need to do this manually or use a different method)
              # git clone https://github.com/your-username/kasparro-backend-pranav-raj.git
              # cd kasparro-backend-pranav-raj
              # ./deploy.sh
              EOF

  tags = {
    Name = "kasparro-etl-instance"
  }
}

# Output
output "instance_public_ip" {
  value       = aws_instance.kasparro_etl.public_ip
  description = "Public IP of the EC2 instance"
}

output "instance_public_dns" {
  value       = aws_instance.kasparro_etl.public_dns
  description = "Public DNS of the EC2 instance"
}

output "api_url" {
  value       = "http://${aws_instance.kasparro_etl.public_ip}:8000"
  description = "API endpoint URL"
}

