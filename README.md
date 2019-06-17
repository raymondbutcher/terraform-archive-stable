# terraform-archive-stable

Terraform module to create zip archives with stable hashes.

Python is used to create these files. Terraform's `archive_file` data source sometimes [produces different results](https://github.com/terraform-providers/terraform-provider-archive/issues/34) which lead to spurious resource changes when working in teams. This module normalizes permissions and timestamps so the resulting file is consistent and only changes when there are meaningful changes to the source files.

It also contains a `search` feature. Given a list of [fnmatch](https://docs.python.org/2/library/fnmatch.html) patterns, it will return any matching file names included in the archive.

## Usage

```terraform
module "archive" {
  source = "github.com/raymondbutcher/terraform-archive-stable"

  source_dir  = "${path.module}/src"
  output_path = "${path.module}/out.zip"
  search      = ["build.sh"]
}

locals {
  has_build_script    = contains(module.archive.search_results, "build.sh")
  output_md5          = module.archive.output_md5
  output_sha          = module.archive.output_sha
  output_base64sha256 = module.archive.output_base64sha256
}
```
