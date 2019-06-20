terraform {
  required_version = ">= 0.12.0"
}

variable "empty_dirs" {
  type    = bool
  default = false
}

variable "enabled" {
  type    = bool
  default = true
}

variable "output_path" {
  type = string
}

variable "search" {
  type    = list(string)
  default = []
}

variable "source_dir" {
  type = string
}

data "external" "archive" {
  count = var.enabled ? 1 : 0

  program = ["python", "${path.module}/zip.py"]
  query = {
    empty_dirs  = jsonencode(var.empty_dirs)
    source_dir  = var.source_dir
    output_path = var.output_path
    search      = jsonencode(var.search)
  }
}

output "output_md5" {
  value = var.enabled ? data.external.archive[0].result.output_md5 : ""
}

output "output_path" {
  value = var.output_path
}

output "output_sha" {
  value = var.enabled ? data.external.archive[0].result.output_sha : ""
}

output "output_base64sha256" {
  value = var.enabled ? data.external.archive[0].result.output_base64sha256 : ""
}

output "search" {
  value = var.search
}

output "search_results" {
  value = jsondecode(var.enabled ? data.external.archive[0].result.search_results : "[]")
}

output "source_dir" {
  value = var.source_dir
}
