locals {
  buckets = {
    state   = "${var.name}-${var.aws_account_id}-state"
    backups = "${var.name}-${var.aws_account_id}-backups"
  }
  bucket_arns = { for purpose, name in local.buckets : purpose => "arn:aws:s3:::${name}" }
}

resource "aws_s3_bucket" "retained" {
  for_each      = local.buckets
  bucket        = each.value
  force_destroy = false
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_public_access_block" "retained" {
  for_each                = local.buckets
  bucket                  = aws_s3_bucket.retained[each.key].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "retained" {
  for_each = local.buckets
  bucket   = aws_s3_bucket.retained[each.key].id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "retained" {
  for_each = local.buckets
  bucket   = aws_s3_bucket.retained[each.key].id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "retained" {
  for_each = local.buckets
  bucket   = aws_s3_bucket.retained[each.key].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_policy" "retained" {
  for_each = local.buckets
  bucket   = aws_s3_bucket.retained[each.key].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = concat([
      {
        Sid       = "DenyInsecureTransport"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource  = [local.bucket_arns[each.key], "${local.bucket_arns[each.key]}/*"]
        Condition = { Bool = { "aws:SecureTransport" = "false" } }
      }
      ], each.key == "state" ? [{
        Sid       = "PreserveStateVersions"
        Effect    = "Deny"
        Principal = "*"
        Action    = ["s3:DeleteObject", "s3:DeleteObjectVersion"]
        Resource  = ["${local.bucket_arns.state}/foundation/terraform.tfstate", "${local.bucket_arns.state}/application/terraform.tfstate"]
    }] : [])
  })
  depends_on = [aws_s3_bucket_public_access_block.retained]
}

# State intentionally has no lifecycle/expiry configuration.
resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.retained["backups"].id
  rule {
    id     = "expire-archives"
    status = "Enabled"
    filter {
      prefix = "archives/"
    }
    expiration {
      days = 30
    }
    noncurrent_version_expiration {
      noncurrent_days = 1
    }
    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }
  }
  rule {
    id     = "remove-expired-markers"
    status = "Enabled"
    filter {
      prefix = "archives/"
    }
    expiration {
      expired_object_delete_marker = true
    }
  }
  depends_on = [aws_s3_bucket_versioning.retained]
}
