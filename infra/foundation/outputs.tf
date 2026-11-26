output "state_bucket_name" {
  value = local.buckets.state
}

output "backup_bucket_name" {
  value = local.buckets.backups
}

output "infrastructure_role_arn" {
  value = aws_iam_role.workflow["infrastructure"].arn
}

output "backup_role_arn" {
  value = aws_iam_role.workflow["backup"].arn
}
