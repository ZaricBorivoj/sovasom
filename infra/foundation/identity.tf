locals {
  github_provider_arn = "arn:aws:iam::${var.aws_account_id}:oidc-provider/token.actions.githubusercontent.com"
}

data "aws_iam_openid_connect_provider" "github" {
  count = var.create_github_oidc_provider ? 0 : 1
  arn   = local.github_provider_arn
}

resource "aws_iam_openid_connect_provider" "github" {
  count          = var.create_github_oidc_provider ? 1 : 0
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_iam_role" "workflow" {
  for_each             = toset(["infrastructure", "backup"])
  name                 = "${var.name}-${each.key}"
  max_session_duration = 3600
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRoleWithWebIdentity"
      Principal = { Federated = local.github_provider_arn }
      Condition = { StringEquals = {
        "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
        "token.actions.githubusercontent.com:sub" = var.github_oidc_subject
      } }
    }]
  })
  depends_on = [aws_iam_openid_connect_provider.github, data.aws_iam_openid_connect_provider.github]
}

# This role manages the disposable application root only. Foundation changes,
# including changes to these IAM policies, require independent operator access.
resource "aws_iam_role_policy" "infrastructure" {
  name = "application-infrastructure"
  role = aws_iam_role.workflow["infrastructure"].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ApplicationState"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = ["${local.bucket_arns.state}/application/terraform.tfstate"]
      },
      {
        Sid      = "ApplicationLock"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
        Resource = ["${local.bucket_arns.state}/application/terraform.tfstate.tflock"]
      },
      {
        Sid       = "ListApplicationState"
        Effect    = "Allow"
        Action    = ["s3:ListBucket"]
        Resource  = [local.bucket_arns.state]
        Condition = { StringLike = { "s3:prefix" = ["application/*"] } }
      },
      {
        Sid      = "ReadRetainedBucketMetadata"
        Effect   = "Allow"
        Action   = ["s3:GetBucketLocation", "s3:ListBucket"]
        Resource = [local.bucket_arns.backups]
      },
      {
        Sid      = "ReadExistingZone"
        Effect   = "Allow"
        Action   = ["route53:GetHostedZone", "route53:ListResourceRecordSets", "route53:ListTagsForResource"]
        Resource = ["arn:aws:route53:::hostedzone/${var.hosted_zone_id}"]
      },
      {
        Sid      = "ApplicationRecordOnly"
        Effect   = "Allow"
        Action   = ["route53:ChangeResourceRecordSets"]
        Resource = ["arn:aws:route53:::hostedzone/${var.hosted_zone_id}"]
        Condition = { "ForAllValues:StringEquals" = {
          "route53:ChangeResourceRecordSetsNormalizedRecordNames" = [var.app_hostname]
          "route53:ChangeResourceRecordSetsRecordTypes"           = ["A"]
          "route53:ChangeResourceRecordSetsActions"               = ["CREATE", "UPSERT", "DELETE"]
        } }
      },
      {
        Sid      = "WaitForDNSChange"
        Effect   = "Allow"
        Action   = ["route53:GetChange"]
        Resource = ["arn:aws:route53:::change/*"]
      }
    ]
  })
}

resource "aws_iam_role_policy" "backup" {
  name = "archive-transfer"
  role = aws_iam_role.workflow["backup"].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "ListArchives"
        Effect    = "Allow"
        Action    = ["s3:ListBucket"]
        Resource  = [local.bucket_arns.backups]
        Condition = { StringLike = { "s3:prefix" = ["archives/*"] } }
      },
      {
        Sid      = "TransferEncryptedArchives"
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:GetObject", "s3:GetObjectVersion", "s3:AbortMultipartUpload", "s3:ListMultipartUploadParts"]
        Resource = ["${local.bucket_arns.backups}/archives/*"]
      }
    ]
  })
}
