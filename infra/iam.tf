data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_ingest_role" {
  name               = "${var.project_name}-lambda-ingest-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role" "lambda_api_role" {
  name               = "${var.project_name}-lambda-api-role-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

# --- Permissões da Lambda de ingestão: ler do S3 + escrever no DynamoDB ---
data "aws_iam_policy_document" "lambda_ingest_policy" {
  statement {
    sid       = "LeituraS3"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.vendas_ingestao.arn}/*"]
  }
  statement {
    sid       = "EscritaDynamo"
    actions   = ["dynamodb:PutItem", "dynamodb:BatchWriteItem"]
    resources = [aws_dynamodb_table.vendas.arn]
  }
  statement {
    sid       = "Logs"
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_role_policy" "lambda_ingest_policy" {
  name   = "${var.project_name}-ingest-policy-${var.environment}"
  role   = aws_iam_role.lambda_ingest_role.id
  policy = data.aws_iam_policy_document.lambda_ingest_policy.json
}

# --- Permissões da Lambda de API: ler do DynamoDB ---
data "aws_iam_policy_document" "lambda_api_policy" {
  statement {
    sid       = "LeituraDynamo"
    actions   = ["dynamodb:Scan", "dynamodb:Query"]
    resources = [aws_dynamodb_table.vendas.arn, "${aws_dynamodb_table.vendas.arn}/index/*"]
  }
  statement {
    sid       = "Logs"
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

resource "aws_iam_role_policy" "lambda_api_policy" {
  name   = "${var.project_name}-api-policy-${var.environment}"
  role   = aws_iam_role.lambda_api_role.id
  policy = data.aws_iam_policy_document.lambda_api_policy.json
}
