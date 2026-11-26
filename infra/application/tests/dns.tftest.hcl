mock_provider "aws" {
  mock_data "aws_route53_zone" {
    defaults = { name = "example.com.", private_zone = false }
  }
}

run "reject_record_outside_existing_zone" {
  command = plan
  variables {
    app_hostname = "coffee.other.example"
  }
  expect_failures = [aws_route53_record.application]
}

run "reject_invalid_ipv4" {
  command = plan
  variables {
    public_ipv4 = "999.0.0.1"
  }
  expect_failures = [var.public_ipv4]
}

variables {
  aws_account_id     = "123456789012"
  backup_bucket_name = "coffee-disposable-test-123456789012-backups"
  hosted_zone_id     = "Z0123456789TEST"
  app_hostname       = "coffee.example.com"
  public_ipv4        = "192.0.2.10"
}

run "point_only_app_record_at_mini" {
  command = plan
  assert {
    condition     = aws_route53_record.application.records == toset(["192.0.2.10"]) && aws_route53_record.application.type == "A"
    error_message = "The application must route the app A record to the configured Mac mini."
  }
}
