resource "aws_cloudwatch_log_group" "image_lambda" {
  name              = "/aws/lambda/image_upload"
  retention_in_days = 365
}

resource "aws_cloudwatch_log_group" "checking_lambda" {
  name              = "/aws/lambda/image_verified"
  retention_in_days = 365
}

