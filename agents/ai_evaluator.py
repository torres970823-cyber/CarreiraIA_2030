"""
Agente Diagnosticador de Risco e Simbiose de IA (AIEvaluatorAgent)
Cálculos econométricos granulares, matriz de simbiose e radar de competências diferenciado por perfil.
"""

from typing import Dict, Any, List


class AIEvaluatorAgent:
    def __init__(self):
        self.name = "AIEvaluatorAgent"
        self.role = "Especialista em Avaliação de Risco de Automação e Simbiose Humano-IA"

    def evaluate_profile(self, parsed_profile: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a avaliação quantitativa e qualitativa do profissional frente ao horizonte 2030.
        Gera resultados altamente diferenciados baseados nas características individuais do perfil.
        """
        base_risk = benchmark.get("automation_risk_score", 50)
        base_augmentation = benchmark.get("augmentation_potential_score", 75)

        # Ajuste dinâmico baseado no perfil individual do usuário
        risk_adjustment = 0
        augmentation_boost = 0

        # 1. Proporção de tarefas rotineiras vs. estratégicas
        routine_ratio = parsed_profile.get("routine_tasks_ratio", 50)
        if routine_ratio >= 75:
            risk_adjustment += 10
            augmentation_boost -= 6
        elif routine_ratio >= 55:
            risk_adjustment += 5
        elif routine_ratio <= 25:
            risk_adjustment -= 12
            augmentation_boost += 6
        elif routine_ratio <= 40:
            risk_adjustment -= 6

        # 2. Senioridade e anos de experiência
        seniority = parsed_profile.get("seniority", "Pleno")
        years_exp = parsed_profile.get("years_experience", 3)

        if "Sênior" in seniority or "Liderança" in seniority or years_exp >= 8:
            risk_adjustment -= 10
            augmentation_boost += 8
        elif "Júnior" in seniority or "Iniciante" in seniority or years_exp <= 2:
            risk_adjustment += 8
            augmentation_boost -= 4

        # 3. Literacia prévia em IA
        if parsed_profile.get("has_ai_experience", False):
            risk_adjustment -= 8
            augmentation_boost += 10
        else:
            risk_adjustment += 4

        # Cálculo final do Risco de Automação (limitado entre 10% e 98%)
        final_risk = max(10, min(98, base_risk + risk_adjustment))

        # Cálculo do Potencial de Aumento (limitado entre 30% e 99%)
        final_augmentation = max(30, min(99, base_augmentation + augmentation_boost))

        # Classificação de Risco
        if final_risk <= 30:
            risk_level = "Baixo"
            risk_badge_color = "green"
            risk_summary = "Perfil altamente protegido por tomada de decisão estratégica, liderança ou julgamento ético complexo."
        elif final_risk <= 55:
            risk_level = "Moderado"
            risk_badge_color = "orange"
            risk_summary = "Perfil com risco moderado. Metade das tarefas sofrerá transformação profunda por agentes de IA até 2028."
        elif final_risk <= 75:
            risk_level = "Alto"
            risk_badge_color = "red"
            risk_summary = "Perfil sob forte pressão de automação. Requer requalificação ativa (upskilling) em orquestração de IA e competências humanas."
        else:
            risk_level = "Crítico"
            risk_badge_color = "darkred"
            risk_summary = "Risco crítico de obsolescência das rotinas operacionais até 2028-2030. Necessidade de pivot de carreira ou transição para papel estratégico."

        # Radar Ideal do Benchmark
        ideal_radar = benchmark.get("skills_radar_ideal", {
            "pensamento_analitico": 8,
            "orquestracao_ia": 8,
            "criatividade_inovacao": 8,
            "lideranca_influencia": 8,
            "resiliencia_adaptabilidade": 8,
            "especializacao_estrategica": 8
        })

        # Estimação do perfil atual do usuário de forma granular
        has_ai = parsed_profile.get("has_ai_experience", False)
        is_senior = "Sênior" in seniority or "Liderança" in seniority
        detected_soft = parsed_profile.get("detected_soft_skills", [])
        soft_str = " ".join(detected_soft).lower()

        # Cálculo granular por habilidade
        val_analitico = min(9, 4 + (years_exp // 3) + (2 if is_senior else 0) + (1 if "analítico" in soft_str or "crítico" in soft_str else 0))
        val_ia = 8 if has_ai else (3 if routine_ratio >= 65 else 5)
        val_criatividade = 8 if "criatividade" in soft_str else (7 if is_senior else (6 if years_exp >= 4 else 4))
        val_lideranca = min(10, 3 + (years_exp // 2) + (3 if is_senior else 0) + (1 if "liderança" in soft_str else 0))
        val_resiliencia = min(9, 5 + (2 if is_senior else 0) + (1 if has_ai else 0) + (1 if "resiliência" in soft_str or "adaptabilidade" in soft_str else 0))
        val_estrategica = min(10, 3 + (years_exp // 2) + (3 if is_senior else 0) + (1 if "estratégia" in soft_str or "decisão" in soft_str else 0))

        current_radar = {
            "pensamento_analitico": max(2, min(10, val_analitico)),
            "orquestracao_ia": max(2, min(10, val_ia)),
            "criatividade_inovacao": max(2, min(10, val_criatividade)),
            "lideranca_influencia": max(2, min(10, val_lideranca)),
            "resiliencia_adaptabilidade": max(2, min(10, val_resiliencia)),
            "especializacao_estrategica": max(2, min(10, val_estrategica))
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

        # Divisão estimada do tempo de trabalho semanal
        task_audit = {
            "hours_threatened_by_ai": round(final_risk * 0.4, 1),
            "hours_augmented_by_ai": round(final_augmentation * 0.4, 1),
            "hours_human_strategic": round(100 - (final_risk * 0.4), 1)
        }

        return {
            "final_automation_risk": final_risk,
            "risk_level": risk_level,
            "risk_badge_color": risk_badge_color,
            "risk_summary": risk_summary,
            "final_augmentation_potential": final_augmentation,
            "productivity_multiplier": f"{round(1 + (final_augmentation / 55), 1)}x",
            "radar_ideal": ideal_radar,
            "radar_current": current_radar,
            "radar_labels": radar_labels,
            "critical_gaps": critical_gaps,
            "strong_pillars": strong_pillars,
            "task_audit": task_audit
        }
