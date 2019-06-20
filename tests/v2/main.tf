module "archive" {
  source      = "../"
  enabled     = false
  source_dir  = "src"
  output_path = "out.zip"
  search      = ["*.txt"]
}

output "output_md5" {
  value = module.archive.output_md5
}

output "search_results" {
  value = module.archive.search_results
}
