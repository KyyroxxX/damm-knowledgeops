# Servicios de Deteccion Continua de Amenazas y Postura de Seguridad (CSPM)
# Ambos servicios ofrecen un periodo de prueba gratuito de 30 dias (Free Trial de AWS)

resource "aws_guardduty_detector" "primary" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = false
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = false
        }
      }
    }
  }

  tags = {
    Name        = "damm-kops-guardduty"
    Environment = var.environment
  }
}

resource "aws_securityhub_account" "primary" {
  enable_default_standards = true
  control_finding_generator = "SECURITY_CONTROL"
  auto_enable_controls     = true
}
