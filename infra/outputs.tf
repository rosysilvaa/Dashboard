output "bucket_ingestao" {
  description = "Nome do bucket S3 para upload dos arquivos de vendas (envie para dentro da pasta uploads/)"
  value       = aws_s3_bucket.vendas_ingestao.bucket
}

output "dynamodb_table" {
  description = "Nome da tabela DynamoDB com os registros de vendas"
  value       = aws_dynamodb_table.vendas.name
}

output "api_endpoint" {
  description = "URL do endpoint da API usada pelo dashboard (defina em API_URL no dashboard/index.html)"
  value       = "${aws_apigatewayv2_stage.default.invoke_url}/dashboard"
}
