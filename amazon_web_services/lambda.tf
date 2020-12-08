resource "aws_iam_role" "image_uploading_fxn" {
  name = "image_uploading_fxn"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "image_lambda" {
  filename      = "./python/test.zip"
  function_name = "image_upload"
  role          = aws_iam_role.image_uploading_fxn.arn
  handler       = "test.lambda_handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("./python/test.zip")

  runtime = "python3.8"

    environment {
    variables = {
      AWS_ACCOUNT_ID = data.aws_caller_identity.current.account_id
      AWS_CUR_REGION = "us-east-1"
    }
  }

  depends_on = [aws_cloudwatch_log_group.image_lambda]

}

resource "aws_lambda_permission" "image_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = "image_upload"
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "${aws_api_gateway_rest_api.UserAvatarAPI.execution_arn}/*/*/*"
}

resource "aws_iam_role" "image_check_fxn" {
  name = "image_check_fxn"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "check_lambda" {
  filename      = "./python/set_has_avatar.zip"
  function_name = "image_verified"
  role          = aws_iam_role.image_check_fxn.arn
  handler       = "set_has_avatar.lambda_handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("./python/set_has_avatar.zip")

  runtime = "python3.8"

    environment {
    variables = {
      AWS_ACCOUNT_ID = data.aws_caller_identity.current.account_id
      AWS_CUR_REGION = "us-east-1"
    }
  }

  depends_on = [aws_cloudwatch_log_group.checking_lambda]

}

resource "aws_lambda_permission" "check_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = "image_verified"
  principal     = "apigateway.amazonaws.com"

  # More: http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html
  source_arn = "${aws_api_gateway_rest_api.UserAvatarAPI.execution_arn}/*/*/*"
}