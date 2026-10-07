"""
Agente Analisador de Currículo e Competências (ResumeParserAgent)
Refatorado para suportar Classificação Multidomínio Dinâmica e Zero Contaminação.
"""

import io
import re
from typing import Dict, Any, List


class ResumeParserAgent:
    def __init__(self):
        self.name = "ResumeParserAgent"
        self.role = "Especialista em Triagem, Competências e Auditoria Multidomínio"

        # Ontologia de Clusters Profissionais para Inferência Semântica Dinâmica
        self.domain_clusters = {
            "Economia, Finanças & Investimentos": {
                "keywords": [
                    "economista", "economia", "macroeconomia", "microeconomia", "econometria",
                    "cfa", "anbima", "fp&a", "valuation", "investimentos", "tesouraria",
                    "cbdc", "tokenização", "esg", "risco financeiro", "mercado de capitais",
                    "derivativos", "planejamento financeiro", "gestão de carteiras", "controladoria",
                    "contábil", "contador", "auditoria fiscal", "tributário", "finanças", "banco"
                ],
                "default_role": "Economista / Analista de Investimentos"
            },
            "Saúde, Medicina & Biociências": {
                "keywords": [
                    "médico", "médica", "medicina", "crm", "clínica", "hospital", "diagnóstico",
                    "cirurgia", "paciente", "prontuário", "anamnese", "telemedicina",
                    "genômica", "farmacologia", "biomarcadores", "epidemiologia", "enfermagem",
                    "nutrição", "nutricionista", "fisioterapia", "fisioterapeuta", "psicologia",
                    "psicólogo", "terapêutico", "saúde pública", "odontologia", "dentista", "veterinária"
                ],
                "default_role": "Médico(a) / Especialista em Saúde"
            },
            "Jurídico, Contratos & Compliance": {
                "keywords": [
                    "advogado", "advogada", "direito", "oab", "jurídico", "contratos",
                    "contencioso", "compliance", "lgpd", "processo civil", "parecer jurídico",
                    "tributário", "societário", "jurisprudência", "petição", "magistratura", "promotoria"
                ],
                "default_role": "Advogado(a) / Consultor(a) Jurídico"
            },
            "Design, Mídia & Comunicação": {
                "keywords": [
                    "designer", "design", "figma", "photoshop", "illustrator", "ui/ux",
                    "direção de arte", "copywriting", "redação", "storytelling", "branding",
                    "mídia digital", "jornalismo", "comunicação corporativa", "redator", "publicitário"
                ],
                "default_role": "Designer / Especialista em Comunicação"
            },
            "Engenharia, Construção & Manufatura": {
                "keywords": [
                    "engenheiro", "engenharia", "civil", "mecânica", "elétrica", "química", "crea",
                    "autocad", "revit", "bim", "obra", "instalações", "gêmeos digitais", "produção industrial",
                    "manufatura", "estrutural", "climatização", "automação industrial", "arquiteto", "arquitetura"
                ],
                "default_role": "Engenheiro(a) de Projetos e Operações"
            },
            "Tecnologia, Dados & Inteligência Artificial": {
                "keywords": [
                    "software", "desenvolvedor", "programador", "fullstack", "backend", "frontend",
                    "python", "react", "node", "sql", "aws", "docker", "kubernetes",
                    "machine learning", "data science", "devops", "qa", "arquiteto de software", "tech lead"
                ],
                "default_role": "Engenheiro(a) de Software / Cientista de Dados"
            },
            "Vendas, Marketing & Expansão de Negócios": {
                "keywords": [
                    "vendas", "comercial", "sdr", "bdr", "account executive", "crm",
                    "growth", "tráfego pago", "negociação", "parcerias", "varejo", "go-to-market",
                    "vendedor", "atendimento", "sac", "telemarketing"
                ],
                "default_role": "Especialista Comercial & Growth"
            },
            "Educação, Formação & Pedagogia": {
                "keywords": [
                    "professor", "professora", "educador", "educadora", "docente", "pedagogo",
                    "pedagogia", "ensino", "escola", "aula", "treinamento", "aluno", "instrutor"
                ],
                "default_role": "Educador(a) / Especialista em Aprendizagem"
            },
            "Gestão, Estratégia & Recursos Humanos": {
                "keywords": [
                    "recursos humanos", "rh", "recrutador", "talent acquisition", "people analytics",
                    "gerente de projetos", "scrum master", "coordenador", "diretor", "operações", "bizops"
                ],
                "default_role": "Gestor(a) Estratégico / People Operations"
            }
        }

        self.soft_skills_catalog = [
            "pensamento analítico", "pensamento crítico", "liderança", "comunicação",
            "inteligência emocional", "empatia", "negociação", "resolução de problemas",
            "resiliência", "adaptabilidade", "flexibilidade", "trabalho em equipe",
            "gestão de tempo", "criatividade", "ética", "aprendizado contínuo", "visão sistêmica"
        ]

        self.routine_task_keywords = [
            "digitação", "planilha", "alimentação de dados", "arquivo", "relatórios manuais",
            "atendimento telefônico", "agendamento", "cadastro", "triagem", "notas fiscais",
            "manutenção básica", "repetitivo", "rotina", "preenchimento", "copiar e colar"
        ]

        self.strategic_task_keywords = [
            "arquitetura", "liderança", "estratégia", "negociação", "tomada de decisão",
            "diagnóstico", "auditoria", "gestão de equipe", "inovação", "mentoria",
            "planejamento", "governança", "resolução de conflitos", "pesquisa avançada"
        ]

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extrai texto limpo de PDF."""
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception as e:
            return f"Erro ao ler PDF: {str(e)}"

    def infer_domain_and_role(self, text: str, manual_role: str = "") -> Dict[str, str]:
        """Classifica dinamicamente a área e o cargo sem viés de TI."""
        if manual_role and len(manual_role.strip()) > 2:
            query = manual_role.lower()
            for cluster, data in self.domain_clusters.items():
                if any(kw in query for kw in data["keywords"]):
                    return {"domain": cluster, "role": manual_role.strip()}
            return {"domain": f"Área de {manual_role.strip()}", "role": manual_role.strip()}

        text_lower = text.lower()
        scores = {}

        for cluster, data in self.domain_clusters.items():
            matches = [kw for kw in data["keywords"] if re.search(rf"\b{re.escape(kw)}\b", text_lower)]
            scores[cluster] = len(matches)

        best_cluster = max(scores, key=scores.get) if scores and max(scores.values()) > 0 else "Geral / Multissetorial"
        inferred_role = self.domain_clusters.get(best_cluster, {}).get("default_role", "Profissional Especialista")

        title_patterns = [
            r"(?:cargo|objetivo|função|título|atuação|sou|atua como|experiência como)\s*[:\-]?\s*([^\n\r,]{3,40})",
            r"\b(?:economista|médico|médica|advogado|advogada|engenheiro|engenheira|designer|arquiteto|arquiteta|professor|professora|psicólogo|psicóloga|nutricionista|contador|contadora|analista financeiro|cientista de dados)\b"
        ]
        for pat in title_patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                extracted = m.group(1 if m.groups() else 0).strip()
                if 3 < len(extracted) < 45:
                    inferred_role = extracted.title()
                    break

        return {"domain": best_cluster, "role": inferred_role}

    def parse_profile(self, text: str, manual_role: str = "", manual_experience_years: int = 0) -> Dict[str, Any]:
        """Estrutura o perfil do candidato com detecção de domínio agnóstica a setor."""
        text_lower = text.lower()
        domain_info = self.infer_domain_and_role(text, manual_role)

        seniority = "Pleno"
        years_exp = manual_experience_years
        if re.search(r"\b(júnior|junior|estagiário|estágio|trainee|residente|iniciante)\b", text_lower):
            seniority = "Júnior / Iniciante"
            if years_exp == 0: years_exp = 1
        elif re.search(r"\b(sênior|senior|especialista|coordenador|gerente|diretor|doutor|chefe|titular)\b", text_lower):
            seniority = "Sênior / Liderança"
            if years_exp == 0: years_exp = 7
        else:
            if years_exp == 0: years_exp = 3

        detected_soft = [s.title() for s in self.soft_skills_catalog if re.search(rf"\b{re.escape(s)}\b", text_lower)]

        rot_matches = [kw for kw in self.routine_task_keywords if re.search(rf"\b{re.escape(kw)}\b", text_lower)]
        strat_matches = [kw for kw in self.strategic_task_keywords if re.search(rf"\b{re.escape(kw)}\b", text_lower)]
        
        total_signals = len(rot_matches) + len(strat_matches)
        if total_signals > 0:
            routine_ratio = round((len(rot_matches) / total_signals) * 100)
        else:
            routine_ratio = 60 if "Júnior" in seniority else (40 if "Pleno" in seniority else 20)
        strategic_ratio = 100 - routine_ratio

        ai_matches = [t for t in ["ia", "inteligência artificial", "chatgpt", "copilot", "machine learning", "telemedicina", "prompt", "automação"] if t in text_lower]

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