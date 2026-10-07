"""
Agente Diagnosticador de Risco e Simbiose de IA (AIEvaluatorAgent)
Cálculos econométricos granulares, matriz de simbiose e radar de competências diferenciado por perfil e domínio.
"""

from typing import Dict, Any, List


class AIEvaluatorAgent:
    def __init__(self):
        self.name = "AIEvaluatorAgent"
        self.role = "Especialista em Avaliação de Risco de Automação e Simbiose Humano-IA"

    def evaluate_profile(self, parsed_profile: Dict[str, Any], benchmark: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa a avaliação quantitativa e qualitativa do profissional frente ao horizonte 2030.
        Gera resultados altamente diferenciados baseados nas características individuais e no domínio.
        """
        base_risk = benchmark.get("automation_risk_score", 50)
        base_augmentation = benchmark.get("augmentation_potential_score", 75)

        risk_adjustment = 0
        augmentation_boost = 0

        # 1. Proporção de tarefas rotineiras vs. estratégicas
        routine_ratio = parsed_profile.get("routine_tasks_ratio", 50)
        if routine_ratio >= 75:
            risk_adjustment += 8
            augmentation_boost -= 6
        elif routine_ratio >= 55:
            risk_adjustment += 4
        elif routine_ratio <= 25:
            risk_adjustment -= 10
            augmentation_boost += 6
        elif routine_ratio <= 40:
            risk_adjustment -= 5

        # 2. Senioridade e anos de experiência
        seniority = parsed_profile.get("seniority", "Pleno")
        years_exp = parsed_profile.get("years_experience", 3)

        if "Sênior" in seniority or "Liderança" in seniority or years_exp >= 8:
            risk_adjustment -= 8
            augmentation_boost += 6
        elif "Júnior" in seniority or "Iniciante" in seniority or years_exp <= 2:
            risk_adjustment += 6
            augmentation_boost -= 4

        # 3. Literacia prévia em IA
        if parsed_profile.get("has_ai_experience", False):
            risk_adjustment -= 6
            augmentation_boost += 8
        else:
            risk_adjustment += 3

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

        # Estimação do perfil atual do usuário de forma calibrada por domínio
        domain = parsed_profile.get("domain", "")
        has_ai = parsed_profile.get("has_ai_experience", False)
        is_senior = "Sênior" in seniority or "Liderança" in seniority
        detected_soft = parsed_profile.get("detected_soft_skills", [])
        soft_str = " ".join(detected_soft).lower()

        # Afinidade por domínio para o Radar
        if "Saúde" in domain:
            analitico_base = 7
            ia_base = 6 if has_ai else 4
            criat_base = 6
            lider_base = 8
            resil_base = 8
            estrat_base = 8
        elif "Tecnologia" in domain:
            analitico_base = 8
            ia_base = 9 if has_ai else 6
            criat_base = 7
            lider_base = 5 + (3 if is_senior else 0)
            resil_base = 8
            estrat_base = 6 + (3 if is_senior else 0)
        elif "Jurídico" in domain:
            analitico_base = 9
            ia_base = 6 if has_ai else 4
            criat_base = 6
            lider_base = 7
            resil_base = 7
            estrat_base = 9
        elif "Design" in domain:
            analitico_base = 6
            ia_base = 8 if has_ai else 6
            criat_base = 9
            lider_base = 6
            resil_base = 8
            estrat_base = 6
        elif "Economia" in domain or "Finanças" in domain:
            analitico_base = 8
            ia_base = 7 if has_ai else 4
            criat_base = 5
            lider_base = 6
            resil_base = 7
            estrat_base = 7
        elif "Administração" in domain:
            analitico_base = 5
            ia_base = 5 if has_ai else 3
            criat_base = 4
            lider_base = 5
            resil_base = 6
            estrat_base = 4
        elif "Educação" in domain:
            analitico_base = 7
            ia_base = 6 if has_ai else 4
            criat_base = 8
            lider_base = 9
            resil_base = 8
            estrat_base = 7
        elif "Vendas" in domain:
            analitico_base = 6
            ia_base = 6 if has_ai else 4
            criat_base = 7
            lider_base = 9
            resil_base = 8
            estrat_base = 7
        else:
            analitico_base = 6
            ia_base = 6 if has_ai else 4
            criat_base = 6
            lider_base = 6
            resil_base = 6
            estrat_base = 6

        # Modulação pelos anos de experiência
        exp_mod = min(2, years_exp // 4)

        current_radar = {
            "pensamento_analitico": max(2, min(10, analitico_base + exp_mod + (1 if "analítico" in soft_str else 0))),
            "orquestracao_ia": max(2, min(10, ia_base + (1 if has_ai else 0))),
            "criatividade_inovacao": max(2, min(10, criat_base + exp_mod + (1 if "criatividade" in soft_str else 0))),
            "lideranca_influencia": max(2, min(10, lider_base + exp_mod + (1 if is_senior else 0))),
            "resiliencia_adaptabilidade": max(2, min(10, resil_base + (1 if is_senior else 0))),
            "especializacao_estrategica": max(2, min(10, estrat_base + exp_mod + (1 if is_senior else 0)))
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
