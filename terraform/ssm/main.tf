resource "aws_ssm_parameter" "token_bot" {
  name        = "/Telegram/TokenBot"
  description = "token bot"
  type        = "SecureString"
  value       = var.token_bot
  tier        = "Standard"

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

resource "aws_ssm_parameter" "chat_id" {
  name        = "/Telegram/MyChatID"
  description = "my chat id"
  type        = "SecureString"
  value       = var.my_chat_id
  tier        = "Standard"

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

resource "aws_ssm_parameter" "last_updated_date" {
  name        = "/Concurso/LastUpdatedDate"
  description = "last date"
  type        = "SecureString"
  value       = var.last_updated_date
  tier        = "Standard"

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}