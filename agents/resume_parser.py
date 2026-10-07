"""
Agente Analisador de Currículo e Competências (ResumeParserAgent)
Classificação Multidomínio Dinâmica, Detecção Semântica e Estimativa de Rotina por Perfil.
"""

import io
import re
from typing import Dict, Any, List


class ResumeParserAgent:
    def __init__(self):
        self.name = "ResumeParserAgent"
        self.role = "Especialista em Triagem, Competências e Auditoria Multidomínio"

        # Ontologia Ampla de Domínios com Estimativas de Rotina Intrínsecas da Profissão
        self.domain_clusters = {
            "Saúde, Medicina & Biociências": {
                "keywords": [
                    "médico", "médica", "medicina", "crm", "clínica", "hospital", "diagnóstico",
                    "cirurgi", "paciente", "prontuário", "anamnese", "telemedicina", "genômica",
                    "farmac", "farmacêutic", "enferm", "enfermeir", "nutri", "nutricionist",
                    "fisioterap", "psicol", "psicólog", "terapeut", "terapia", "saúde",
                    "odontol", "dentist", "veterinár", "biomedicin", "fonoaudiol", "biólog"
                ],
                "default_role": "Especialista em Saúde / Cuidados Clínicos",
                "default_routine_ratio": 20
            },
            "Jurídico, Contratos & Compliance": {
                "keywords": [
                    "advogad", "direito", "oab", "jurídic", "contrat", "contencioso", "compliance",
                    "lgpd", "processual", "parecer", "tributár", "societár", "jurisprudência",
                    "petição", "magistratur", "promotor", "defensor", "cartóri", "legal", "compliance"
                ],
                "default_role": "Advogado(a) / Especialista Jurídico",
                "default_routine_ratio": 35
            },
            "Tecnologia, Dados & Inteligência Artificial": {
                "keywords": [
                    "software", "desenvolvedor", "programador", "dev", "fullstack", "backend",
                    "frontend", "python", "react", "node", "javascript", "typescript", "sql",
                    "aws", "azure", "docker", "kubernetes", "machine learning", "data science",
                    "ciência de dados", "engenheiro de dados", "analista de dados", "devops", "qa",
                    "arquiteto de software", "tech lead", "cto", "cloud", "ciberseguran", "segurança da informação"
                ],
                "default_role": "Engenheiro(a) de Software / Especialista em Dados & IA",
                "default_routine_ratio": 30
            },
            "Economia, Finanças & Investimentos": {
                "keywords": [
                    "economist", "economia", "macroeconomia", "econometria", "cfa", "anbima",
                    "fp&a", "valuation", "investiment", "tesouraria", "cbdc", "tokenização",
                    "risco financeiro", "mercado de capitais", "planejamento financeiro", "controladoria",
                    "contábil", "contabilidade", "contador", "contadora", "auditoria", "fiscal",
                    "tributário", "finanças", "financeir", "banco", "bancári", "crédito"
                ],
                "default_role": "Analista Financeiro / Economista",
                "default_routine_ratio": 50
            },
            "Design, Mídia & Comunicação": {
                "keywords": [
                    "designer", "design", "figma", "photoshop", "illustrator", "ui", "ux", "ui/ux",
                    "direção de arte", "copywriting", "copywriter", "redator", "storytelling",
                    "branding", "mídia", "jornalism", "jornalist", "comunicação", "publicidad",
                    "publicitár", "marketing digital", "vídeo", "audiovisual", "social media", "ilustrad", "gráfico"
                ],
                "default_role": "Designer / Especialista em Criação",
                "default_routine_ratio": 30
            },
            "Educação, Formação & Pedagogia": {
                "keywords": [
                    "professor", "professora", "educador", "docent", "pedagog", "pedagogia",
                    "ensino", "escola", "aula", "treinamento", "instrutor", "didática", "ead", "tutor", "mentoria"
                ],
                "default_role": "Educador(a) / Especialista em Aprendizagem",
                "default_routine_ratio": 25
            },
            "Vendas, Marketing & Expansão de Negócios": {
                "keywords": [
                    "venda", "vendedor", "comercial", "sdr", "bdr", "account executive", "crm",
                    "growth", "tráfego pago", "negociação", "parcerias", "varejo", "prospecção",
                    "inside sales", "representante comercial", "key account", "marketing"
                ],
                "default_role": "Especialista Comercial & Negociação",
                "default_routine_ratio": 35
            },
            "Gestão, Liderança & Estratégia": {
                "keywords": [
                    "gerente", "gerência", "gestor", "gestora", "scrum master", "product owner",
                    "product manager", "coordenador", "diretor", "operações", "bizops", "líder",
                    "planejamento estratégico", "head", "supervis"
                ],
                "default_role": "Gerente Estratégico / Product Manager",
                "default_routine_ratio": 20
            },
            "Engenharia, Construção & Manufatura": {
                "keywords": [
                    "engenheir", "engenharia", "civil", "mecânic", "elétric", "químic", "crea",
                    "autocad", "revit", "bim", "obra", "instalações", "produção industrial",
                    "manufatura", "estrutural", "automação industrial", "arquiteto", "construção"
                ],
                "default_role": "Engenheiro(a) de Projetos e Operações",
                "default_routine_ratio": 30
            },
            "Administração, Suporte & Atendimento Operacional": {
                "keywords": [
                    "assistente", "auxiliar", "atendente", "sac", "telemarketing", "call center",
                    "recepcionista", "digitador", "secretári", "suporte", "backoffice", "cadastro",
                    "escritório", "faturamento", "contas a pagar", "arquivo", "rotinas administrativas"
                ],
                "default_role": "Assistente Administrativo / Operações de Suporte",
                "default_routine_ratio": 80
            }
        }

        self.soft_skills_catalog = [
            "pensamento analítico", "pensamento crítico", "liderança", "comunicação",
            "inteligência emocional", "empatia", "negociação", "resolução de problemas",
            "resiliência", "adaptabilidade", "flexibilidade", "trabalho em equipe",
            "gestão de tempo", "criatividade", "ética", "aprendizado contínuo", "visão sistêmica",
            "tomada de decisão", "mentoria", "gestão de projetos", "visão de negócio"
        ]

        self.routine_task_keywords = [
            "digitação", "planilha", "planilhas", "alimentação de dados", "arquivo", "relatórios manuais",
            "atendimento telefônico", "agendamento", "cadastro", "triagem", "notas fiscais",
            "manutenção básica", "repetitivo", "rotina", "preenchimento", "copiar e colar", "lançamento",
            "conferência manual", "emissão de notas", "consulta padrão", "resposta de chamados", "atendimento padrão"
        ]

        self.strategic_task_keywords = [
            "arquitetura", "liderança", "estratégia", "negociação", "tomada de decisão",
            "diagnóstico", "auditoria", "gestão de equipe", "inovação", "mentoria",
            "planejamento", "governança", "resolução de conflitos", "pesquisa avançada",
            "tese", "análise preditiva", "modelagem", "visão executiva", "alinhamento estratégico", "clínica"
        ]

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extrai texto limpo de PDF."""
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception as e:
            return f"Erro ao ler PDF: {str(e)}"

    def infer_domain_and_role(self, text: str, manual_role: str = "") -> Dict[str, Any]:
        """Classifica dinamicamente a área e o cargo com busca semântica completa."""
        combined_text = f"{manual_role} {text}".lower()

        scores = {}
        for cluster, data in self.domain_clusters.items():
            matches = [kw for kw in data["keywords"] if kw in combined_text]
            scores[cluster] = len(matches)

        best_cluster = max(scores, key=scores.get) if scores and max(scores.values()) > 0 else None

        if manual_role and len(manual_role.strip()) > 1:
            role_name = manual_role.strip()
            if not best_cluster:
                role_lower = role_name.lower()
                if any(w in role_lower for w in ["dev", "soft", "dados", "ti", "program", "code", "tech"]):
                    best_cluster = "Tecnologia, Dados & Inteligência Artificial"
                elif any(w in role_lower for w in ["finan", "banc", "cont", "econ", "fiscal"]):
                    best_cluster = "Economia, Finanças & Investimentos"
                elif any(w in role_lower for w in ["advog", "jurid", "direit", "contrat", "oab"]):
                    best_cluster = "Jurídico, Contratos & Compliance"
                elif any(w in role_lower for w in ["médic", "medic", "saúd", "enferm", "psic", "nutri", "dent"]):
                    best_cluster = "Saúde, Medicina & Biociências"
                elif any(w in role_lower for w in ["desig", "art", "mídia", "comunic", "copy"]):
                    best_cluster = "Design, Mídia & Comunicação"
                elif any(w in role_lower for w in ["vend", "comerc", "sdr", "trade"]):
                    best_cluster = "Vendas, Marketing & Expansão de Negócios"
                elif any(w in role_lower for w in ["prof", "educ", "ensin", "pedag"]):
                    best_cluster = "Educação, Formação & Pedagogia"
                elif any(w in role_lower for w in ["assist", "auxil", "sac", "atend", "recep", "secret"]):
                    best_cluster = "Administração, Suporte & Atendimento Operacional"
                elif any(w in role_lower for w in ["geren", "diret", "coord", "líd", "scrum", "pm"]):
                    best_cluster = "Gestão, Liderança & Estratégia"
                else:
                    best_cluster = "Gestão, Liderança & Estratégia"

            default_rot = self.domain_clusters.get(best_cluster, {}).get("default_routine_ratio", 40)
            return {"domain": best_cluster, "role": role_name, "default_routine": default_rot}

        final_cluster = best_cluster or "Administração, Suporte & Atendimento Operacional"
        inferred_role = self.domain_clusters.get(final_cluster, {}).get("default_role", "Profissional Especialista")
        default_rot = self.domain_clusters.get(final_cluster, {}).get("default_routine_ratio", 40)

        title_patterns = [
            r"(?:cargo|objetivo|função|título|atuação|sou|atua como|experiência como)\s*[:\-]?\s*([^\n\r,]{3,40})",
            r"\b(?:economista|médico|médica|advogado|advogada|engenheiro|engenheira|designer|arquiteto|arquiteta|professor|professora|psicólogo|psicóloga|nutricionista|contador|contadora|analista financeiro|cientista de dados|desenvolvedor|assistente administrativo|vendedor)\b"
        ]
        for pat in title_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                extracted = m.group(1 if m.groups() else 0).strip()
                if 3 < len(extracted) < 45:
                    inferred_role = extracted.title()
                    break

        return {"domain": final_cluster, "role": inferred_role, "default_routine": default_rot}

    def parse_profile(self, text: str, manual_role: str = "", manual_experience_years: int = 0) -> Dict[str, Any]:
        """Estrutura o perfil do candidato com detecção de domínio e sinais comportamentais reais."""
        text_lower = text.lower()
        domain_info = self.infer_domain_and_role(text, manual_role)

        seniority = "Pleno"
        years_exp = manual_experience_years
        if re.search(r"\b(júnior|junior|estagiário|estágio|trainee|residente|iniciante|assistente|auxiliar)\b", text_lower):
            seniority = "Júnior / Iniciante"
            if years_exp == 0: years_exp = 1
        elif re.search(r"\b(sênior|senior|especialista|coordenador|coordenadora|gerente|diretor|diretora|doutor|chefe|titular|lead|head)\b", text_lower):
            seniority = "Sênior / Liderança"
            if years_exp == 0: years_exp = 8
        else:
            if years_exp == 0: years_exp = 3

        detected_soft = [s.title() for s in self.soft_skills_catalog if s in text_lower]

        rot_matches = [kw for kw in self.routine_task_keywords if kw in text_lower]
        strat_matches = [kw for kw in self.strategic_task_keywords if kw in text_lower]

        total_signals = len(rot_matches) + len(strat_matches)
        if total_signals > 0:
            routine_ratio = round((len(rot_matches) / total_signals) * 100)
        else:
            # Usa a taxa intrínseca de rotina daquele domínio profissional específico
            base_dom_rot = domain_info.get("default_routine", 40)
            if "Júnior" in seniority:
                routine_ratio = min(90, base_dom_rot + 15)
            elif "Sênior" in seniority:
                routine_ratio = max(10, base_dom_rot - 15)
            else:
                routine_ratio = base_dom_rot

        strategic_ratio = 100 - routine_ratio

        ai_matches = [t for t in ["ia", "inteligência artificial", "chatgpt", "copilot", "machine learning", "telemedicina", "prompt", "automação", "llm", "claude", "gemini", "cursor"] if t in text_lower]

        return {
            "domain": domain_info["domain"],
            "role": domain_info["role"],
            "seniority": seniority,
            "years_experience": years_exp,
            "detected_soft_skills": detected_soft if detected_soft else ["Comunicação", "Pensamento Crítico"],
            "routine_tasks_ratio": routine_ratio,
            "strategic_tasks_ratio": strategic_ratio,
            "has_ai_experience": len(ai_matches) > 0,
            "ai_tools_found": ai_matches
        }