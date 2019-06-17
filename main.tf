terraform {
  required_version = ">= 0.12.0"
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
  program = ["python", "${path.module}/zip.py"]
  query = {
    source_dir  = var.source_dir
    output_path = var.output_path
    search      = jsonencode(var.search)
  }
}

output "output_md5" {
  value = data.external.archive.result.output_md5
}

output "output_path" {
  value = data.external.archive.result.output_path
}

output "output_sha" {
  value = data.external.archive.result.output_sha
}

output "output_base64sha256" {
  value = data.external.archive.result.output_base64sha256
}

output "search" {
  value = jsondecode(data.external.archive.result.search)
}

output "search_results" {
  value = jsondecode(data.external.archive.result.search_results)
}

output "source_dir" {
  value = data.external.archive.result.source_dir
}
