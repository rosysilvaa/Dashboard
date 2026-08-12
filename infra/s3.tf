# Bucket onde os arquivos CSV/Excel de vendas são enviados (upload manual ou automatizado)
resource "aws_s3_bucket" "vendas_ingestao" {
  bucket = "${var.project_name}-ingestao-${var.environment}-${data.aws_caller_identity.current.account_id}"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "vendas_ingestao" {
  bucket = aws_s3_bucket.vendas_ingestao.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "vendas_ingestao" {
  bucket                  = aws_s3_bucket.vendas_ingestao.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Permite que o S3 invoque a Lambda de ingestão
resource "aws_s3_bucket_notification" "vendas_ingestao" {
  bucket = aws_s3_bucket.vendas_ingestao.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.ingest.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "uploads/"
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke]
}

data "aws_caller_identity" "current" {}
