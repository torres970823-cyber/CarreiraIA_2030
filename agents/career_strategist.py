"""
Agente Estrategista de Carreira (CareerStrategistAgent)
Gera planos estratégicos 2026-2030 com isolamento total de domínio.
"""

from typing import Dict, Any, List


class CareerStrategistAgent:
    def __init__(self):
        self.name = "CareerStrategistAgent"
        self.role = "Especialista em Estratégia de Carreira e Upskilling 2030"

    def generate_strategy(
        self,
        parsed_profile: Dict[str, Any],
        benchmark: Dict[str, Any],
        evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera recomendações táticas alinhadas à profissão do candidato."""
        role = parsed_profile.get("role", "Profissional")
        domain = parsed_profile.get("domain", "Sua Área")
        seniority = parsed_profile.get("seniority", "Pleno")
        tools_2030 = benchmark.get("recommended_tools_2030", ["Copilotos de IA Especializados", "Ferramentas Analíticas da Área", "Sistemas de Decisão"])

        # Roadmap 2026-2030 com Zero Contaminação
        roadmap = [
            {
                "period": "2026 (Fundação Imediata)",
                "theme": f"Automação de Rotinas & Adoção de Copilotos em {domain}",
                "goal": "Eliminar tarefas manuais e burocráticas no dia a dia.",
                "action": f"Adotar ferramentas de IA generativa para redação, síntese de dados e triagem de documentos da rotina de {role}.",
                "key_tools": [tools_2030[0] if len(tools_2030) > 0 else "Copiloto Especializado", "Assistentes de IA Aplicados à Área"],
                "focus": "Adoção de Copiloto"
            },
            {
                "period": "2027 - 2028 (Médio Prazo)",
                "theme": f"Especialização Analítica & Supervisão Crítica em {domain}",
                "goal": f"Posicionar-se como o profissional que valida e audita soluções assistidas por IA em {role}.",
                "action": f"Desenvolver raciocínio analítico para checar consistência de dados, mitigar riscos éticos/regulatórios e integrar ferramentas especializadas de {domain}.",
                "key_tools": [tools_2030[1] if len(tools_2030) > 1 else "Sistemas Analíticos da Área", "Frameworks de Qualidade & Ética"],
                "focus": "Supervisão e Qualidade"
            },
            {
                "period": "2029 - 2030 (Longo Prazo)",
                "theme": f"Liderança Estratégica & Diferencial Humano em {domain}",
                "goal": "Consolidar autoridade profissional insubstituível em julgamento, ética e negociação.",
                "action": f"Liderar a estratégia da área de {domain}, focando em decisões sob alta incerteza, empatia e construção de confiança com stakeholders.",
                "key_tools": [tools_2030[2] if len(tools_2030) > 2 else "Plataformas de Tomada de Decisão", "Governança & Estratégia"],
                "focus": "Liderança e Visão de Futuro"
            }
        ]

        return {
            "roadmap": roadmap,
            "career_pivots": benchmark.get("transition_pivots", []),
            "recommended_certifications": benchmark.get("recommended_certifications", []),
            "declining_skills": benchmark.get("declining_skills", []),
            "emerging_skills": benchmark.get("emerging_skills_2030", []),
            "critical_advice": (
                f"No setor de {domain}, a IA não vai substituir o {role}; "
                f"porém, o {role} que dominar e supervisionar a IA com pensamento crítico "
                f"substituirá aquele que permanecer apenas na execução manual."
            )
        }

    def generate_markdown_dossier(
        self,
        parsed_profile: Dict[str, Any],
        benchmark: Dict[str, Any],
        evaluation: Dict[str, Any],
        strategy: Dict[str, Any]
    ) -> str:
        """Gera um relatório completo em formato Markdown para download e leitura executiva."""
        md = f"""# Dossiê de Carreira e Impacto da IA até 2030
*Gerado pelo Sistema Multiagente CarreiraIA 2030 (Base WEF & McKinsey)*

---

## 1. Perfil Analisado
- **Área / Domínio:** {parsed_profile.get('domain')}
- **Cargo Atual / Alvo:** {parsed_profile.get('role')}
- **Senioridade Diagnosticada:** {parsed_profile.get('seniority')}
- **Tempo Estimado de Experiência:** {parsed_profile.get('years_experience')} anos
- **Proporção de Tarefas Rotineiras:** {parsed_profile.get('routine_tasks_ratio')}%
- **Proporção de Tarefas Estratégicas:** {parsed_profile.get('strategic_tasks_ratio')}%

---

## 2. Diagnóstico de Risco e Potencial de Aumento (WEF 2030)
- **Índice de Risco de Automação:** {evaluation.get('final_automation_risk')}% ({evaluation.get('risk_level')})
- **Potencial de Aumento de Produtividade com IA:** {evaluation.get('final_augmentation_potential')}% (Multiplicador {evaluation.get('productivity_multiplier')})
- **Resumo Diagnóstico:** {evaluation.get('risk_summary')}

---

## 3. Auditoria de Tarefas da Rotina em {parsed_profile.get('domain')}
### ⚠️ Tarefas Ameaçadas de Automação até 2028:
"""
        for t in benchmark.get("declining_tasks", []):
            md += f"- {t}\n"

        md += f"\n### 🚀 Tarefas Híbridas (Onde a IA será seu Copiloto em {parsed_profile.get('role')}):\n"
        for t in benchmark.get("augmented_tasks", []):
            md += f"- {t}\n"

        md += "\n### 🛡️ Fortalezas Humanas Insubstituíveis:\n"
        for t in benchmark.get("human_core_tasks", []):
            md += f"- {t}\n"

        md += f"""
---

## 4. O Que Desaprender vs. O Que Aprender até 2030
### 📉 Habilidades em Declínio:
"""
        for s in strategy.get("declining_skills", []):
            md += f"- {s}\n"

        md += "\n### 📈 Habilidades Críticas Emergentes até 2030:\n"
        for s in strategy.get("emerging_skills", []):
            md += f"- {s}\n"

        md += f"""
---

## 5. Roadmap de Requalificação 2026 - 2030
"""
        for item in strategy.get("roadmap", []):
            md += f"""### {item.get('period')}: {item.get('theme')}
- **Meta:** {item.get('goal')}
- **Plano de Ação:** {item.get('action')}
- **Ferramentas Chave:** {', '.join(item.get('key_tools', []))}

"""

        md += f"""---

## 6. Transições de Carreira Recomendadas (Career Pivots)
"""
        for p in strategy.get("career_pivots", []):
            md += f"- **{p}**\n"

        md += f"""
---

## 7. Certificações Recomendadas
"""
        for c in strategy.get("recommended_certifications", []):
            md += f"- {c}\n"

        md += f"""
---
> *{strategy.get('critical_advice')}*
"""
        return md