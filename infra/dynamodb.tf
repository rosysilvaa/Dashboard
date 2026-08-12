# Tabela onde cada item representa uma venda individual
resource "aws_dynamodb_table" "vendas" {
  name         = "${var.project_name}-vendas-${var.environment}"
  billing_mode = "PAY_PER_REQUEST" # sob demanda: sem necessidade de provisionar capacidade
  hash_key     = "id_venda"

  attribute {
    name = "id_venda"
    type = "S"
  }

  # Índice global secundário para consultas futuras por cidade
  # (ex: filtrar vendas de uma cidade específica sem fazer scan completo)
  global_secondary_index {
    name            = "cidade-index"
    hash_key        = "cidade"
    projection_type = "ALL"
  }

  attribute {
    name = "cidade"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
