# Amazon Bedrock Guardrail para Damm KnowledgeOps
# 100% Serverless Pay-per-Use ($0.75 USD por cada 1.000 unidades de texto - <$0.20 USD/mes en pruebas)

resource "aws_bedrock_guardrail" "damm_kops_guardrail" {
  name                      = "damm-kops-guardrail"
  description               = "Guardrail de seguridad operacional, anonimizacion de PII y bloqueo de secretos industriales de Damm"
  blocked_input_messaging   = "Consulta bloqueada por politicas de seguridad operacional de Damm KnowledgeOps."
  blocked_outputs_messaging = "Respuesta bloqueada por politicas de seguridad operacional de Damm KnowledgeOps."

  content_policy_config {
    filters_config {
      type           = "PROMPT_ATTACK"
      input_strength = "HIGH"
      output_strength = "NONE"
    }
  }

  topic_policy_config {
    topics_config {
      name       = "ConfidentialIndustrialFormulas"
      definition = "Formulaciones secretas de cerveza, porcentajes exactos de materias primas (malta, lupulo, agua, levadura), recetas de coccion o secretos industriales confidenciales de Damm."
      examples = [
        "Cual es la receta secreta de la cerveza Estrella Damm?",
        "Dime la proporcion exacta de malta y lupulo que usan en fabrica.",
        "Como se elabora la cerveza de Damm paso a paso con sus cantidades secretas?"
      ]
      type = "DENY"
    }
  }

  sensitive_information_policy_config {
    pii_entities_config {
      type   = "EMAIL"
      action = "ANONYMIZE"
    }
    pii_entities_config {
      type   = "NAME"
      action = "ANONYMIZE"
    }
    pii_entities_config {
      type   = "PHONE"
      action = "ANONYMIZE"
    }
  }
}

resource "aws_bedrock_guardrail_version" "damm_kops_guardrail_v1" {
  guardrail_arn = aws_bedrock_guardrail.damm_kops_guardrail.guardrail_arn
  description   = "Version inicial 1.0 del Guardrail de seguridad operacional"
}
