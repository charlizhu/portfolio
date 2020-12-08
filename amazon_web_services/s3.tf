resource "aws_s3_bucket" "avatar_bucket" {
  bucket = "yalty-dev-users"
  acl    = "private"

  tags = {
    Name        = "Avatar Bucket in DEV"
    Environment = "Dev"
  }
}

# resource "aws_s3_bucket" "avatar_bucket" {
#   bucket = "yalty-stage-users"
#   acl    = "private"

#   tags = {
#     Name        = "Avatar Bucket in STAGE"
#     Environment = "Stage"
#   }
# }

# resource "aws_s3_bucket" "avatar_bucket" {
#   bucket = "yalty-prod-users"
#   acl    = "private"

#   tags = {
#     Name        = "Avatar Bucket in PROD"
#     Environment = "Prod"
#   }
# }