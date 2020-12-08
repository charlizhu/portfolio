locals {
  AWS_REGION  = "us-east-1"
  STATE_BUCKET = "bucket-to-test-if-things-work"
}
#need to figure out easier way to set variables for devs buckets, also some easier way to pull current env

remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = local.STATE_BUCKET

    key = "${path_relative_to_include()}/coupon-system.tfstate"
    region         = local.AWS_REGION 
    encrypt        = true
  }
}

generate "provider" {
    path = "provider.tf"
    if_exists = "overwrite_terragrunt"
    contents = <<EOF
    provider "aws" {
        region = "${local.AWS_REGION}" 
    }
    EOF
}