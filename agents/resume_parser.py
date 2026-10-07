"""
Agente Analisador de Currículo e Competências (ResumeParserAgent)
Classificação Multidomínio Dinâmica, Detecção Semântica e Extração de Sinais Reais.
"""

import io
import re
from typing import Dict, Any, List


class ResumeParserAgent:
    def __init__(self):
        self.name = "ResumeParserAgent"
        self.role = "Especialista em Triagem, Competências e Auditoria Multidomínio"

        # Ontologia Ampla de Clusters Profissionais com sinônimos e radicais
        self.domain_clusters = {
            "Economia, Finanças & Investimentos": {
                "keywords": [
                    "economista", "economia", "macroeconomia", "microeconomia", "econometria",
                    "cfa", "anbima", "fp&a", "valuation", "investimento", "investimentos", "tesouraria",
                    "cbdc", "tokenização", "esg", "risco financeiro", "mercado de capitais",
                    "derivativos", "planejamento financeiro", "gestão de carteiras", "controladoria",
                    "contábil", "contabilidade", "contador", "contadora", "auditoria", "fiscal",
                    "tributário", "finanças", "financeiro", "financeira", "banco", "bancário", "crédito",
                    "faturamento", "contas a pagar", "contas a receber"
                ],
                "default_role": "Analista / Consultor Financeiro"
            },
            "Saúde, Medicina & Biociências": {
                "keywords": [
                    "médico", "médica", "medicina", "crm", "clínica", "hospital", "diagnóstico",
                    "cirurgia", "cirurgião", "paciente", "prontuário", "anamnese", "telemedicina",
                    "genômica", "farmacologia", "farmácia", "farmacêutico", "biomarcadores", "epidemiologia",
                    "enfermagem", "enfermeiro", "enfermeira", "nutrição", "nutricionista", "fisioterapia",
                    "fisioterapeuta", "psicologia", "psicólogo", "psicóloga", "terapeuta", "terapêutico",
                    "saúde", "odontologia", "dentista", "veterinária", "veterinário", "biomedicina"
                ],
                "default_role": "Especialista em Saúde / Cuidados Clínicos"
            },
            "Jurídico, Contratos & Compliance": {
                "keywords": [
                    "advogado", "advogada", "direito", "oab", "jurídico", "jurídica", "contrato",
                    "contratos", "contencioso", "compliance", "lgpd", "processo civil", "processual",
                    "parecer", "tributário", "societário", "jurisprudência", "petição", "magistratura",
                    "promotoria", "defensoria", "notarial", "cartório", "leis", "legal"
                ],
                "default_role": "Advogado(a) / Especialista Jurídico"
            },
            "Design, Mídia & Comunicação": {
                "keywords": [
                    "designer", "design", "figma", "photoshop", "illustrator", "ui", "ux", "ui/ux",
                    "arte", "direção de arte", "copywriting", "copywriter", "redação", "redator", "redatora",
                    "storytelling", "branding", "mídia", "mídias", "jornalismo", "jornalista",
                    "comunicação", "publicidade", "publicitário", "marketing digital", "vídeo", "audiovisual",
                    "conteúdo", "social media", "ilustrador", "gráfico"
                ],
                "default_role": "Designer / Especialista em Comunicação Criativa"
            },
            "Engenharia, Construção & Manufatura": {
                "keywords": [
                    "engenheiro", "engenheira", "engenharia", "civil", "mecânica", "elétrica", "química",
                    "crea", "autocad", "revit", "bim", "obra", "obras", "instalações", "gêmeos digitais",
                    "produção industrial", "manufatura", "estrutural", "climatização", "automação industrial",
                    "arquiteto", "arquiteta", "arquitetura", "construção", "projetista", "logística de fábrica"
                ],
                "default_role": "Engenheiro(a) de Projetos e Operações"
            },
            "Tecnologia, Dados & Inteligência Artificial": {
                "keywords": [
                    "software", "desenvolvedor", "desenvolvedora", "programador", "programadora", "dev",
                    "fullstack", "backend", "frontend", "python", "react", "node", "javascript", "typescript",
                    "sql", "aws", "azure", "docker", "kubernetes", "machine learning", "data science",
                    "ciência de dados", "engenheiro de dados", "analista de dados", "devops", "qa",
                    "arquiteto de software", "tech lead", "cto", "cloud", "segurança da informação", "cibersegurança"
                ],
                "default_role": "Engenheiro(a) de Software / Especialista em Dados & IA"
            },
            "Vendas, Marketing & Expansão de Negócios": {
                "keywords": [
                    "venda", "vendas", "vendedor", "vendedora", "comercial", "sdr", "bdr", "executivo de contas",
                    "account executive", "crm", "growth", "tráfego pago", "negociação", "parcerias", "varejo",
                    "go-to-market", "prospecção", "inside sales", "atendimento", "sac", "telemarketing",
                    "call center", "representante comercial", "key account"
                ],
                "default_role": "Especialista em Vendas & Expansão Comercial"
            },
            "Educação, Formação & Pedagogia": {
                "keywords": [
                    "professor", "professora", "educador", "educadora", "docente", "pedagogo", "pedagoga",
                    "pedagogia", "ensino", "escola", "aula", "treinamento", "instrutor", "instrutora",
                    "coordenador pedagógico", "didática", "ead", "tutor", "mentoria"
                ],
                "default_role": "Educador(a) / Especialista em Aprendizagem"
            },
            "Gestão, Estratégia & Recursos Humanos": {
                "keywords": [
                    "recursos humanos", "rh", "recrutador", "recrutadora", "talent acquisition", "people",
                    "people analytics", "gerente", "gerência", "gestor", "gestora", "scrum master",
                    "product owner", "product manager", "coordenador", "diretor", "operações", "bizops",
                    "administração", "administrador", "assistente administrativo", "auxiliar administrativo",
                    "secretária", "secretário", "office", "planejamento estratégico"
                ],
                "default_role": "Gestor(a) Estratégico / Operações"
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
            "conferência manual", "emissão de notas", "consulta padrão", "resposta de chamados"
        ]

        self.strategic_task_keywords = [
            "arquitetura", "liderança", "estratégia", "negociação", "tomada de decisão",
            "diagnóstico", "auditoria", "gestão de equipe", "inovação", "mentoria",
            "planejamento", "governança", "resolução de conflitos", "pesquisa avançada",
            "tese", "análise preditiva", "modelagem", "visão executiva", "alinhamento estratégico"
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
        """Classifica dinamicamente a área e o cargo com busca semântica completa."""
        combined_text = f"{manual_role} {text}".lower()

        # 1. Busca por pontuação de keywords nos clusters
        scores = {}
        for cluster, data in self.domain_clusters.items():
            matches = [kw for kw in data["keywords"] if kw in combined_text]
            scores[cluster] = len(matches)

        best_cluster = max(scores, key=scores.get) if scores and max(scores.values()) > 0 else None

        # Se manual_role foi fornecido
        if manual_role and len(manual_role.strip()) > 1:
            role_name = manual_role.strip()
            if not best_cluster:
                # Se não encontrou cluster, infere o mais próximo
                role_lower = role_name.lower()
                if any(w in role_lower for w in ["dev", "soft", "dados", "ti", "program"]):
                    best_cluster = "Tecnologia, Dados & Inteligência Artificial"
                elif any(w in role_lower for w in ["finan", "banc", "cont", "econ"]):
                    best_cluster = "Economia, Finanças & Investimentos"
                elif any(w in role_lower for w in ["advog", "jurid", "direit", "contrat"]):
                    best_cluster = "Jurídico, Contratos & Compliance"
                elif any(w in role_lower for w in ["médic", "medic", "saúd", "enferm", "psic"]):
                    best_cluster = "Saúde, Medicina & Biociências"
                elif any(w in role_lower for w in ["desig", "art", "mídia", "comunic"]):
                    best_cluster = "Design, Mídia & Comunicação"
                elif any(w in role_lower for w in ["vend", "comerc", "atend"]):
                    best_cluster = "Vendas, Marketing & Expansão de Negócios"
                elif any(w in role_lower for w in ["prof", "educ", "ensin"]):
                    best_cluster = "Educação, Formação & Pedagogia"
                elif any(w in role_lower for w in ["engenh", "civil", "obras", "arq"]):
                    best_cluster = "Engenharia, Construção & Manufatura"
                else:
                    best_cluster = "Gestão, Estratégia & Recursos Humanos"

            return {"domain": best_cluster, "role": role_name}

        # Se não forneceu manual_role, tenta extrair do texto
        final_cluster = best_cluster or "Gestão, Estratégia & Recursos Humanos"
        inferred_role = self.domain_clusters.get(final_cluster, {}).get("default_role", "Profissional Especialista")

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

        return {"domain": final_cluster, "role": inferred_role}

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
            # Baseline diferenciado por cargo e senioridade
            role_l = domain_info["role"].lower()
            if any(w in role_l for w in ["assistente", "auxiliar", "atendente", "sac", "digitador"]):
                routine_ratio = 80
            elif any(w in role_l for w in ["lead", "arquiteto", "diretor", "gerente", "estrat"]):
                routine_ratio = 15
            elif "Júnior" in seniority:
                routine_ratio = 65
            elif "Sênior" in seniority:
                routine_ratio = 25
            else:
                routine_ratio = 45

        strategic_ratio = 100 - routine_ratio

        ai_matches = [t for t in ["ia", "inteligência artificial", "chatgpt", "copilot", "machine learning", "telemedicina", "prompt", "automação", "llm", "claude", "gemini"] if t in text_lower]

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