resource "aws_api_gateway_rest_api" "UserAvatarAPI" {
  name        = "UserAvatarAPI"
  description = "For when user uploads an Avatar"
  body        = data.template_file.endpoint_yaml.rendered
}

data "template_file" "endpoint_yaml" {
  template = file("${path.module}/endpoints.yml")

  vars = {
    # Lambda functions
    fxn_arn = aws_lambda_function.image_lambda.invoke_arn
    check_arn = aws_lambda_function.check_lambda.invoke_arn
  }
}

resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowUserAvatarAPIInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "image_upload"
  principal     = "apigateway.amazonaws.com"

  # The /*/*/* part allows invocation from any stage, method and resource path
  # within API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.UserAvatarAPI.execution_arn}/*/*/*"
}