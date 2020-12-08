data "aws_iam_policy" "lambda_exec" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy" "dynamo_exec" {
  arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

data "aws_iam_policy" "needs_fixing" {
  arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_iam_policy" "cloud_permissions" {
  name = "image_lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:PutLogEvents",
          "logs:GetLogEvents",
          "logs:FilterLogEvents"
        ],
        "Resource": "*"
      }     
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "image_lambda"  {
  role       = aws_iam_role.image_uploading_fxn.name
  policy_arn = data.aws_iam_policy.lambda_exec.arn
}

resource "aws_iam_role_policy_attachment" "check_lambda_dynamo" {
  role       = aws_iam_role.image_check_fxn.name
  policy_arn = data.aws_iam_policy.dynamo_exec.arn
}

resource "aws_iam_role_policy_attachment" "check_lambda_lambda"  {
  role       = aws_iam_role.image_check_fxn.name
  policy_arn = data.aws_iam_policy.lambda_exec.arn
}

# resource "aws_iam_role_policy_attachment" "image_lambda_again" {
#   role       = aws_iam_role.image_uploading_fxn.name
#   policy_arn = aws_iam_policy.cloud_permissions.arn
# }




resource "aws_dynamodb_table" "game_state" {
  name           = "game_state"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }
}
