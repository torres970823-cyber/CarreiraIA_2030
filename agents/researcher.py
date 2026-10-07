"""
Agente Pesquisador de Mercado e Tendências 2030 (ResearcherAgent)
Mapeamento estrito Like-for-Like e projeções 2030 por indústria.
"""

import json
import os
import re
from typing import Dict, Any, List, Optional


class ResearcherAgent:
    def __init__(self, data_path: Optional[str] = None):
        self.name = "ResearcherAgent"
        self.role = "Especialista em Tendências 2030 do Fórum Econômico Mundial (WEF) e McKinsey"
        
        if not data_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "wef_benchmark_2030.json")

        self.data_path = data_path
        self.benchmark_data = self._load_data()

        # Benchmarks Setoriais Nativos 2030 (Zero Contaminação)
        self.specialized_benchmarks_2030 = {
            "Economia, Finanças & Investimentos": {
                "category": "Economia, Finanças & Mercado de Capitais",
                "risk": 42,
                "augmentation": 94,
                "skills_radar_ideal": { "pensamento_analitico": 10, "orquestracao_ia": 9, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 10 },
                "declining_tasks": [
                    "Coleta manual e consolidação de planilhas de balanços e indicadores macroeconômicos",
                    "Cálculos manuais de regressões estatísticas básicas e projeções lineares simples",
                    "Elaboração mecânica de relatórios descritivos de fechamento contábil e orçamentário"
                ],
                "augmented_tasks": [
                    "Modelagem econométrica preditiva e backtesting automatizado com algoritmos de Machine Learning",
                    "Análise em tempo real de risco de ativos tokenizados e regulação de moedas digitais (CBDCs)",
                    "Orquestração de modelos de inteligência de mercado cruzando dados alternativos e métricas ESG"
                ],
                "human_core_tasks": [
                    "Julgamento de cenários geopolíticos e sensibilidade a choques macroeconômicos não lineares",
                    "Tomada de decisão fiduciária, governança de risco e responsabilidade executiva com clientes",
                    "Negociação estratégica e formulação de políticas econômicas ou teses de investimento proprietárias"
                ],
                "declining_skills": [
                    "Montagem manual de fórmulas em Excel sem automação",
                    "Análise estática retrospectiva sem modelagem preditiva"
                ],
                "emerging_skills_2030": [
                    "Modelagem Econométrica Aumentada por IA",
                    "Tokenização de Ativos & Infraestrutura de CBDCs",
                    "Análise de Risco Climático & Métricas ESG Algorítmicas",
                    "Storytelling Executivo & Tomada de Decisão sob Incerteza"
                ],
                "transition_pivots": [
                    "Economista Chefe de Estratégia de Ativos Digitais & IA",
                    "Diretor(a) de Inteligência de Risco & Modelagem Preditiva",
                    "Consultor(a) Sênior em Tokenização e Mercados de Carbono"
                ],
                "recommended_certifications": [
                    "AI in Financial Markets & Macroeconomic Forecasting (Oxford / MIT)",
                    "Digital Assets, CBDCs & Blockchain Economics (Wharton)",
                    "ESG Investing & Quantitative Risk Management (CFA Institute)"
                ],
                "recommended_tools_2030": [
                    "Copilotos Financeiros (BloombergGPT, FinChat AI)",
                    "Python/R para Econometria Preditiva & Análise de Dados",
                    "Plataformas de On-Chain Analytics & Tokenomics"
                ]
            },
            "Saúde, Medicina & Biociências": {
                "category": "Saúde, Medicina & Cuidados Clínicos",
                "risk": 28,
                "augmentation": 96,
                "skills_radar_ideal": { "pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 7, "lideranca_influencia": 9, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 10 },
                "declining_tasks": [
                    "Preenchimento burocrático de prontuários, formulários de convênio e fichas clínicas",
                    "Busca manual em tabelas de posologia e diretrizes de interação medicamentosa",
                    "Triagem mecânica inicial de sinais vitais básicos e transcrição de consultas"
                ],
                "augmented_tasks": [
                    "Apoio a diagnósticos complexos e triagem por visão computacional e IA multimodal",
                    "Uso de escribas médicos de voz inteligentes para registro automático de prontuário eletrônico",
                    "Medicina de precisão: cruzamento de biossensores contínuos com perfis genômicos do paciente"
                ],
                "human_core_tasks": [
                    "Empatia, escuta clínica aprofundada e construção de vínculo terapêutico de confiança",
                    "Decisões éticas críticas, bioética em terminalidade e casos clínicos de alta complexidade",
                    "Comunicação de diagnósticos delicados e engajamento comportamental do paciente no tratamento"
                ],
                "declining_skills": [
                    "Memorização passiva de bulas sem checagem automatizada",
                    "Atendimento médico transacional sem foco na experiência humana"
                ],
                "emerging_skills_2030": [
                    "Interpretação e Auditoria de Diagnósticos Gerados por IA",
                    "Telemedicina Avançada & Monitoramento Remoto por IoT",
                    "Medicina de Precisão, Genômica & Farmacogenética",
                    "Comunicação Clínica Empática & Bioética Digital"
                ],
                "transition_pivots": [
                    "Médico(a) Especialista em Saúde Digital & Telemedicina Avançada",
                    "Diretor(a) Clínico de Inovação e Medicina Personalizada",
                    "Consultor(a) de Inteligência Clínica e Auditoria Médica de Algoritmos"
                ],
                "recommended_certifications": [
                    "AI in Healthcare & Clinical Decision Support (Harvard Medical School)",
                    "Precision Medicine & Genomics (Stanford Online)",
                    "Liderança Clínica e Gestão da Experiência do Paciente"
                ],
                "recommended_tools_2030": [
                    "Escribas Médicos por IA (Nuance DAX, Nabla Copilot)",
                    "Sistemas de Apoio à Decisão Clínica (CDSS Multimodal)",
                    "Plataformas de Telemonitoramento e Prontuário Preditivo"
                ]
            },
            "Jurídico, Contratos & Compliance": {
                "category": "Direito, Regulação & Conformidade Empresarial",
                "risk": 55,
                "augmentation": 82,
                "skills_radar_ideal": { "pensamento_analitico": 10, "orquestracao_ia": 8, "criatividade_inovacao": 7, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 10 },
                "declining_tasks": [
                    "Revisão manual linha a linha de contratos padronizados e minutas de NDA sem inteligência semântica",
                    "Busca jurisprudencial não assistida em bases de dados legais e compilação de precedentes",
                    "Preenchimento repetitivo de petições de rotina, procurações e formulários administrativos"
                ],
                "augmented_tasks": [
                    "Análise automatizada de riscos contratuais com LLMs jurídicos (Harvey AI, Lexis+ AI)",
                    "Due diligence acelerada por IA em M&A, cruzando cláusulas contratuais com regulação vigente",
                    "Monitoramento contínuo de alterações regulatórias e impacto em políticas de compliance"
                ],
                "human_core_tasks": [
                    "Estratégia processual, argumentação jurídica criativa e persuasão perante tribunal",
                    "Aconselhamento ético em zonas cinzentas regulatórias e negociação de acordos complexos",
                    "Gestão de relacionamento com reguladores e construção de teses jurídicas inovadoras"
                ],
                "declining_skills": [
                    "Revisão manual de contratos sem suporte de ferramentas de NLP jurídico",
                    "Pesquisa jurisprudencial exclusivamente manual sem IA de recuperação semântica"
                ],
                "emerging_skills_2030": [
                    "Legal Tech & Orquestração de LLMs Jurídicos (Harvey AI, CoCounsel)",
                    "Compliance Regulatório Digital & Privacidade de Dados (LGPD/GDPR)",
                    "Arbitragem Internacional & Resolução Online de Disputas (ODR)",
                    "Análise de Risco Contratual por IA e Gestão de Contratos Inteligentes"
                ],
                "transition_pivots": [
                    "Especialista em Legal Tech & Automação de Contratos com IA",
                    "Diretor(a) de Compliance Digital & Privacidade de Dados",
                    "Árbitro(a) Especializado em Disputas de Tecnologia e Propriedade Intelectual Digital"
                ],
                "recommended_certifications": [
                    "Legal Tech & AI for Lawyers (Harvard Law School Executive Education)",
                    "Certified Information Privacy Professional — CIPP/E (IAPP)",
                    "Compliance & Ética Empresarial com Tecnologia (FGV Online)"
                ],
                "recommended_tools_2030": [
                    "Plataformas de IA Jurídica (Harvey AI, Lexis+ AI, CoCounsel)",
                    "Ferramentas de Gestão de Contratos Inteligentes (Ironclad, Juro)",
                    "Sistemas de Monitoramento Regulatório Automatizado (RegTech)"
                ]
            },
            "Design, Mídia & Comunicação": {
                "category": "Criatividade, Mídia & Comunicação Estratégica",
                "risk": 62,
                "augmentation": 78,
                "skills_radar_ideal": { "pensamento_analitico": 8, "orquestracao_ia": 9, "criatividade_inovacao": 10, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8 },
                "declining_tasks": [
                    "Produção manual de variações repetitivas de banners, thumbnails e peças estáticas padronizadas",
                    "Copywriting de baixa complexidade para descrições de produto, legendas e anúncios genéricos",
                    "Edição básica de vídeo sem narrativa estratégica: cortes simples, legendagem e ajuste de cor automático"
                ],
                "augmented_tasks": [
                    "Geração e curadoria de conceitos visuais com ferramentas generativas (Midjourney, Adobe Firefly, Sora)",
                    "Personalização massiva de campanhas multicanal usando IA de otimização criativa",
                    "Produção de narrativas audiovisuais com avatares digitais, voice cloning e síntese de vídeo por IA"
                ],
                "human_core_tasks": [
                    "Direção criativa estratégica, conceituação de marca e visão estética diferenciada",
                    "Construção de narrativas culturalmente relevantes e conexão emocional com audiências",
                    "Curadoria ética do conteúdo gerado por IA, garantindo autenticidade e responsabilidade de marca"
                ],
                "declining_skills": [
                    "Execução técnica repetitiva em ferramentas sem componente estratégico ou criativo",
                    "Produção de conteúdo genérico não personalizado sem análise de audiência"
                ],
                "emerging_skills_2030": [
                    "Direção Criativa de Conteúdo Gerado por IA (AIGC) & Prompt Design",
                    "Estratégia de Marca em Ambientes Imersivos (AR/VR/Metaverso)",
                    "Análise de Performance Criativa & Otimização por IA (Creative Intelligence)",
                    "Ética em Mídia Sintética & Governança de Desinformação Digital"
                ],
                "transition_pivots": [
                    "Diretor(a) Criativo de IA & Experiências Imersivas de Marca",
                    "Estrategista de Conteúdo Generativo & Creative Intelligence",
                    "Especialista em Brand Safety & Ética na Era da Mídia Sintética"
                ],
                "recommended_certifications": [
                    "AI-Powered Creative Strategy & Generative Design (IDEO / Coursera)",
                    "Brand Experience in the Metaverse & Immersive Media (Parsons School)",
                    "Creative Intelligence & Data-Driven Storytelling (Google / HubSpot)"
                ],
                "recommended_tools_2030": [
                    "Ferramentas de IA Generativa Visual (Midjourney, Adobe Firefly, Runway ML)",
                    "Plataformas de Creative Intelligence (Pencil AI, Smartly.io)",
                    "Ferramentas de Vídeo Sintético & Avatar Digital (HeyGen, Synthesia, Sora)"
                ]
            },
            "Engenharia, Construção & Manufatura": {
                "category": "Engenharia, Indústria & Infraestrutura Física",
                "risk": 38,
                "augmentation": 88,
                "skills_radar_ideal": { "pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 10 },
                "declining_tasks": [
                    "Elaboração manual de plantas e projetos 2D sem integração paramétrica ou BIM",
                    "Inspeção de campo por amostragem humana sem suporte de sensores IoT e visão computacional",
                    "Geração de cronogramas e orçamentos de obra baseados em memórias de cálculo sem automação"
                ],
                "augmented_tasks": [
                    "Projeto paramétrico e simulação estrutural acelerada por IA generativa em BIM e gêmeo digital",
                    "Monitoramento preditivo de falhas em ativos industriais com sensores IoT e modelos de manutenção preditiva",
                    "Otimização de cadeia de suprimentos e logística de materiais com algoritmos de roteirização inteligente"
                ],
                "human_core_tasks": [
                    "Tomada de decisão técnica em projetos de alta complexidade, risco estrutural e segurança crítica",
                    "Gestão de obra em campo: liderança de equipes multidisciplinares e resolução de imprevistos",
                    "Relação com clientes, stakeholders e órgãos reguladores em licenciamentos e aprovações"
                ],
                "declining_skills": [
                    "Desenho técnico manual e prancheta sem ferramentas CAD/BIM paramétrico",
                    "Controle de qualidade exclusivamente visual sem instrumentação e sensoriamento digital"
                ],
                "emerging_skills_2030": [
                    "BIM Avançado & Gêmeo Digital (Digital Twin) para Infraestrutura",
                    "Manutenção Preditiva & IoT Industrial (Indústria 4.0 / 5.0)",
                    "Sustentabilidade & Engenharia de Baixo Carbono (Construção Verde)",
                    "Gestão de Projetos Ágeis com Ferramentas de IA e Automação de Cronograma"
                ],
                "transition_pivots": [
                    "Especialista em Gêmeo Digital & Engenharia de Infraestrutura Inteligente",
                    "Gerente de Projetos de Construção Sustentável & Certificação LEED/WELL",
                    "Engenheiro(a) de Confiabilidade & Manutenção Preditiva Industrial (IoT)"
                ],
                "recommended_certifications": [
                    "BIM Professional & Digital Twin Engineering (Autodesk / buildingSMART)",
                    "Lean Construction & Gestão de Projetos de Alta Performance (PMI)",
                    "Engenharia de Sustentabilidade & Certificação LEED Green Associate"
                ],
                "recommended_tools_2030": [
                    "Plataformas BIM & Gêmeo Digital (Autodesk Revit, Bentley iTwin)",
                    "Sistemas de Manutenção Preditiva & IoT Industrial (IBM Maximo, PTC ThingWorx)",
                    "IA para Planejamento de Obras & Controle de Escopo (Buildots, Alice Technologies)"
                ]
            },
            "Tecnologia, Dados & Inteligência Artificial": {
                "category": "Tecnologia da Informação, Dados & IA",
                "risk": 22,
                "augmentation": 97,
                "skills_radar_ideal": { "pensamento_analitico": 10, "orquestracao_ia": 10, "criatividade_inovacao": 9, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 10, "especializacao_estrategica": 9 },
                "declining_tasks": [
                    "Escrita manual de código boilerplate repetitivo, testes unitários triviais e documentação básica de APIs",
                    "Configuração manual de ambientes de desenvolvimento e provisionamento de infraestrutura sem IaC",
                    "Geração de relatórios analíticos estáticos sem pipelines automatizados de dados em tempo real"
                ],
                "augmented_tasks": [
                    "Desenvolvimento acelerado de software com copilotos de código (GitHub Copilot, Cursor, Devin AI)",
                    "Orquestração de agentes de IA autônomos para automação de pipelines de dados e ML Ops",
                    "Arquitetura de sistemas de IA multimodal, RAG e LLMs fine-tuned para domínios específicos"
                ],
                "human_core_tasks": [
                    "Arquitetura de sistemas críticos, decisões de design de alto nível e trade-offs tecnológicos",
                    "Liderança técnica, mentoria de times e definição de cultura de engenharia e qualidade",
                    "Ética em IA, auditoria de modelos por viés e responsabilidade em sistemas de decisão autônoma"
                ],
                "declining_skills": [
                    "Codificação manual sem uso de copilotos de IA e ferramentas de geração assistida",
                    "Administração de infraestrutura on-premise sem automação cloud-native e IaC"
                ],
                "emerging_skills_2030": [
                    "Engenharia de Agentes de IA & Orquestração de LLMs (LangChain, AutoGen)",
                    "MLOps Avançado, LLMOps & Governança de Modelos de IA em Produção",
                    "Arquitetura de Dados em Tempo Real & Plataformas de Feature Store",
                    "Segurança em IA & Red Teaming de Sistemas de Linguagem de Grande Escala"
                ],
                "transition_pivots": [
                    "Engenheiro(a) de IA & Agentes Autônomos (AI Engineer)",
                    "Arquiteto(a) de Dados em Tempo Real & Plataformas de Decisão Inteligente",
                    "Líder Técnico(a) de MLOps & Governança Responsável de IA"
                ],
                "recommended_certifications": [
                    "Deep Learning Specialization & MLOps (DeepLearning.AI / Coursera)",
                    "AWS Certified Machine Learning Specialty ou Google Professional ML Engineer",
                    "AI Safety, Ethics & Governance (MIT Sloan / Partnership on AI)"
                ],
                "recommended_tools_2030": [
                    "Copilotos de Código com IA (GitHub Copilot, Cursor, Devin AI)",
                    "Frameworks de Agentes & LLMs (LangChain, LlamaIndex, AutoGen, CrewAI)",
                    "Plataformas de MLOps & LLMOps (MLflow, Weights & Biases, Vertex AI)"
                ]
            },
            "Vendas, Marketing & Expansão de Negócios": {
                "category": "Vendas Estratégicas, Marketing & Crescimento de Receita",
                "risk": 58,
                "augmentation": 85,
                "skills_radar_ideal": { "pensamento_analitico": 8, "orquestracao_ia": 9, "criatividade_inovacao": 9, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8 },
                "declining_tasks": [
                    "Prospecção fria manual via ligações não segmentadas e envio de e-mails em massa sem personalização",
                    "Geração de relatórios de vendas e dashboards de funil montados manualmente em planilhas",
                    "Segmentação de base de clientes por critérios estáticos sem modelos preditivos de propensão"
                ],
                "augmented_tasks": [
                    "Hiperpersonalização de jornadas de compra com IA preditiva e recomendação em tempo real",
                    "Uso de agentes de IA para qualificação de leads, follow-up automatizado e scoring preditivo",
                    "Otimização de campanhas multicanal com IA generativa e testes A/B acelerados por algoritmos"
                ],
                "human_core_tasks": [
                    "Negociação consultiva de alto valor, gestão de contas estratégicas e fechamento de contratos complexos",
                    "Construção de parcerias de ecossistema, alianças estratégicas e relações de confiança de longo prazo",
                    "Definição da estratégia go-to-market, posicionamento de marca e visão de expansão de mercado"
                ],
                "declining_skills": [
                    "Vendas transacionais de baixo valor sem diferenciação consultiva ou expertise de solução",
                    "Marketing baseado em intuição sem análise de dados, testes e otimização contínua"
                ],
                "emerging_skills_2030": [
                    "Revenue Intelligence & Sales AI (Gong, Clari, Salesforce Einstein)",
                    "Growth Hacking com IA & Product-Led Growth (PLG) Orientado a Dados",
                    "Vendas Consultivas de Alta Complexidade & Gestão de Stakeholders C-Level",
                    "Estratégia de Conteúdo Generativo & SEO Semântico para Demanda Orgânica"
                ],
                "transition_pivots": [
                    "Revenue Operations (RevOps) Lead com IA e Análise de Funil Preditivo",
                    "Diretor(a) de Growth & Expansão de Receita em Mercados Digitais",
                    "Consultor(a) de Estratégia Go-to-Market & Parcerias de Ecossistema"
                ],
                "recommended_certifications": [
                    "HubSpot Sales & Revenue Operations Certification (HubSpot Academy)",
                    "AI-Powered Marketing & Growth Strategy (Kellogg School / Northwestern)",
                    "Strategic Account Management & Executive Selling (Miller Heiman Group)"
                ],
                "recommended_tools_2030": [
                    "Plataformas de Revenue Intelligence (Gong, Clari, Chorus.ai)",
                    "CRMs com IA & Automação de Pipeline (Salesforce Einstein, HubSpot AI)",
                    "Ferramentas de IA para Geração de Demanda & Prospecção (Clay, Apollo, 6sense)"
                ]
            },
            "Educação, Formação & Pedagogia": {
                "category": "Educação, Desenvolvimento Humano & Aprendizagem",
                "risk": 30,
                "augmentation": 90,
                "skills_radar_ideal": { "pensamento_analitico": 8, "orquestracao_ia": 8, "criatividade_inovacao": 9, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8 },
                "declining_tasks": [
                    "Elaboração manual de provas, gabaritos e listas de exercícios repetitivas sem personalização adaptativa",
                    "Correção manual de redações e atividades de múltipla escolha sem suporte de ferramentas de avaliação",
                    "Transmissão expositiva unidirecional de conteúdo sem metodologias ativas ou personalização"
                ],
                "augmented_tasks": [
                    "Design de trilhas de aprendizagem adaptativas com IA, personalizando ritmo e nível por aluno",
                    "Uso de tutores de IA (Khanmigo, Socratic) para feedback imediato e scaffolding personalizado",
                    "Criação de simulações imersivas, jogos pedagógicos e cenários de realidade estendida (XR)"
                ],
                "human_core_tasks": [
                    "Mentoria profunda, escuta ativa e desenvolvimento socioemocional de estudantes",
                    "Facilitação de debates complexos, pensamento crítico coletivo e dinâmicas de grupo",
                    "Curadoria pedagógica estratégica e responsabilidade ética no design de experiências de aprendizagem"
                ],
                "declining_skills": [
                    "Aula expositiva tradicional sem integração de metodologias ativas ou tecnologias educacionais",
                    "Avaliação somativa exclusiva sem feedback formativo contínuo e análise de progresso"
                ],
                "emerging_skills_2030": [
                    "Learning Design com IA & Trilhas Adaptativas Personalizadas (Adaptive Learning)",
                    "Facilitação de Experiências Imersivas em XR & Gamificação Avançada",
                    "Avaliação Baseada em Competências & Análise de Aprendizagem (Learning Analytics)",
                    "Desenvolvimento Socioemocional & Mentoria de Alta Performance"
                ],
                "transition_pivots": [
                    "Designer Instrucional de Experiências de Aprendizagem com IA (Learning Experience Designer)",
                    "Especialista em Educação Imersiva & Realidade Estendida para Treinamento Corporativo",
                    "Analista de Aprendizagem & Especialista em Personalização Educacional com Dados"
                ],
                "recommended_certifications": [
                    "Learning Experience Design & AI in Education (MIT Media Lab / Coursera)",
                    "Gamification & Immersive Learning Design (Karl Kapp / ATD)",
                    "Learning Analytics & Data-Driven Education (edX / IMS Global)"
                ],
                "recommended_tools_2030": [
                    "Plataformas de Aprendizagem Adaptativa com IA (Khan Academy AI, Duolingo for Business)",
                    "Ferramentas de Design Instrucional & LXP (Articulate 360, Adobe Learning Manager)",
                    "Ambientes de Aprendizagem Imersiva (Prisms VR, Labster, Engage XR)"
                ]
            },
            "Gestão, Estratégia & Recursos Humanos": {
                "category": "Liderança Executiva, Estratégia Organizacional & Gestão de Pessoas",
                "risk": 35,
                "augmentation": 92,
                "skills_radar_ideal": { "pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9 },
                "declining_tasks": [
                    "Triagem manual de currículos e filtragem inicial de candidatos sem ATS inteligente",
                    "Elaboração de relatórios de clima e desempenho baseados em surveys manuais sem análise preditiva",
                    "Agendamento manual de entrevistas, onboarding burocrático e controle de ponto sem automação"
                ],
                "augmented_tasks": [
                    "Análise preditiva de turnover, engajamento e fit cultural com People Analytics e IA comportamental",
                    "Recrutamento com IA: triagem semântica, assessment automatizado e predição de sucesso por cargo",
                    "Planejamento estratégico de força de trabalho com cenários de automação e simulação de impacto por IA"
                ],
                "human_core_tasks": [
                    "Liderança transformacional, criação de cultura organizacional e desenvolvimento de talentos de alto potencial",
                    "Tomada de decisão estratégica em ambientes VUCA, gestão de mudança e alinhamento de stakeholders",
                    "Negociação de relações trabalhistas, resolução de conflitos complexos e promoção de equidade e inclusão"
                ],
                "declining_skills": [
                    "Gestão de pessoas baseada exclusivamente em intuição sem dados de People Analytics",
                    "Processos seletivos e de avaliação de desempenho não estruturados e sem métricas objetivas"
                ],
                "emerging_skills_2030": [
                    "People Analytics Avançado & Predição de Performance e Retenção com IA",
                    "Liderança de Times Híbridos Humano-IA & Orquestração de Agentes Autônomos",
                    "Design Organizacional Ágil & Gestão de Mudança em Transformações Digitais",
                    "Estratégia de Diversidade, Equidade & Inclusão (DEI) Orientada por Dados"
                ],
                "transition_pivots": [
                    "Chief People Officer (CPO) com Especialização em People Analytics & IA",
                    "Especialista em Transformação Organizacional & Gestão da Mudança Digital",
                    "Head of Workforce Strategy & Future of Work Planning"
                ],
                "recommended_certifications": [
                    "People Analytics & Workforce Intelligence (Wharton / SHRM)",
                    "Strategic HR Leadership & Organizational Design (INSEAD Executive Education)",
                    "Change Management Certification — PROSCI ADKAR ou Kotter"
                ],
                "recommended_tools_2030": [
                    "Plataformas de People Analytics & IA para RH (Visier, Eightfold AI, Workday AI)",
                    "ATS com IA Avançada & Assessment Preditivo (Greenhouse, Lever, HireVue)",
                    "Ferramentas de Gestão de Performance & OKRs (Lattice, 15Five, Betterworks)"
                ]
            }
        }

    def _load_data(self) -> Dict[str, Any]:
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"macro_stats_2030": {}, "occupations": []}

    def get_macro_stats(self) -> Dict[str, Any]:
        return self.benchmark_data.get("macro_stats_2030", {
            "source": "World Economic Forum - Future of Jobs Report 2025/2030",
            "net_job_creation": "+78 milhões de postos líquidos",
            "skills_disrupted": "39% das competências essenciais transformadas até 2030"
        })

    def list_available_occupations(self) -> List[Dict[str, str]]:
        return [
            {"id": occ["id"], "title": occ["title"], "category": occ["category"]}
            for occ in self.benchmark_data.get("occupations", [])
        ]

    def match_occupation(self, role: str, domain: str = "", cv_text: str = "") -> Dict[str, Any]:
        """Recupera o benchmark exato da mesma área sem contaminação externa."""
        clean_role = role.strip() if role else "Profissional Especialista"

        # 1. Match direto pelo nome exato do domínio (cobre todos os 9 domínios do domain_clusters)
        if domain and domain in self.specialized_benchmarks_2030:
            data = self.specialized_benchmarks_2030[domain]
            return {
                "id": domain.lower().replace(" ", "_"),
                "title": clean_role,
                "category": data["category"],
                "automation_risk_score": data["risk"],
                "augmentation_potential_score": data["augmentation"],
                "skills_radar_ideal": data.get("skills_radar_ideal", { "pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 9 }),
                "declining_tasks": data["declining_tasks"],
                "augmented_tasks": data["augmented_tasks"],
                "human_core_tasks": data["human_core_tasks"],
                "declining_skills": data["declining_skills"],
                "emerging_skills_2030": data["emerging_skills_2030"],
                "transition_pivots": data["transition_pivots"],
                "recommended_certifications": data["recommended_certifications"],
                "recommended_tools_2030": data["recommended_tools_2030"]
            }

        # 2. Fallback: busca parcial pelo nome do domínio nos benchmarks (tolerância a variações de texto)
        if domain:
            domain_lower = domain.lower()
            for domain_name, data in self.specialized_benchmarks_2030.items():
                if domain_lower in domain_name.lower() or domain_name.lower() in domain_lower:
                    return {
                        "id": domain_name.lower().replace(" ", "_"),
                        "title": clean_role,
                        "category": data["category"],
                        "automation_risk_score": data["risk"],
                        "augmentation_potential_score": data["augmentation"],
                        "skills_radar_ideal": data.get("skills_radar_ideal", { "pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 9 }),
                        "declining_tasks": data["declining_tasks"],
                        "augmented_tasks": data["augmented_tasks"],
                        "human_core_tasks": data["human_core_tasks"],
                        "declining_skills": data["declining_skills"],
                        "emerging_skills_2030": data["emerging_skills_2030"],
                        "transition_pivots": data["transition_pivots"],
                        "recommended_certifications": data["recommended_certifications"],
                        "recommended_tools_2030": data["recommended_tools_2030"]
                    }

        # 2. Match nas ocupações da base WEF
        for occ in self.benchmark_data.get("occupations", []):
            if occ["title"].lower() in clean_role.lower() or clean_role.lower() in occ["title"].lower():
                return occ

        # 3. Fallback Sintetizado com Isolamento de Domínio
        return self._synthesize_isolated_domain(clean_role, domain or "Área do Candidato")

    def _synthesize_isolated_domain(self, role: str, domain: str) -> Dict[str, Any]:
        """Sintetizador genérico com isolamento total de domínio."""
        return {
            "id": "custom_domain_role",
            "title": role,
            "category": f"Setor de {domain}",
            "automation_risk_score": 40,
            "augmentation_potential_score": 90,
            "skills_radar_ideal": { "pensamento_analitico": 8, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8 },
            "declining_tasks": [
                f"Lançamentos manuais, formulários e arquivos operacionais repetitivos em {role}",
                f"Busca e consolidação não assistida de documentos padrão de {domain}",
                "Tarefas burocráticas que não demandam pensamento crítico"
            ],
            "augmented_tasks": [
                f"Adoção de copilotos de IA especializados no ecossistema de {domain}",
                f"Automação de fluxos de trabalho e análise inteligente de dados da área de {role}",
                "Triagem e pré-redação assistida por agentes inteligentes"
            ],
            "human_core_tasks": [
                "Julgamento ético, bom senso e tomada de decisão estratégica em cenários complexos",
                "Construção de relacionamentos interpessoais de alta confiança e liderança",
                "Visão holística conectando o conhecimento técnico aos objetivos do negócio"
            ],
            "declining_skills": [
                "Processamento puramente mecânico de tarefas sem reflexão analítica",
                "Execução rotineira descolada de ferramentas digitais da área"
            ],
            "emerging_skills_2030": [
                f"Orquestração de IA Aplicada a {domain}",
                "Pensamento Crítico e Julgamento Ético",
                "Comunicação Estratégica e Liderança Interpessoal"
            ],
            "transition_pivots": [
                f"Especialista em Inovação e Inteligência de Dados em {role}",
                f"Consultor(a) Sênior de Estratégia em {domain}",
                f"Líder de Eficiência e Transformação da Área"
            ],
            "recommended_certifications": [
                f"Inteligência Artificial Aplicada a {domain}",
                "Liderança Estratégica e Tomada de Decisão",
                "Gestão de Projetos e Inovação"
            ],
            "recommended_tools_2030": [
                f"Copilotos de IA específicos para {domain}",
                "Ferramentas de Automação de Rotinas da Área",
                "Plataformas de Análise de Indicadores e Decisão"
            ]
        }