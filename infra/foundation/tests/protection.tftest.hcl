mock_provider "aws" {}

variables {
  aws_account_id              = "123456789012"
  name                        = "coffee-disposable-test"
  github_oidc_subject         = "repo:example-org@12345678/office-ordering@87654321:ref:refs/heads/main"
  hosted_zone_id              = "Z0123456789TEST"
  app_hostname                = "coffee.example.com"
  create_github_oidc_provider = false
}

run "separate_workflow_privileges" {
  command = plan

  assert {
    condition     = jsondecode(aws_iam_role.workflow["backup"].assume_role_policy).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:sub"] == var.github_oidc_subject
    error_message = "Backup trust must match the exact trusted repository subject."
  }
  assert {
    condition     = jsondecode(aws_iam_role.workflow["infrastructure"].assume_role_policy).Statement[0].Condition.StringEquals["token.actions.githubusercontent.com:aud"] == "sts.amazonaws.com"
    error_message = "Infrastructure trust must validate the STS audience."
  }
  assert {
    condition     = length(aws_iam_openid_connect_provider.github) == 0
    error_message = "Shared GitHub OIDC provider must be referenced by default."
  }
  assert {
    condition     = alltrue([for s in jsondecode(aws_iam_role_policy.backup.policy).Statement : alltrue([for a in s.Action : startswith(a, "s3:") && !strcontains(a, "Delete")])])
    error_message = "Backup role must have only S3 archive access and cannot delete data or administer infrastructure."
  }
  assert {
    condition     = jsondecode(aws_iam_role_policy.infrastructure.policy).Statement[0].Resource == ["arn:aws:s3:::coffee-disposable-test-123456789012-state/application/terraform.tfstate"]
    error_message = "Infrastructure workflow must write only application state, never foundation state."
  }
}

run "retained_private_storage" {
  command = plan

  assert {
    condition     = aws_s3_bucket.retained["state"].force_destroy == false && aws_s3_bucket.retained["backups"].force_destroy == false
    error_message = "Both retained buckets must refuse forced emptying."
  }
  assert {
    condition     = alltrue([for b in aws_s3_bucket_public_access_block.retained : b.block_public_acls && b.block_public_policy && b.ignore_public_acls && b.restrict_public_buckets])
    error_message = "Neither state nor backups may become public."
  }
  assert {
    condition     = alltrue([for b in aws_s3_bucket_versioning.retained : b.versioning_configuration[0].status == "Enabled"])
    error_message = "Both buckets need recoverable versions."
  }
  assert {
    condition     = one([for r in aws_s3_bucket_lifecycle_configuration.backups.rule : r if r.id == "expire-archives"]).expiration[0].days == 30
    error_message = "Archive expiry must remain 30 days."
  }
  assert {
    condition     = one([for r in aws_s3_bucket_lifecycle_configuration.backups.rule : r if r.id == "expire-archives"]).noncurrent_version_expiration[0].noncurrent_days == 1
    error_message = "Old versions must be cleaned up as well as current archives."
  }
  assert {
    condition     = alltrue([for b in aws_s3_bucket_server_side_encryption_configuration.retained : one(b.rule).apply_server_side_encryption_by_default[0].sse_algorithm == "AES256"])
    error_message = "State and archives require encryption at rest."
  }
  assert {
    condition     = alltrue([for b in aws_s3_bucket_policy.retained : jsondecode(b.policy).Statement[0].Condition.Bool["aws:SecureTransport"] == "false" && jsondecode(b.policy).Statement[0].Effect == "Deny"])
    error_message = "Both buckets must reject unencrypted transport."
  }
}

run "reject_untrusted_github_subject" {
  command = plan
  variables {
    github_oidc_subject = "repo:example-org/office-ordering:pull_request"
  }
  expect_failures = [var.github_oidc_subject]
}

run "reject_wildcard_github_subject" {
  command = plan
  variables {
    github_oidc_subject = "repo:example-org/office-ordering:*"
  }
  expect_failures = [var.github_oidc_subject]
}
