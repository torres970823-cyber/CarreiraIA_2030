"""
CarreiraIA 2030 — Plataforma Agêntica de Inteligência de Carreira & Impacto de IA
Baseada nas diretrizes de agentes_universais.md e nos dados oficiais do Fórum Econômico Mundial (WEF) e McKinsey.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import json
import os
import sys
from datetime import datetime

# Importar agentes do pacote local
from agents.security_reviewer import SecurityReviewerAgent
from agents.resume_parser import ResumeParserAgent
from agents.researcher import ResearcherAgent
from agents.ai_evaluator import AIEvaluatorAgent
from agents.career_strategist import CareerStrategistAgent

# Importar FPDF para exportação PDF
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False

# ─────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CarreiraIA 2030 | Diagnóstico de Carreira & IA",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────
# SEÇÃO 1 — CSS COMPLETO (Paleta Nova, Fundo Branco)
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8F9FA !important;
    }

    /* ── HEADER ── */
    .main-header {
        background: linear-gradient(135deg, #780D34 0%, #951165 35%, #CB1D4E 65%, #E6228C 100%);
        padding: 2.5rem 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px -8px rgba(120, 13, 52, 0.45);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -60px;
        right: -60px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: rgba(247, 175, 32, 0.15);
    }
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -40px;
        left: 30%;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: rgba(230, 34, 140, 0.2);
    }

    /* ── BADGE WEF ── */
    .badge-wef {
        background: rgba(247, 175, 32, 0.25);
        border: 1.5px solid #F7AF20;
        color: #F7AF20;
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1rem;
    }

    /* ── BADGE DE NÍVEL DE RISCO ── */
    .badge-risk-alto {
        background: #D83C15;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-risk-medio {
        background: #E07618;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-risk-baixo {
        background: #2E7D32;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-critico {
        background: linear-gradient(90deg, #CB1D4E, #D83C15);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }

    /* ── METRIC CARDS ── */
    .metric-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.6rem 1.4rem;
        border: 1.5px solid #F0F0F0;
        border-left: 5px solid #951165;
        box-shadow: 0 4px 16px -4px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px -6px rgba(149, 17, 101, 0.18);
    }
    .metric-card-danger {
        border-left-color: #D83C15;
    }
    .metric-card-warning {
        border-left-color: #E07618;
    }
    .metric-card-success {
        border-left-color: #2E7D32;
    }
    .metric-card-info {
        border-left-color: #E6228C;
    }
    .metric-card-purple {
        border-left-color: #951165;
    }

    .metric-label {
        color: #6B7280;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0.3rem 0 0.5rem 0;
        line-height: 1;
    }
    .metric-sub {
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* ── TASK BOXES ── */
    .task-box {
        padding: 1.4rem;
        border-radius: 14px;
        min-height: 260px;
        box-shadow: 0 2px 8px -2px rgba(0,0,0,0.07);
        background: #FFFFFF;
    }
    .task-threatened {
        border: 1.5px solid #D83C15;
        border-top: 4px solid #D83C15;
    }
    .task-augmented {
        border: 1.5px solid #E07618;
        border-top: 4px solid #E07618;
    }
    .task-human {
        border: 1.5px solid #2E7D32;
        border-top: 4px solid #2E7D32;
    }

    /* ── SECTION CARD ── */
    .section-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.8rem;
        border: 1.5px solid #F0F0F0;
        border-left: 5px solid #F7AF20;
        box-shadow: 0 4px 14px -4px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }
    .section-card-pink {
        border-left-color: #E6228C;
    }
    .section-card-orange {
        border-left-color: #E07618;
    }
    .section-card-red {
        border-left-color: #D83C15;
    }
    .section-card-purple {
        border-left-color: #951165;
    }

    /* ── EXECUTIVE SUMMARY CARD ── */
    .exec-summary {
        background: linear-gradient(135deg, #FFF8F0 0%, #FFF0F5 100%);
        border: 1.5px solid #F7AF20;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px -4px rgba(247, 175, 32, 0.2);
    }

    /* ── SIDEBAR HISTORY ITEM ── */
    .history-item {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #951165;
        font-size: 0.82rem;
        box-shadow: 0 2px 6px -2px rgba(0,0,0,0.06);
    }
    .history-item-critico { border-left-color: #CB1D4E; }
    .history-item-alto { border-left-color: #D83C15; }
    .history-item-medio { border-left-color: #E07618; }
    .history-item-baixo { border-left-color: #2E7D32; }

    /* ── BOTÕES ── */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(90deg, #780D34, #CB1D4E) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em;
        box-shadow: 0 4px 14px -2px rgba(120, 13, 52, 0.4) !important;
        transition: all 0.2s !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #CB1D4E, #E07618) !important;
        box-shadow: 0 6px 20px -2px rgba(203, 29, 78, 0.5) !important;
        transform: translateY(-2px);
    }

    /* ── PROGRESS BAR OVERRIDE ── */
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #951165, #E6228C) !important;
    }

    /* ── SEPARATOR COLORIDO ── */
    .color-sep {
        height: 3px;
        background: linear-gradient(90deg, #F7AF20, #E07618, #D83C15, #CB1D4E, #E6228C, #951165);
        border-radius: 9999px;
        margin: 1.5rem 0;
    }

    /* ── SKILL PILL ── */
    .skill-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .skill-pill-grow {
        background: rgba(149, 17, 101, 0.1);
        color: #951165;
        border: 1px solid #951165;
    }
    .skill-pill-decline {
        background: rgba(216, 60, 21, 0.1);
        color: #D83C15;
        border: 1px solid #D83C15;
    }

    /* ── COMPARADOR CARD ── */
    .compare-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid #F7AF20;
        box-shadow: 0 4px 16px -4px rgba(247, 175, 32, 0.2);
    }
    .compare-card-b {
        border-color: #E6228C;
        box-shadow: 0 4px 16px -4px rgba(230, 34, 140, 0.2);
    }

    /* ── MISC ── */
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #951165 !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# INICIALIZAÇÃO DE SESSION STATE
# ─────────────────────────────────────────────────────────
if 'analysis_history' not in st.session_state:
    st.session_state['analysis_history'] = []

if 'last_results' not in st.session_state:
    st.session_state['last_results'] = None


# ─────────────────────────────────────────────────────────
# INICIALIZAR AGENTES
# ─────────────────────────────────────────────────────────
@st.cache_resource
def get_agents():
    security_agent = SecurityReviewerAgent()
    parser_agent = ResumeParserAgent()
    researcher_agent = ResearcherAgent()
    evaluator_agent = AIEvaluatorAgent()
    strategist_agent = CareerStrategistAgent()
    return security_agent, parser_agent, researcher_agent, evaluator_agent, strategist_agent

security_agent, parser_agent, researcher_agent, evaluator_agent, strategist_agent = get_agents()


# ─────────────────────────────────────────────────────────
# PRESETS DE CURRÍCULO
# ─────────────────────────────────────────────────────────
PRESET_CV_TEXTS = {
    "dev_junior": """Carlos Silva
Desenvolvedor Front-end Júnior
Experiência: 1 ano e meio com desenvolvimento web.
Atividades diárias: Criação de telas e componentes básicos em React e HTML/CSS a partir de layouts do Figma. Correção de bugs simples de formulários, consumo de APIs REST prontas e testes manuais de interface.
Habilidades: JavaScript, React, HTML5, CSS3, Git, GitHub, noções de TypeScript.
Objetivo: Crescer como desenvolvedor fullstack e entender mais sobre boas práticas de arquitetura.""",

    "dev_senior": """Mariana Albuquerque
Tech Lead & Arquiteta de Software Sênior
Experiência: 9 anos em engenharia de software distribuída.
Atividades diárias: Definição de arquitetura de microsserviços em nuvem (AWS), mentoria técnica de engenheiros pleno e júnior, decisões de trade-off de escalabilidade e segurança, code review semântico e alinhamento estratégico com C-Level.
Habilidades: Python, Go, Docker, Kubernetes, AWS, Arquitetura Hexagonal, Microservices, CI/CD, Pensamento Crítico, Liderança de Equipes.""",

    "assistente_adm": """Ana Paula Santos
Assistente Administrativa
Experiência: 4 anos em rotinas de escritório e compras.
Atividades diárias: Preenchimento manual de planilhas de controle no Excel, lançamento e conferência de notas fiscais no sistema ERP, agendamento de reuniões para gerência, arquivo de comprovantes e elaboração de relatórios semanais de despesas.
Habilidades: Excel intermediário, Word, digitação rápida, atendimento ao cliente, organização de documentos.""",

    "analista_financeiro": """Rodrigo Mendes
Analista Financeiro / FP&A
Experiência: 3 anos em controladoria e planejamento orçamentário.
Atividades diárias: Consolidação de relatórios mensais de receita e despesas em planilhas Excel, análise descritiva de desvios de orçamento, conciliação de contas a pagar e receber, confecção de slides para diretoria.
Habilidades: Excel Avançado, Finanças Corporativas, Matemática Financeira, ERP SAP, PowerBI básico.""",

    "advogado_junior": """Beatriz Lima
Advogada Associada / Analista de Contratos
Experiência: 2 anos em direito corporativo.
Atividades diárias: Revisão manual de minutas de contratos de prestação de serviços e NDAs, pesquisa de jurisprudência em tribunais, redação de petições iniciais padronizadas de cobrança e triagem de publicações em diários oficiais.
Habilidades: Direito Contratual, Pesquisa Jurisprudencial, Redação Jurídica, OAB ativa, Negociação básica.""",

    "designer_grafico": """Lucas Farias
Designer Gráfico & Mídias Digitais
Experiência: 3 anos em agências de marketing.
Atividades diárias: Criação de banners estáticos para redes sociais (Instagram, Facebook), recorte manual de fotos de produtos em e-commerce, ajuste de formatos para anúncios digitais e diagramação de e-books simples.
Habilidades: Photoshop, Illustrator, InDesign, Canva, Teoria das Cores, Tipografia.""",

    "atendente_sac": """Juliana Rocha
Operadora de Atendimento ao Cliente / SAC
Experiência: 2 anos em contact center.
Atividades diárias: Atendimento a chamados de clientes por telefone e chat para tirar dúvidas frequentes de pedidos, emissão de 2ª via de faturas, abertura de tickets de suporte e aplicação de script de retenção de cancelamento.
Habilidades: Comunicação verbal, digitação, empatia, sistemas de CRM, escuta ativa.""",

    "gerente_projetos": """Felipe Andrade
Gerente de Projetos Ágeis / Scrum Master
Experiência: 6 anos liderando entregas em tecnologia.
Atividades diárias: Facilitação de cerimônias ágeis (Dailies, Plannings, Retrospectivas), acompanhamento diário de impedimentos do time no Jira, negociação de escopo com stakeholders de negócios e gestão de cronogramas.
Habilidades: Scrum, Kanban, Jira, Liderança de Equipes, Gestão de Conflitos, OKRs, Comunicação Executiva."""
}


# ─────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────
def get_risk_badge(risk_level: str) -> str:
    """Retorna HTML do badge colorido conforme nível de risco."""
    level_lower = str(risk_level).lower()
    if "crítico" in level_lower or "critico" in level_lower:
        return f'<span class="badge-critico">🔴 {risk_level}</span>'
    elif "alto" in level_lower:
        return f'<span class="badge-risk-alto">🟠 {risk_level}</span>'
    elif "médio" in level_lower or "medio" in level_lower:
        return f'<span class="badge-risk-medio">🟡 {risk_level}</span>'
    else:
        return f'<span class="badge-risk-baixo">🟢 {risk_level}</span>'


def get_risk_color(risk_value: int) -> str:
    """Retorna cor hexadecimal com base no valor de risco."""
    if risk_value >= 70:
        return "#D83C15"
    elif risk_value >= 45:
        return "#E07618"
    else:
        return "#2E7D32"


def get_history_class(risk_level: str) -> str:
    """Retorna classe CSS do item de histórico conforme risco."""
    level_lower = str(risk_level).lower()
    if "crítico" in level_lower or "critico" in level_lower:
        return "history-item-critico"
    elif "alto" in level_lower:
        return "history-item-alto"
    elif "médio" in level_lower or "medio" in level_lower:
        return "history-item-medio"
    return "history-item-baixo"


def run_full_pipeline(cv_text: str, role: str = "", exp_years: int = 3):
    """Executa o pipeline completo dos 5 agentes e retorna todos os resultados."""
    with st.status("Orquestrando agentes especializados...", expanded=True) as status:
        st.write("🛡️ **[SecurityReviewerAgent]** Inspecionando dados sensíveis e conformidade LGPD...")
        sanitized_cv, sec_audit = security_agent.audit_and_sanitize(cv_text)
        st.caption(
            f"✓ Mascarados: {sec_audit['cpf_masked']} CPFs, "
            f"{sec_audit['phones_masked']} telefones, "
            f"{sec_audit['emails_masked']} e-mails. Dados sanitizados."
        )

        st.write("📑 **[ResumeParserAgent]** Extraindo entidades, senioridade e divisão de rotina...")
        parsed_profile = parser_agent.parse_profile(
            sanitized_cv, manual_role=role, manual_experience_years=exp_years
        )
        st.caption(
            f"✓ Área: **{parsed_profile['role']}** | "
            f"Senioridade: **{parsed_profile['seniority']}** | "
            f"Rotina: **{parsed_profile['routine_tasks_ratio']}% repetitiva** vs "
            f"**{parsed_profile['strategic_tasks_ratio']}% cognitiva**."
        )

        st.write(
            f"📊 **[ResearcherAgent]** Cruzando perfil de '{parsed_profile['role']}' "
            "com bases do World Economic Forum 2025/2030 e McKinsey..."
        )
        benchmark = researcher_agent.match_occupation(
            role=parsed_profile['role'],
            domain=parsed_profile.get('domain', ''),
            cv_text=sanitized_cv
        )
        st.caption(
            f"✓ Setor: **{benchmark.get('category', 'Multissetorial')}** — "
            f"Comparativo para **{benchmark.get('title')}**."
        )

        st.write("⚡ **[AIEvaluatorAgent]** Calculando índices de automação e potencial de aumento...")
        evaluation = evaluator_agent.evaluate_profile(parsed_profile, benchmark)
        st.caption(
            f"✓ Risco: **{evaluation['final_automation_risk']}% ({evaluation['risk_level']})** | "
            f"Potencial de Aumento: **{evaluation['final_augmentation_potential']}%**."
        )

        st.write("🎯 **[CareerStrategistAgent]** Formulando roadmap tático 2026-2030...")
        strategy = strategist_agent.generate_strategy(parsed_profile, benchmark, evaluation)
        st.caption(
            f"✓ Roadmap gerado: {len(strategy['roadmap'])} fases, "
            f"{len(strategy['career_pivots'])} pivôs recomendados."
        )

        status.update(
            label="✅ Diagnóstico Concluído com Sucesso por todos os Agentes!",
            state="complete",
            expanded=False
        )

    return parsed_profile, benchmark, evaluation, strategy


# ─────────────────────────────────────────────────────────
# SEÇÃO 4 — GERAÇÃO DE PDF
# ─────────────────────────────────────────────────────────
def generate_pdf_report(parsed_profile, benchmark, evaluation, strategy) -> bytes:
    """Gera o relatório em PDF usando fpdf2 e retorna os bytes."""
    pdf = FPDF()
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    # Título
    pdf.set_fill_color(120, 13, 52)
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(18, 10)
    pdf.cell(0, 12, 'CarreiraIA 2030 — Dossie de Carreira', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_xy(18, 24)
    pdf.cell(0, 8, f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}', ln=True)

    pdf.set_y(45)
    pdf.set_text_color(30, 30, 30)

    # Perfil
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '1. Perfil Identificado', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, f"Cargo/Funcao: {parsed_profile.get('role', 'N/A')}", ln=True)
    pdf.cell(0, 7, f"Senioridade: {parsed_profile.get('seniority', 'N/A')}", ln=True)
    pdf.cell(0, 7, f"Tarefas Repetitivas: {parsed_profile.get('routine_tasks_ratio', 0)}%", ln=True)
    pdf.cell(0, 7, f"Tarefas Cognitivas: {parsed_profile.get('strategic_tasks_ratio', 0)}%", ln=True)
    pdf.ln(4)

    # Métricas Principais
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '2. Metricas Principais', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, f"Risco de Automacao: {evaluation.get('final_automation_risk', 0)}% — Nivel: {evaluation.get('risk_level', 'N/A')}", ln=True)
    pdf.cell(0, 7, f"Potencial de Aumento (IA Copiloto): +{evaluation.get('final_augmentation_potential', 0)}%", ln=True)
    pdf.cell(0, 7, f"Multiplicador de Produtividade: {evaluation.get('productivity_multiplier', 'N/A')}", ln=True)
    pdf.ln(4)

    # Gaps Críticos
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '3. Gaps Criticos de Competencia', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    gaps = evaluation.get('critical_gaps', [])
    if gaps:
        for g in gaps:
            pdf.cell(0, 7, f"  - {g.get('skill', '')}: Atual {g.get('current', 0)}/10 -> Meta {g.get('ideal', 0)}/10 (Gap: -{g.get('gap', 0)} pts)", ln=True)
    else:
        pdf.cell(0, 7, '  Nenhum gap critico detectado.', ln=True)
    pdf.ln(4)

    # Tarefas Ameacadas
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '4. Tarefas Ameacadas pela IA ate 2028', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    for t in benchmark.get('declining_tasks', []):
        safe_t = str(t).encode('latin-1', errors='replace').decode('latin-1')
        pdf.cell(0, 7, f'  - {safe_t}', ln=True)
    pdf.ln(4)

    # Habilidades Emergentes
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '5. Habilidades a Desenvolver com Urgencia', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    for sk in strategy.get('emerging_skills', []):
        safe_sk = str(sk).encode('latin-1', errors='replace').decode('latin-1')
        pdf.cell(0, 7, f'  + {safe_sk}', ln=True)
    pdf.ln(4)

    # Roadmap
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '6. Roadmap de Requalificacao 2026-2030', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    for phase in strategy.get('roadmap', []):
        period = str(phase.get('period', '')).encode('latin-1', errors='replace').decode('latin-1')
        theme = str(phase.get('theme', '')).encode('latin-1', errors='replace').decode('latin-1')
        goal = str(phase.get('goal', '')).encode('latin-1', errors='replace').decode('latin-1')
        action = str(phase.get('action', '')).encode('latin-1', errors='replace').decode('latin-1')
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, f'  {period}: {theme}', ln=True)
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 6, f'    Meta: {goal}')
        pdf.multi_cell(0, 6, f'    Acao: {action}')
        pdf.ln(2)

    # Career Pivots
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '7. Transicoes de Carreira Recomendadas', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    for pivot in strategy.get('career_pivots', []):
        safe_pivot = str(pivot).encode('latin-1', errors='replace').decode('latin-1')
        pdf.cell(0, 7, f'  -> {safe_pivot}', ln=True)
    pdf.ln(4)

    # Certificações
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(120, 13, 52)
    pdf.cell(0, 10, '8. Certificacoes Recomendadas', ln=True)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    for cert in strategy.get('recommended_certifications', []):
        safe_cert = str(cert).encode('latin-1', errors='replace').decode('latin-1')
        pdf.cell(0, 7, f'  * {safe_cert}', ln=True)

    # Rodapé
    pdf.set_y(-20)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, 'CarreiraIA 2030 — Sistema Agetico de Inteligencia de Carreira | Dados: WEF Future of Jobs 2025 & McKinsey', align='C')

    return bytes(pdf.output())


# ─────────────────────────────────────────────────────────
# SEÇÃO 2 — SIDEBAR REFORMULADA
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🚀</div>
        <div style="font-size: 1.3rem; font-weight: 800; color: #780D34; line-height: 1.2;">CarreiraIA 2030</div>
        <div style="font-size: 0.78rem; color: #6B7280; font-weight: 500; margin-top: 0.2rem;">Sistema Agêntico de Inteligência de Carreira</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)

    st.markdown("**⚡ Presets de Teste Rápido**")
    st.markdown('<span style="font-size:0.82rem; color:#6B7280;">Selecione um perfil pré-configurado:</span>', unsafe_allow_html=True)

    occupations_list = researcher_agent.list_available_occupations()
    preset_options = {occ["title"]: occ["id"] for occ in occupations_list}

    selected_preset_title = st.selectbox("Escolha um Perfil:", list(preset_options.keys()), label_visibility="collapsed")
    load_preset = st.button("🚀 Carregar Perfil de Teste", use_container_width=True)

    if load_preset:
        selected_id = preset_options[selected_preset_title]
        st.session_state["active_role"] = selected_preset_title
        st.session_state["active_cv_text"] = PRESET_CV_TEXTS.get(selected_id, "")
        st.session_state["active_preset_id"] = selected_id
        st.toast(f"Perfil '{selected_preset_title}' carregado!", icon="✅")

    st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)

    # Stats WEF
    st.markdown("**📊 Projeções WEF 2030**")
    macro_stats = researcher_agent.get_macro_stats()

    st.markdown(f"""
    <div style="background:#FFF8F0; border-radius:10px; padding:0.8rem 1rem; margin-bottom:0.5rem; border-left:4px solid #F7AF20;">
        <div style="font-size:0.75rem; color:#6B7280; font-weight:600; text-transform:uppercase;">Criação Líquida de Empregos</div>
        <div style="font-size:1.1rem; font-weight:800; color:#780D34;">{macro_stats.get('net_job_creation', '+78M')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#FFF0F5; border-radius:10px; padding:0.8rem 1rem; margin-bottom:0.5rem; border-left:4px solid #CB1D4E;">
        <div style="font-size:0.75rem; color:#6B7280; font-weight:600; text-transform:uppercase;">Impacto nas Habilidades</div>
        <div style="font-size:0.95rem; font-weight:700; color:#780D34;">{macro_stats.get('skills_disrupted', '39% habilidades transformadas')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Fontes: WEF Future of Jobs Report 2025/2030 & McKinsey Global Institute.")

    st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)

    # SEÇÃO 5 — HISTÓRICO DE ANÁLISES (Sidebar)
    st.markdown("**🕐 Histórico de Análises**")
    history = st.session_state.get('analysis_history', [])

    if not history:
        st.markdown('<span style="font-size:0.8rem; color:#9CA3AF;">Nenhuma análise realizada ainda.</span>', unsafe_allow_html=True)
    else:
        with st.expander(f"Ver histórico ({len(history)} análise{'s' if len(history) > 1 else ''})", expanded=False):
            for i, item in enumerate(reversed(history)):
                hist_class = get_history_class(item.get('risk_level', ''))
                risk_color = get_risk_color(item.get('risk', 0))
                st.markdown(f"""
                <div class="history-item {hist_class}">
                    <div style="font-weight:700; color:#1F2937; font-size:0.82rem;">#{len(history)-i} {item.get('role', 'N/A')}</div>
                    <div style="color:#6B7280; font-size:0.75rem;">{item.get('timestamp', '')}</div>
                    <div style="margin-top:0.3rem;">
                        <span style="color:{risk_color}; font-weight:700; font-size:0.8rem;">⚠ {item.get('risk', 0)}% risco</span>
                        <span style="color:#951165; font-weight:700; font-size:0.8rem; margin-left:0.5rem;">↑ +{item.get('augmentation', 0)}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if st.button("🗑️ Limpar Histórico", use_container_width=True):
            st.session_state['analysis_history'] = []
            st.rerun()

    st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)
    st.caption("Desenvolvido conforme `agentes_universais.md` com arquitetura multiagente.")


# ─────────────────────────────────────────────────────────
# CABEÇALHO PRINCIPAL
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <span class="badge-wef">📡 Estudo Projetivo 2026 – 2030</span>
    <h1 style="margin: 0.5rem 0 0 0; font-size: 2.4rem; font-weight: 800; color: white; line-height: 1.2;">
        Carreira Inteligente: Seu Perfil no Mercado de IA
    </h1>
    <p style="margin-top: 0.8rem; font-size: 1.05rem; color: rgba(255,255,255,0.85); max-width: 820px; line-height: 1.6;">
        Avalie seu currículo com <strong>5 agentes inteligentes especializados</strong>. Descubra sua taxa de risco de automação,
        seu potencial de aumento de produtividade e o que você precisa aprender até 2030 para se manter indispensável.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# ABAS DE ENTRADA (incluindo Comparador)
# ─────────────────────────────────────────────────────────
tab_upload, tab_manual, tab_paste, tab_compare = st.tabs([
    "📄 Enviar Currículo (PDF/TXT)",
    "✍️ Preenchimento Guiado",
    "📋 Colar Texto / LinkedIn",
    "⚖️ Comparar 2 Carreiras"
])

cv_text_input = ""
selected_role = st.session_state.get("active_role", "")
experience_years = 3

# ── Tab Upload ──
with tab_upload:
    uploaded_file = st.file_uploader(
        "Faça upload do seu currículo em PDF ou TXT:",
        type=["pdf", "txt"]
    )
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            with st.spinner("Lendo arquivo PDF..."):
                cv_text_input = parser_agent.extract_text_from_pdf(uploaded_file.getvalue())
        else:
            cv_text_input = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        st.success(f"✅ Arquivo **'{uploaded_file.name}'** carregado — {len(cv_text_input)} caracteres lidos!")

# ── Tab Manual ──
with tab_manual:
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        manual_role = st.text_input(
            "Qual o seu cargo ou profissão?",
            value=selected_role,
            placeholder="Ex: Nutricionista, Engenheiro Civil, Psicólogo, Vendedor, Contador..."
        )
    with col_m2:
        manual_exp = st.slider("Anos de experiência profissional:", 0, 30, 3)

    manual_tasks = st.text_area(
        "Quais são suas principais atividades e rotinas diárias no trabalho?",
        placeholder="Ex: Preencho planilhas diárias, reviso contratos padrão, atendo clientes pelo chat, escrevo código de telas...",
        height=120
    )
    manual_skills = st.text_input(
        "Quais ferramentas e habilidades você mais utiliza?",
        placeholder="Ex: Excel, Python, Figma, React, Negociação, Gestão de Projetos..."
    )

    if st.button("💾 Usar dados do formulário", type="secondary"):
        cv_text_input = (
            f"Cargo: {manual_role}\n"
            f"Experiência: {manual_exp} anos\n"
            f"Atividades diárias: {manual_tasks}\n"
            f"Habilidades: {manual_skills}"
        )
        selected_role = manual_role
        experience_years = manual_exp
        st.info("✅ Dados do formulário prontos para avaliação. Clique em 'Executar Diagnóstico' abaixo.")

# ── Tab Colar Texto ──
with tab_paste:
    default_text = st.session_state.get("active_cv_text", "")
    pasted_text = st.text_area(
        "Cole aqui o texto do seu currículo ou perfil do LinkedIn:",
        value=default_text,
        height=200,
        placeholder="Cole o texto aqui — pode ser cópia do LinkedIn, Word ou qualquer descrição de cargo..."
    )
    if pasted_text:
        cv_text_input = pasted_text


# ─────────────────────────────────────────────────────────
# SEÇÃO 3 — COMPARADOR DE 2 CARREIRAS
# ─────────────────────────────────────────────────────────
with tab_compare:
    st.markdown("""
    <div class="section-card section-card-pink" style="margin-bottom:1.2rem;">
        <h3 style="margin:0 0 0.5rem 0; color:#951165;">⚖️ Comparador de Carreiras</h3>
        <p style="margin:0; color:#6B7280; font-size:0.9rem;">
            Compare dois perfis profissionais lado a lado e visualize as diferenças de risco, potencial de aumento e composição de tarefas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_perfil_a, col_perfil_b = st.columns(2)

    with col_perfil_a:
        st.markdown('<div class="compare-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Perfil A", help="Primeiro perfil para comparação")
        comp_role_a = st.text_input("Cargo / Profissão (A):", placeholder="Ex: Analista Financeiro", key="comp_role_a")
        comp_exp_a = st.slider("Anos de experiência (A):", 0, 30, 3, key="comp_exp_a")
        comp_text_a = st.text_area(
            "Descreva as atividades e habilidades (A):",
            height=150,
            placeholder="Ex: Consolido relatórios financeiros em Excel, análise de desvios...",
            key="comp_text_a"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_perfil_b:
        st.markdown('<div class="compare-card compare-card-b">', unsafe_allow_html=True)
        st.markdown("#### 👤 Perfil B", help="Segundo perfil para comparação")
        comp_role_b = st.text_input("Cargo / Profissão (B):", placeholder="Ex: Tech Lead / Arquiteta de Software", key="comp_role_b")
        comp_exp_b = st.slider("Anos de experiência (B):", 0, 30, 5, key="comp_exp_b")
        comp_text_b = st.text_area(
            "Descreva as atividades e habilidades (B):",
            height=150,
            placeholder="Ex: Defino arquitetura de microsserviços, mentoria de equipes...",
            key="comp_text_b"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    run_comparison = st.button(
        "⚖️ COMPARAR CARREIRAS",
        type="primary",
        use_container_width=True,
        key="btn_compare"
    )

    if run_comparison:
        if not comp_text_a.strip() and not comp_role_a.strip():
            st.error("Por favor, preencha ao menos o Perfil A para comparar.")
        elif not comp_text_b.strip() and not comp_role_b.strip():
            st.error("Por favor, preencha ao menos o Perfil B para comparar.")
        else:
            st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)
            st.subheader("📊 Resultados da Comparação")

            col_prog_a, col_prog_b = st.columns(2)

            with col_prog_a:
                with st.spinner(f"Analisando Perfil A: {comp_role_a or 'Perfil A'}..."):
                    cv_a = comp_text_a if comp_text_a.strip() else f"Cargo: {comp_role_a}\nExperiência: {comp_exp_a} anos"
                    san_a, _ = security_agent.audit_and_sanitize(cv_a)
                    parsed_a = parser_agent.parse_profile(san_a, manual_role=comp_role_a, manual_experience_years=comp_exp_a)
                    bench_a = researcher_agent.match_occupation(
                        role=parsed_a['role'], domain=parsed_a.get('domain', ''), cv_text=san_a
                    )
                    eval_a = evaluator_agent.evaluate_profile(parsed_a, bench_a)
                st.success(f"✅ Perfil A analisado: **{parsed_a['role']}**")

            with col_prog_b:
                with st.spinner(f"Analisando Perfil B: {comp_role_b or 'Perfil B'}..."):
                    cv_b = comp_text_b if comp_text_b.strip() else f"Cargo: {comp_role_b}\nExperiência: {comp_exp_b} anos"
                    san_b, _ = security_agent.audit_and_sanitize(cv_b)
                    parsed_b = parser_agent.parse_profile(san_b, manual_role=comp_role_b, manual_experience_years=comp_exp_b)
                    bench_b = researcher_agent.match_occupation(
                        role=parsed_b['role'], domain=parsed_b.get('domain', ''), cv_text=san_b
                    )
                    eval_b = evaluator_agent.evaluate_profile(parsed_b, bench_b)
                st.success(f"✅ Perfil B analisado: **{parsed_b['role']}**")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Tabela Comparativa ──
            st.markdown("#### 📋 Tabela Comparativa")
            col_tab_a, col_tab_b = st.columns(2)

            def render_compare_metric(label, val_a, val_b, format_a="", format_b=""):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label=label + " (A)", value=f"{val_a}{format_a}")
                with col2:
                    st.metric(label=label + " (B)", value=f"{val_b}{format_b}")

            risk_a = eval_a['final_automation_risk']
            risk_b = eval_b['final_automation_risk']
            aug_a = eval_a['final_augmentation_potential']
            aug_b = eval_b['final_augmentation_potential']
            routine_a = parsed_a['routine_tasks_ratio']
            routine_b = parsed_b['routine_tasks_ratio']
            strat_a = parsed_a['strategic_tasks_ratio']
            strat_b = parsed_b['strategic_tasks_ratio']

            col_c1, col_c2, col_c3, col_c4 = st.columns(4)
            with col_c1:
                st.markdown(f"""
                <div class="metric-card metric-card-danger" style="margin-bottom:0.5rem;">
                    <div class="metric-label">Risco Automação A</div>
                    <div class="metric-value" style="color:#D83C15;">{risk_a}%</div>
                    <div class="metric-sub" style="color:#D83C15;">{eval_a['risk_level']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_c2:
                st.markdown(f"""
                <div class="metric-card metric-card-danger" style="margin-bottom:0.5rem;">
                    <div class="metric-label">Risco Automação B</div>
                    <div class="metric-value" style="color:#CB1D4E;">{risk_b}%</div>
                    <div class="metric-sub" style="color:#CB1D4E;">{eval_b['risk_level']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_c3:
                st.markdown(f"""
                <div class="metric-card metric-card-info" style="margin-bottom:0.5rem;">
                    <div class="metric-label">Potencial Aumento A</div>
                    <div class="metric-value" style="color:#E6228C;">+{aug_a}%</div>
                    <div class="metric-sub" style="color:#E6228C;">{eval_a.get('productivity_multiplier','N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_c4:
                st.markdown(f"""
                <div class="metric-card metric-card-info" style="margin-bottom:0.5rem;">
                    <div class="metric-label">Potencial Aumento B</div>
                    <div class="metric-value" style="color:#951165;">+{aug_b}%</div>
                    <div class="metric-sub" style="color:#951165;">{eval_b.get('productivity_multiplier','N/A')}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Gráfico de Barras Comparativo ──
            st.markdown("#### 📊 Gráfico Comparativo de Indicadores")
            col_bar, col_radar_comp = st.columns(2)

            with col_bar:
                label_a = parsed_a['role'][:22] + "..." if len(parsed_a['role']) > 25 else parsed_a['role']
                label_b = parsed_b['role'][:22] + "..." if len(parsed_b['role']) > 25 else parsed_b['role']

                fig_bar = go.Figure()
                categories = ["Risco de Automação (%)", "Potencial de Aumento (%)", "Tarefas Repetitivas (%)", "Tarefas Cognitivas (%)"]
                vals_a = [risk_a, aug_a, routine_a, strat_a]
                vals_b = [risk_b, aug_b, routine_b, strat_b]

                fig_bar.add_trace(go.Bar(
                    name=f"A: {label_a}",
                    x=categories,
                    y=vals_a,
                    marker_color="#F7AF20",
                    marker_line_color="#E07618",
                    marker_line_width=1.5,
                    text=vals_a,
                    textposition='outside'
                ))
                fig_bar.add_trace(go.Bar(
                    name=f"B: {label_b}",
                    x=categories,
                    y=vals_b,
                    marker_color="#E6228C",
                    marker_line_color="#951165",
                    marker_line_width=1.5,
                    text=vals_b,
                    textposition='outside'
                ))

                fig_bar.update_layout(
                    barmode='group',
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="#FAFAFA",
                    margin=dict(l=20, r=20, t=30, b=60),
                    height=340,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
                    yaxis=dict(range=[0, 110], gridcolor="#F0F0F0"),
                    xaxis=dict(tickfont=dict(size=10))
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            # ── Radar Chart Comparativo ──
            with col_radar_comp:
                keys_r = list(eval_a["radar_labels"].keys())
                labels_r = list(eval_a["radar_labels"].values())
                curr_a_vals = [eval_a["radar_current"].get(k, 5) for k in keys_r]
                curr_b_vals = [eval_b["radar_current"].get(k, 5) for k in keys_r]

                labels_cycle_r = labels_r + [labels_r[0]]
                curr_a_cycle = curr_a_vals + [curr_a_vals[0]]
                curr_b_cycle = curr_b_vals + [curr_b_vals[0]]

                fig_rad = go.Figure()
                fig_rad.add_trace(go.Scatterpolar(
                    r=curr_a_cycle,
                    theta=labels_cycle_r,
                    fill='toself',
                    name=f"A: {label_a}",
                    line=dict(color='#F7AF20', width=2.5),
                    fillcolor='rgba(247, 175, 32, 0.2)'
                ))
                fig_rad.add_trace(go.Scatterpolar(
                    r=curr_b_cycle,
                    theta=labels_cycle_r,
                    fill='toself',
                    name=f"B: {label_b}",
                    line=dict(color='#E6228C', width=2.5),
                    fillcolor='rgba(230, 34, 140, 0.2)'
                ))
                fig_rad.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=9)),
                        angularaxis=dict(tickfont=dict(size=10))
                    ),
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                    margin=dict(l=30, r=30, t=20, b=50),
                    height=340,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_rad, use_container_width=True)

            # ── Tabela de Detalhes ──
            st.markdown("#### 🗂️ Detalhes por Perfil")
            col_det_a, col_det_b = st.columns(2)
            with col_det_a:
                st.markdown(f"""
                <div class="section-card" style="border-left-color:#F7AF20;">
                    <strong>👤 Perfil A — {parsed_a['role']}</strong><br>
                    <span style="font-size:0.85rem; color:#6B7280;">
                        Senioridade: <strong>{parsed_a['seniority']}</strong><br>
                        Experiência: <strong>{comp_exp_a} anos</strong><br>
                        Rotina: <strong>{routine_a}% repetitiva / {strat_a}% cognitiva</strong>
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with col_det_b:
                st.markdown(f"""
                <div class="section-card section-card-pink" style="border-left-color:#E6228C;">
                    <strong>👤 Perfil B — {parsed_b['role']}</strong><br>
                    <span style="font-size:0.85rem; color:#6B7280;">
                        Senioridade: <strong>{parsed_b['seniority']}</strong><br>
                        Experiência: <strong>{comp_exp_b} anos</strong><br>
                        Rotina: <strong>{routine_b}% repetitiva / {strat_b}% cognitiva</strong>
                    </span>
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# BOTÃO PRINCIPAL DE DIAGNÓSTICO
# ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
run_evaluation = st.button(
    "🔍 EXECUTAR DIAGNÓSTICO AGÊNTICO 2030",
    type="primary",
    use_container_width=True,
    key="btn_main_eval"
)


# ─────────────────────────────────────────────────────────
# PROCESSAMENTO AGÊNTICO PRINCIPAL
# ─────────────────────────────────────────────────────────
if run_evaluation:
    if not cv_text_input.strip() and not selected_role.strip():
        st.error("⚠️ Por favor, digite sua profissão, envie um currículo ou selecione um perfil de teste!")
    else:
        st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)
        st.subheader("🤖 Pipeline Multiagente em Execução")

        parsed_profile, benchmark, evaluation, strategy = run_full_pipeline(
            cv_text=cv_text_input,
            role=selected_role,
            exp_years=experience_years
        )

        # ── SEÇÃO 5 — Salvar no histórico ──
        st.session_state['analysis_history'].append({
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'role': parsed_profile['role'],
            'risk': evaluation['final_automation_risk'],
            'augmentation': evaluation['final_augmentation_potential'],
            'risk_level': evaluation['risk_level']
        })

        # Salvar últimos resultados
        st.session_state['last_results'] = {
            'parsed_profile': parsed_profile,
            'benchmark': benchmark,
            'evaluation': evaluation,
            'strategy': strategy
        }

        # ─────────────────────────────────────────────────────────
        # SEÇÃO 6 — DASHBOARD DE RESULTADOS REFORMULADO
        # ─────────────────────────────────────────────────────────
        st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)
        st.subheader("📈 Diagnóstico Executivo de Carreira — Horizonte 2030")

        # ── Resumo Executivo ──
        risk_val = evaluation['final_automation_risk']
        aug_val = evaluation['final_augmentation_potential']
        risk_lvl = evaluation['risk_level']
        risk_badge_html = get_risk_badge(risk_lvl)
        risk_color_hex = get_risk_color(risk_val)

        st.markdown(f"""
        <div class="exec-summary">
            <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem; flex-wrap:wrap;">
                <span style="font-size:1.1rem; font-weight:800; color:#780D34;">🧠 Resumo Executivo</span>
                {risk_badge_html}
            </div>
            <p style="margin:0; color:#374151; font-size:0.95rem; line-height:1.7;">
                O perfil <strong>{parsed_profile['role']}</strong> (nível <strong>{parsed_profile['seniority']}</strong>)
                apresenta <strong style="color:{risk_color_hex};">{risk_val}% de risco de automação</strong> de suas tarefas
                rotineiras até 2030, classificado como <strong>{risk_lvl}</strong>.
                Ao adotar ferramentas de IA como copiloto, o potencial de aumento de produtividade
                é de <strong style="color:#951165;">+{aug_val}%</strong>.
                A composição atual é de <strong>{parsed_profile['routine_tasks_ratio']}% tarefas repetitivas</strong>
                e <strong>{parsed_profile['strategic_tasks_ratio']}% tarefas cognitivas/estratégicas</strong>.
                O roadmap 2026–2030 aborda {len(strategy['roadmap'])} fases de requalificação com
                {len(strategy['career_pivots'])} possibilidades de transição de carreira.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── 3 Cartões de Métricas ──
        col_m1, col_m2, col_m3 = st.columns(3)

        card_risk_class = "metric-card-danger" if risk_val >= 70 else ("metric-card-warning" if risk_val >= 45 else "metric-card-success")

        with col_m1:
            st.markdown(f"""
            <div class="metric-card {card_risk_class}">
                <div class="metric-label">Risco de Automação de Rotinas</div>
                <div class="metric-value" style="color:{risk_color_hex};">{risk_val}%</div>
                <div>{risk_badge_html}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_m2:
            st.markdown(f"""
            <div class="metric-card metric-card-info">
                <div class="metric-label">Potencial de Aumento (Copiloto)</div>
                <div class="metric-value" style="color:#E6228C;">+{aug_val}%</div>
                <div class="metric-sub" style="color:#951165;">Multiplicador: {evaluation['productivity_multiplier']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_m3:
            routine_r = parsed_profile['routine_tasks_ratio']
            strat_r = parsed_profile['strategic_tasks_ratio']
            routine_status = "Crítico (Alta Rotina) ⚠️" if routine_r > 60 else "Equilibrado / Estratégico ✅"
            st.markdown(f"""
            <div class="metric-card metric-card-purple">
                <div class="metric-label">Composição da Sua Rotina</div>
                <div class="metric-value" style="color:#951165;">{routine_r}% / {strat_r}%</div>
                <div class="metric-sub" style="color:#780D34;">Repetitiva vs. Cognitiva</div>
                <div style="font-size:0.78rem; color:#6B7280; margin-top:0.3rem;">{routine_status}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Barras de Progresso Visual (antes do Radar) ──
        st.markdown("#### 📊 Barras de Competência — Perfil Atual vs. Meta 2030")

        keys_prog = list(evaluation["radar_labels"].keys())
        labels_prog = list(evaluation["radar_labels"].values())

        cols_prog = st.columns(2)
        for i, (k, lbl) in enumerate(zip(keys_prog, labels_prog)):
            curr = evaluation["radar_current"].get(k, 5)
            ideal = evaluation["radar_ideal"].get(k, 8)
            gap = ideal - curr
            col_idx = i % 2
            with cols_prog[col_idx]:
                bar_color = "#D83C15" if gap >= 4 else ("#E07618" if gap >= 2 else "#2E7D32")
                st.markdown(f"""
                <div style="margin-bottom:0.8rem;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
                        <span style="font-size:0.82rem; font-weight:600; color:#374151;">{lbl}</span>
                        <span style="font-size:0.78rem; color:{bar_color}; font-weight:700;">{curr}/10 → Meta: {ideal}/10</span>
                    </div>
                    <div style="background:#F3F4F6; border-radius:9999px; height:8px; overflow:hidden;">
                        <div style="height:8px; width:{curr*10}%; background:linear-gradient(90deg,#951165,#E6228C); border-radius:9999px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Gráfico Radar de Competências ──
        st.subheader("🎯 Radar de Competências: Perfil Atual vs. Exigência WEF 2030")
        col_radar, col_gaps = st.columns([3, 2])

        with col_radar:
            labels_r2 = list(evaluation["radar_labels"].values())
            keys_r2 = list(evaluation["radar_labels"].keys())
            ideal_vals = [evaluation["radar_ideal"].get(k, 8) for k in keys_r2]
            current_vals = [evaluation["radar_current"].get(k, 5) for k in keys_r2]

            labels_cycle2 = labels_r2 + [labels_r2[0]]
            ideal_cycle2 = ideal_vals + [ideal_vals[0]]
            current_cycle2 = current_vals + [current_vals[0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=ideal_cycle2,
                theta=labels_cycle2,
                fill='toself',
                name='Exigência de Mercado 2030 (WEF)',
                line=dict(color='#F7AF20', width=2.5),
                fillcolor='rgba(247, 175, 32, 0.15)'
            ))
            fig.add_trace(go.Scatterpolar(
                r=current_cycle2,
                theta=labels_cycle2,
                fill='toself',
                name='Diagnóstico do Perfil Atual',
                line=dict(color='#E6228C', width=2.5),
                fillcolor='rgba(230, 34, 140, 0.2)'
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10],
                        tickfont=dict(size=10, color="#9CA3AF"),
                        gridcolor="#F0F0F0"
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=11, color="#374151")
                    ),
                    bgcolor="rgba(0,0,0,0)"
                ),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
                margin=dict(l=40, r=40, t=20, b=60),
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_gaps:
            st.markdown("""
            <div class="section-card section-card-red" style="margin-bottom:1rem;">
                <h4 style="margin:0 0 0.7rem 0; color:#D83C15;">🚨 Gaps Críticos de Competência</h4>
            """, unsafe_allow_html=True)
            if evaluation["critical_gaps"]:
                for gap in evaluation["critical_gaps"]:
                    st.error(
                        f"**{gap['skill']}** — Gap: -{gap['gap']} pts\n"
                        f"*Atual: {gap['current']}/10 → Meta: {gap['ideal']}/10*"
                    )
            else:
                st.success("✅ Nenhum gap crítico! Seu perfil demonstra bom equilíbrio.")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="section-card" style="border-left-color:#2E7D32; margin-top:0.5rem;">
                <h4 style="margin:0 0 0.7rem 0; color:#2E7D32;">🛡️ Fortalezas Diagnosticadas</h4>
            """, unsafe_allow_html=True)
            if evaluation["strong_pillars"]:
                for strong in evaluation["strong_pillars"]:
                    st.success(f"**{strong['skill']}** — Score: {strong['score']}/10")
            else:
                st.info("Fortalezas em desenvolvimento. Invista nas habilidades emergentes!")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)

        # ── Auditoria de Tarefas ──
        st.subheader("📋 Auditoria de Tarefas: Onde a IA Afeta Sua Rotina")
        col_t1, col_t2, col_t3 = st.columns(3)

        with col_t1:
            st.markdown("""
            <div class="task-box task-threatened">
                <h4 style="color:#D83C15; margin:0 0 0.5rem 0;">⚠️ Ameaçadas até 2028</h4>
                <p style="font-size:0.82rem; color:#6B7280; margin-bottom:0.8rem;">Alta probabilidade de automação por agentes de IA e modelos generativos:</p>
            """, unsafe_allow_html=True)
            for t in benchmark.get("declining_tasks", []):
                st.markdown(f"- <span style='font-size:0.88rem; color:#374151;'>{t}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_t2:
            st.markdown("""
            <div class="task-box task-augmented">
                <h4 style="color:#E07618; margin:0 0 0.5rem 0;">⚡ Tarefas Copiloto (Híbridas)</h4>
                <p style="font-size:0.82rem; color:#6B7280; margin-bottom:0.8rem;">A IA atua como acelerador de produtividade supervisionado por você:</p>
            """, unsafe_allow_html=True)
            for t in benchmark.get("augmented_tasks", []):
                st.markdown(f"- <span style='font-size:0.88rem; color:#374151;'>{t}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_t3:
            st.markdown("""
            <div class="task-box task-human">
                <h4 style="color:#2E7D32; margin:0 0 0.5rem 0;">🛡️ Fortalezas 100% Humanas</h4>
                <p style="font-size:0.82rem; color:#6B7280; margin-bottom:0.8rem;">Exigem empatia, julgamento ético, negociação e visão de negócio:</p>
            """, unsafe_allow_html=True)
            for t in benchmark.get("human_core_tasks", []):
                st.markdown(f"- <span style='font-size:0.88rem; color:#374151;'>{t}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Matriz de Habilidades ──
        st.subheader("⚖️ Matriz de Habilidades: O Que Desaprender vs. O Que Aprender")
        col_h1, col_h2 = st.columns(2)

        with col_h1:
            st.markdown("""
            <div class="section-card section-card-red">
                <h4 style="margin:0 0 0.8rem 0; color:#D83C15;">📉 Parar de investir tempo (Em Declínio):</h4>
            """, unsafe_allow_html=True)
            for sk in strategy["declining_skills"]:
                st.markdown(
                    f'<span class="skill-pill skill-pill-decline">❌ {sk}</span>',
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_h2:
            st.markdown("""
            <div class="section-card section-card-purple">
                <h4 style="margin:0 0 0.8rem 0; color:#951165;">📈 Desenvolver com urgência (Essenciais até 2030):</h4>
            """, unsafe_allow_html=True)
            for sk in strategy["emerging_skills"]:
                st.markdown(
                    f'<span class="skill-pill skill-pill-grow">✅ {sk}</span>',
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)

        # ── Roadmap de Requalificação ──
        st.subheader("🗺️ Roadmap Anual de Requalificação (2026 – 2030)")

        phase_colors = ["#F7AF20", "#E07618", "#D83C15", "#CB1D4E", "#951165"]
        for i, phase in enumerate(strategy["roadmap"]):
            color = phase_colors[i % len(phase_colors)]
            with st.expander(
                f"📍 **{phase['period']}: {phase['theme']}** — Foco: {phase['focus']}",
                expanded=(i == 0)
            ):
                st.markdown(f"""
                <div style="border-left:4px solid {color}; padding-left:1rem;">
                    <div style="margin-bottom:0.5rem;"><strong style="color:{color};">🎯 Meta Principal:</strong> {phase['goal']}</div>
                    <div style="margin-bottom:0.5rem;"><strong style="color:{color};">⚡ Ação Prática:</strong> {phase['action']}</div>
                    <div><strong style="color:{color};">🛠️ Ferramentas Chave:</strong>
                """, unsafe_allow_html=True)
                tools_html = " ".join([
                    f'<code style="background:#F3F4F6; color:#374151; padding:0.2rem 0.5rem; border-radius:6px; font-size:0.82rem;">{tool}</code>'
                    for tool in phase['key_tools']
                ])
                st.markdown(tools_html + "</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Transições & Certificações ──
        col_pivots, col_certs = st.columns(2)

        with col_pivots:
            st.markdown("""
            <div class="section-card section-card-orange">
                <h3 style="margin:0 0 0.8rem 0; color:#E07618;">🔀 Transições de Carreira Recomendadas</h3>
                <p style="margin:0 0 1rem 0; color:#6B7280; font-size:0.88rem;">
                    Se sua função estiver sob alto risco, estas são as áreas correlatas de maior crescimento até 2030:
                </p>
            """, unsafe_allow_html=True)
            for pivot in strategy["career_pivots"]:
                st.info(f"🚀 **{pivot}**")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_certs:
            st.markdown("""
            <div class="section-card section-card-pink">
                <h3 style="margin:0 0 0.8rem 0; color:#E6228C;">🎓 Certificações Recomendadas</h3>
                <p style="margin:0 0 1rem 0; color:#6B7280; font-size:0.88rem;">
                    Qualificações de prestígio global para validar seu perfil profissional:
                </p>
            """, unsafe_allow_html=True)
            for cert in strategy["recommended_certifications"]:
                st.success(f"📜 {cert}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)

        # ── SEÇÃO 4 — Exportação (Markdown + PDF) ──
        st.subheader("📥 Exportar Relatório Executivo")

        dossier_content = strategist_agent.generate_markdown_dossier(
            parsed_profile, benchmark, evaluation, strategy
        )

        col_exp1, col_exp2 = st.columns(2)

        with col_exp1:
            st.download_button(
                label="📄 Baixar Dossiê em Markdown (.md)",
                data=dossier_content,
                file_name=f"Dossie_Carreira_2030_{parsed_profile['role'].replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col_exp2:
            if FPDF_AVAILABLE:
                with st.spinner("Gerando PDF..."):
                    try:
                        pdf_bytes = generate_pdf_report(parsed_profile, benchmark, evaluation, strategy)
                        st.download_button(
                            label="📥 Exportar Relatório em PDF",
                            data=pdf_bytes,
                            file_name=f"Dossie_Carreira_2030_{parsed_profile['role'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.warning(f"Não foi possível gerar o PDF: {e}")
            else:
                st.warning(
                    "⚠️ A biblioteca `fpdf2` não está instalada. "
                    "Execute `pip install fpdf2>=2.7.0` para habilitar a exportação PDF.",
                    icon="⚠️"
                )


# ─────────────────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="color-sep"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:1rem 0 0.5rem 0;">
    <span style="font-size:0.8rem; color:#9CA3AF;">
        CarreiraIA 2030 — Desenvolvido conforme
        <code>agentes_universais.md</code> com arquitetura multiagente.
        Dados: <strong>WEF Future of Jobs Report 2025/2030</strong> & <strong>McKinsey Global Institute</strong>.
    </span>
</div>
""", unsafe_allow_html=True)
