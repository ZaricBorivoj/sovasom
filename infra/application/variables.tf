variable "aws_profile" {
  type        = string
  default     = null
  description = "Optional local AWS shared-config profile. Leave unset in CI to use OIDC credentials."
}

variable "aws_account_id" {
  type = string
  validation {
    condition     = can(regex("^[0-9]{12}$", var.aws_account_id))
    error_message = "Supply the actual 12-digit AWS account ID."
  }
}

variable "backup_bucket_name" {
  type        = string
  description = "Retained foundation output. This root references but never owns this bucket."
}

variable "hosted_zone_id" {
  type        = string
  description = "Existing public Route 53 zone ID; never recreated or destroyed here."
}

variable "app_hostname" {
  type = string
  validation {
    condition     = can(regex("^([a-z0-9]([a-z0-9-]*[a-z0-9])?\\.)+[a-z]{2,}$", var.app_hostname))
    error_message = "Supply a lowercase DNS hostname without a trailing dot or wildcard."
  }
}

variable "public_ipv4" {
  type        = string
  description = "Verified public static IPv4 routed to the Mac mini."
  validation {
    condition     = can(cidrnetmask("${var.public_ipv4}/32"))
    error_message = "Supply an IPv4 address without a CIDR suffix."
  }
}
