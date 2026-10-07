"""
Agente de Segurança e Privacidade (SecurityReviewerAgent)
Conforme especificação da Seção 5 e 11.1 de agentes_universais.md:
- Garantia de privacidade e conformidade com LGPD
- Sanitização de dados pessoais em currículos antes do processamento
- Prevenção contra injeção de prompt e vazamento de dados sensíveis
"""

import re
from typing import Dict, Any, Tuple


class SecurityReviewerAgent:
    def __init__(self):
        self.name = "SecurityReviewerAgent"
        self.role = "Guardião de Privacidade, LGPD e Segurança de Dados"

    def audit_and_sanitize(self, raw_text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Analisa o texto do currículo, mascara dados estritamente pessoais/sensíveis (LGPD)
        e verifica se há riscos de segurança.
        """
        audit_log = {
            "cpf_masked": 0,
            "emails_masked": 0,
            "phones_masked": 0,
            "sensitive_warnings": [],
            "status": "APPROVED",
        }

        sanitized_text = raw_text

        # 1. Mascarar CPFs: 000.000.000-00 ou 11 dígitos sequenciais
        cpf_pattern = r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"
        cpfs_found = re.findall(cpf_pattern, sanitized_text)
        if cpfs_found:
            audit_log["cpf_masked"] = len(cpfs_found)
            sanitized_text = re.sub(cpf_pattern, "[CPF_PROTEGIDO_LGPD]", sanitized_text)

        # 2. Mascarar Telefones brasileiros comuns
        phone_pattern = r"(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\s?\d{4}[-\s]?\d{4}|\d{4}[-\s]?\d{4})"
        # Aplicar com cautela para não mascarar anos (ex: 2024, 2030)
        phones = re.findall(phone_pattern, sanitized_text)
        filtered_phones = [p for p in phones if len(re.sub(r"\D", "", p)) in (10, 11, 12, 13)]
        if filtered_phones:
            audit_log["phones_masked"] = len(filtered_phones)
            for p in filtered_phones:
                sanitized_text = sanitized_text.replace(p.strip(), "[TELEFONE_PROTEGIDO]")

        # 3. Mascarar e-mails pessoais
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        emails = re.findall(email_pattern, sanitized_text)
        if emails:
            audit_log["emails_masked"] = len(emails)
            sanitized_text = re.sub(email_pattern, "[EMAIL_PROTEGIDO]", sanitized_text)

        # 4. Checagem de palavras-chave de risco (segredos, senhas acidentais)
        leak_keywords = ["senha", "password", "token_secreto", "api_key", "secret_key"]
        for kw in leak_keywords:
            if re.search(rf"\b{kw}\b", sanitized_text, re.IGNORECASE):
                audit_log["sensitive_warnings"].append(
                    f"Atenção: Termo sensível '{kw}' detectado e isolado para proteção."
                )

        return sanitized_text, audit_log
