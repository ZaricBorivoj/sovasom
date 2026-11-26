variable "aws_profile" {
  type        = string
  default     = null
  description = "Optional local AWS shared-config profile. Leave unset in CI to use OIDC credentials."
}

variable "aws_account_id" {
  type        = string
  description = "Expected AWS account; prevents accidental application to another account."
  validation {
    condition     = can(regex("^[0-9]{12}$", var.aws_account_id))
    error_message = "Supply the actual 12-digit AWS account ID."
  }
}

variable "name" {
  type        = string
  description = "Unique application/environment prefix for retained resources and IAM roles."
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,29}$", var.name))
    error_message = "Use 3–30 lowercase letters, digits or hyphens, starting with a letter."
  }
}

variable "github_oidc_subject" {
  type        = string
  description = "Exact observed GitHub OIDC sub for the trusted main branch or protected environment, including immutable IDs when enabled. No wildcards."
  validation {
    condition     = can(regex("^repo:[A-Za-z0-9_.-]+(@[0-9]+)?/[A-Za-z0-9_.-]+(@[0-9]+)?:(ref:refs/heads/main|environment:[A-Za-z0-9_.%-]+)$", var.github_oidc_subject))
    error_message = "Use an exact repository main-branch or protected-environment subject, without wildcards."
  }
}

variable "create_github_oidc_provider" {
  type        = bool
  default     = false
  description = "Set true only after confirming this account has no shared GitHub OIDC provider. Otherwise reference it without ownership."
}

variable "hosted_zone_id" {
  type        = string
  description = "Existing public Route 53 zone ID; Terraform does not own the zone."
}

variable "app_hostname" {
  type        = string
  description = "Lowercase FQDN without trailing dot; DNS write permissions are limited to this A record."
  validation {
    condition     = can(regex("^([a-z0-9]([a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$", var.app_hostname))
    error_message = "Supply a lowercase DNS hostname without a trailing dot or wildcard."
  }
}
