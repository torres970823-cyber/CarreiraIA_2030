"""
Agente Diagnosticador de Risco e Simbiose de IA (AIEvaluatorAgent)
Conforme especificação de agentes_universais.md:
- Modela e calcula a vulnerabilidade à automação e potencial de aumento (Augmentation)
- Cruza o perfil do candidato com a matriz de impacto WEF/McKinsey até 2030
- Gera métricas para gráficos de radar de competências e auditoria de rotina
"""

from typing import Dict, Any, List


class AIEvaluatorAgent:
    def __init__(self):
        self.name = "AIEvaluatorAgent"
        self.role = "Especialista em Avaliação de Risco de Automação e Simbiose Humano-IA"

    def evaluate_profile(self, parsed_profile: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a avaliação quantitativa e qualitativa do profissional frente ao horizonte 2030.
        """
        base_risk = benchmark.get("automation_risk_score", 50)
        base_augmentation = benchmark.get("augmentation_potential_score", 75)

        # Ajuste dinâmico baseado no perfil individual do usuário
        risk_adjustment = 0

        # 1. Proporção de tarefas rotineiras vs. estratégicas
        routine_ratio = parsed_profile.get("routine_tasks_ratio", 50)
        if routine_ratio >= 70:
            risk_adjustment += 12
        elif routine_ratio >= 50:
            risk_adjustment += 6
        elif routine_ratio <= 30:
            risk_adjustment -= 10

        # 2. Senioridade e anos de experiência
        seniority = parsed_profile.get("seniority", "")
        if "Sênior" in seniority or "Liderança" in seniority:
            risk_adjustment -= 12
        elif "Júnior" in seniority or "Iniciante" in seniority:
            risk_adjustment += 8

        # 3. Literacia prévia em IA
        if parsed_profile.get("has_ai_experience", False):
            risk_adjustment -= 10
            augmentation_boost = 8
        else:
            risk_adjustment += 5
            augmentation_boost = 0

        # Cálculo final do Risco de Automação (limitado entre 10% e 98%)
        final_risk = max(10, min(98, base_risk + risk_adjustment))

        # Cálculo do Potencial de Aumento (limitado entre 30% e 99%)
        final_augmentation = max(30, min(99, base_augmentation + augmentation_boost))

        # Classificação de Risco
        if final_risk <= 35:
            risk_level = "Baixo"
            risk_badge_color = "green"
            risk_summary = "Perfil altamente protegido por tomada de decisão estratégica, empatia ou julgamento complexo."
        elif final_risk <= 60:
            risk_level = "Moderado"
            risk_badge_color = "orange"
            risk_summary = "Perfil com risco moderado. Metade das tarefas sofrerá transformação profunda por agentes de IA até 2028."
        elif final_risk <= 80:
            risk_level = "Alto"
            risk_badge_color = "red"
            risk_summary = "Perfil sob forte pressão de automação. Requer requalificação ativa (upskilling) em orquestração de IA e competências humanas."
        else:
            risk_level = "Crítico"
            risk_badge_color = "darkred"
            risk_summary = "Risco crítico de obsolescência das rotinas operacionais até 2028-2030. Necessidade de pivot de carreira ou transição para papel consultivo."

        # Estimativa de Radar de Competências (Perfil Atual vs. 2030 Ideal)
        ideal_radar = benchmark.get("skills_radar_ideal", {
            "pensamento_analitico": 8,
            "orquestracao_ia": 8,
            "criatividade_inovacao": 8,
            "lideranca_influencia": 8,
            "resiliencia_adaptabilidade": 8,
            "especializacao_estrategica": 8
        })

        # Estimação do perfil atual do usuário com base no currículo
        has_ai = parsed_profile.get("has_ai_experience", False)
        is_senior = "Sênior" in seniority or "Liderança" in seniority
        detected_soft = parsed_profile.get("detected_soft_skills", [])
        years = parsed_profile.get("years_experience", 3)

        # Radar granular: usa anos de experiência e proporção de rotina além da senioridade binária
        current_radar = {
            "pensamento_analitico": min(9, 4 + (years // 2) + (1 if is_senior else 0)),
            "orquestracao_ia": 8 if has_ai else (3 if routine_ratio > 60 else 4),
            "criatividade_inovacao": 7 if "criatividade" in str(detected_soft).lower() else (6 if is_senior else (5 if years >= 5 else 4)),
            "lideranca_influencia": min(9, 3 + (years // 2) + (3 if is_senior else 0)),
            "resiliencia_adaptabilidade": min(9, 5 + (1 if is_senior else 0) + (1 if has_ai else 0) + (1 if years >= 7 else 0)),
            "especializacao_estrategica": min(9, 3 + (years // 2) + (2 if is_senior else 0))
        }

        # Identificação de Gaps Críticos (diferença >= 3 pontos)
        radar_labels = {
            "pensamento_analitico": "Pensamento Analítico e Crítico",
            "orquestracao_ia": "Orquestração de IA & Dados",
            "criatividade_inovacao": "Criatividade e Inovação",
            "lideranca_influencia": "Liderança e Inteligência Interpessoal",
            "resiliencia_adaptabilidade": "Resiliência e Flexibilidade Cognitiva",
            "especializacao_estrategica": "Especialização Estratégica e Julgamento"
        }

        critical_gaps = []
        strong_pillars = []

        for key, ideal_val in ideal_radar.items():
            curr_val = current_radar.get(key, 5)
            gap = ideal_val - curr_val
            label = radar_labels.get(key, key)
            if gap >= 3:
                critical_gaps.append({
                    "skill": label,
                    "ideal": ideal_val,
                    "current": curr_val,
                    "gap": gap
                })
            elif curr_val >= 7:
                strong_pillars.append({
                    "skill": label,
                    "score": curr_val
                })

        # Divisão estimada do tempo de trabalho semanal atual e futuro
        task_audit = {
            "hours_threatened_by_ai": round(final_risk * 0.4, 1),      # % de horas semanais rotineiras
            "hours_augmented_by_ai": round(final_augmentation * 0.4, 1), # % de horas em simbiose
            "hours_human_strategic": round(100 - (final_risk * 0.4), 1)
        }

        return {
            "final_automation_risk": final_risk,
            "risk_level": risk_level,
            "risk_badge_color": risk_badge_color,
            "risk_summary": risk_summary,
            "final_augmentation_potential": final_augmentation,
            "productivity_multiplier": f"{round(1 + (final_augmentation / 60), 1)}x",
            "radar_ideal": ideal_radar,
            "radar_current": current_radar,
            "radar_labels": radar_labels,
            "critical_gaps": critical_gaps,
            "strong_pillars": strong_pillars,
            "task_audit": task_audit
        }
