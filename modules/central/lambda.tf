data "archive_file" "central_flow_logs_athena_partition" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/vpc-central-flow-logs-athena-create-partition"
  output_path = "${path.module}/lambda/vpc-central-flow-logs-athena-create-partition.zip"
}

resource "aws_lambda_function" "central_flow_logs_athena_partition" {
  filename         = data.archive_file.central_flow_logs_athena_partition.output_path
  function_name    = "vpc-central-flow-logs-athena-create-partition"
  handler          = "vpc-central-flow-logs-athena-create-partition.lambda_handler"
  source_code_hash = data.archive_file.central_flow_logs_athena_partition.output_base64sha256
  role             = aws_iam_role.central_flow_logs_athena_partition.arn
  runtime          = "python3.9"
  timeout          = 900
  memory_size      = 512

  environment {
    variables = {
      TABLE_NAME         = aws_glue_catalog_table.central_flow_logs.name
      S3_OUTPUT          = aws_s3_bucket.central_flow_logs.bucket
      S3_ACCOUNT_PREFIX  = ""
      S3_BUCKET_FLOW_LOG = aws_s3_bucket.central_flow_logs.bucket
      DATABASE           = aws_athena_database.central_flow_logs.name
      FREQUENCY          = "Daily"
    }
  }
}

resource "aws_cloudwatch_log_group" "central_flow_logs_athena_partition" {
  name              = "/aws/lambda/${aws_lambda_function.central_flow_logs_athena_partition.function_name}"
  retention_in_days = 14
}

data "aws_iam_policy_document" "central_flow_logs_athena_partition" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]
  }
  statement {
    actions = [
      "s3:ListObjects",
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:GetBucketLocation",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
  statement {
    actions = [
      "athena:StartQueryExecution",
      "athena:GetQueryExecution",
      "athena:GetQueryResults",
      "athena:CreateNamedQuery",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
  statement {
    actions = [
      "glue:GetDatabase",
      "glue:GetTable",
      "glue:CreateTable",
      "glue:UpdateTable",
      "glue:BatchCreatePartition",
      "glue:CreatePartition",
      "glue:UpdatePartition",
      "glue:GetPartition",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_policy" "central_flow_logs_athena_partition" {
  name        = "vpc-central-flow-logs-athena-create-partition"
  path        = "/"
  description = "Policy to be used by the Central flow logs athena partition"
  policy      = data.aws_iam_policy_document.central_flow_logs_athena_partition.json
}


resource "aws_iam_role" "central_flow_logs_athena_partition" {
  name               = "vpc-central-flow-logs-athena-create-partition"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "central_flow_logs_athena_partition" {
  role       = aws_iam_role.central_flow_logs_athena_partition.name
  policy_arn = aws_iam_policy.central_flow_logs_athena_partition.arn
}

resource "aws_cloudwatch_event_rule" "central_flow_logs_athena_partition" {
  name                = "vpc-central-flow-logs-athena-create-partition"
  description         = "Create Athena partition on a daily basis"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "central_flow_logs_athena_partition" {
  rule      = aws_cloudwatch_event_rule.central_flow_logs_athena_partition.name
  target_id = "vpc-central-flow-logs-athena-create-partition"
  arn       = aws_lambda_function.central_flow_logs_athena_partition.arn
}

resource "aws_lambda_permission" "central_flow_logs_athena_partition" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.central_flow_logs_athena_partition.function_name
  principal     = "events.amazonaws.com"
}

data "archive_file" "central_flow_logs_athena_view" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/vpc-central-flow-logs-athena-create-views"
  output_path = "${path.module}/lambda/vpc-central-flow-logs-athena-create-views.zip"
}

resource "aws_lambda_function" "central_flow_logs_athena_view" {
  filename         = data.archive_file.central_flow_logs_athena_view.output_path
  function_name    = "vpc-central-flow-logs-athena-create-views"
  handler          = "vpc-central-flow-logs-athena-create-views.lambda_handler"
  source_code_hash = data.archive_file.central_flow_logs_athena_view.output_base64sha256
  role             = aws_iam_role.central_flow_logs_athena_view.arn
  runtime          = "python3.9"
  timeout          = 900
  memory_size      = 512

  environment {
    variables = {
      TABLE_NAME = aws_glue_catalog_table.central_flow_logs.name
      S3_OUTPUT  = aws_s3_bucket.central_flow_logs.bucket
      DATABASE   = aws_athena_database.central_flow_logs.name
    }
  }
}

resource "aws_cloudwatch_log_group" "central_flow_logs_athena_view" {
  name              = "/aws/lambda/${aws_lambda_function.central_flow_logs_athena_view.function_name}"
  retention_in_days = 14
}

data "aws_iam_policy_document" "central_flow_logs_athena_view" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]
  }
  statement {
    actions = [
      "athena:StartQueryExecution",
      "athena:GetQueryExecution",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
  statement {
    actions = [
      "glue:GetTable",
      "glue:CreateTable",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
  statement {
    actions = [
      "s3:PutObject",
      "s3:GetBucketLocation",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_policy" "central_flow_logs_athena_view" {
  name        = "vpc-central-flow-logs-athena-create-views"
  path        = "/"
  description = "Policy to be used by the Central flow logs athena views"
  policy      = data.aws_iam_policy_document.central_flow_logs_athena_view.json
}


resource "aws_iam_role" "central_flow_logs_athena_view" {
  name               = "vpc-central-flow-logs-athena-create-views"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "central_flow_logs_athena_view" {
  role       = aws_iam_role.central_flow_logs_athena_view.name
  policy_arn = aws_iam_policy.central_flow_logs_athena_view.arn
}

resource "aws_lambda_invocation" "central_flow_logs_athena_view" {
  function_name = aws_lambda_function.central_flow_logs_athena_view.function_name
  input         = ""
}

data "archive_file" "central_flow_logs_quicksight" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/vpc-central-flow-logs-quicksight-create-dashboard"
  output_path = "${path.module}/lambda/vpc-central-flow-logs-quicksight-create-dashboard.zip"
}

resource "aws_lambda_function" "central_flow_logs_quicksight" {
  filename         = data.archive_file.central_flow_logs_quicksight.output_path
  function_name    = "vpc-central-flow-logs-quicksight-create-dashboard"
  handler          = "vpc-central-flow-logs-quicksight-create-dashboard.lambda_handler"
  source_code_hash = data.archive_file.central_flow_logs_quicksight.output_base64sha256
  role             = aws_iam_role.central_flow_logs_quicksight.arn
  runtime          = "python3.9"
  timeout          = 900
  memory_size      = 512

  environment {
    variables = {
      ACCOUNT_ID = data.aws_caller_identity.current.account_id
      ATHENA_DATASOURCE_ARN  = aws_quicksight_data_source.central_flow_logs.arn
      DATABASE   = aws_athena_database.central_flow_logs.name
      QUICKSIGHT_USER_ARN = var.quicksight_user_arn
    }
  }
}

resource "aws_cloudwatch_log_group" "central_flow_logs_quicksight" {
  name              = "/aws/lambda/${aws_lambda_function.central_flow_logs_quicksight.function_name}"
  retention_in_days = 14
}

data "aws_iam_policy_document" "central_flow_logs_quicksight" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    effect    = "Allow"
    resources = ["arn:aws:logs:*:*:*"]
  }
  statement {
    actions = [
      "quicksight:CreateDataSet",
      "quicksight:CreateDashboard",
    ]
    effect    = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_policy" "central_flow_logs_quicksight" {
  name        = "vpc-central-flow-logs-quicksight-create-dashboard"
  path        = "/"
  description = "Policy to be used by the Central flow logs quicksignt"
  policy      = data.aws_iam_policy_document.central_flow_logs_quicksight.json
}


resource "aws_iam_role" "central_flow_logs_quicksight" {
  name               = "vpc-central-flow-logs-quicksight-create-dashboard"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "central_flow_logs_quicksight" {
  role       = aws_iam_role.central_flow_logs_quicksight.name
  policy_arn = aws_iam_policy.central_flow_logs_quicksight.arn
}

resource "aws_lambda_invocation" "central_flow_logs_quicksight" {
  function_name = aws_lambda_function.central_flow_logs_quicksight.function_name
  input         = ""

  depends_on = [
    aws_quicksight_data_source.central_flow_logs
  ]
}