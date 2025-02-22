output "chat_id_arn" {
  value = aws_ssm_parameter.chat_id.arn
}

output "last_updated_date_parameter_arn" {
  value = aws_ssm_parameter.last_updated_date.arn
}

output "token_bot_arn" {
  value       = aws_ssm_parameter.token_bot.arn
}