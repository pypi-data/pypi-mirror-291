terraform {
  backend "s3" {
    bucket = "{{data.s3_bucket}}"
    key    = "{{data.tf_state_key}}"
    region = "{{data.s3_region}}"
  }
}