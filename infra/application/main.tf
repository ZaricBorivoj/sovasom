data "aws_s3_bucket" "backups" {
  bucket = var.backup_bucket_name
}

data "aws_route53_zone" "existing" {
  zone_id      = var.hosted_zone_id
  private_zone = false
}

resource "aws_route53_record" "application" {
  zone_id = data.aws_route53_zone.existing.zone_id
  name    = var.app_hostname
  type    = "A"
  ttl     = 300
  records = [var.public_ipv4]

  # Existing records must be deliberately imported, never silently overwritten.
  allow_overwrite = false
  lifecycle {
    precondition {
      condition     = !data.aws_route53_zone.existing.private_zone && (var.app_hostname == trimsuffix(data.aws_route53_zone.existing.name, ".") || endswith(var.app_hostname, ".${trimsuffix(data.aws_route53_zone.existing.name, ".")}"))
      error_message = "The application hostname must belong to the selected public hosted zone."
    }
  }
}

output "backup_bucket_name" {
  value = data.aws_s3_bucket.backups.id
}

output "application_origin" {
  value = "https://${var.app_hostname}"
}
