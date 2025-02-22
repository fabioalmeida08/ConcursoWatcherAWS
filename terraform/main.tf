module "ssm" {
  source    = "./ssm"
  token_bot = var.token_bot
  my_chat_id = var.my_chat_id
  last_updated_date = var.last_updated_date
}

output "TokenBot_ARN" {
  value       = module.ssm.token_bot_arn
}

output "ChatID_ARN" {
  value       = module.ssm.chat_id_arn
}

output "LastUpdatedDate_ARN" {
  value       = module.ssm.last_updated_date_parameter_arn
}