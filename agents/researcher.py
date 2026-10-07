"""
Agente Pesquisador de Mercado e Tendências 2030 (ResearcherAgent)
Calibrado com dados do Fórum Econômico Mundial (WEF 2025/2030), McKinsey e Kaggle (AI Impact on Jobs 2030).
"""

import json
import os
import re
from typing import Dict, Any, List, Optional


class ResearcherAgent:
    def __init__(self, data_path: Optional[str] = None):
        self.name = "ResearcherAgent"
        self.role = "Especialista em Tendências 2030 (WEF, McKinsey & Kaggle AI Impact)"

        if not data_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "wef_benchmark_2030.json")

        self.data_path = data_path
        self.benchmark_data = self._load_data()

        # Dicionário de Benchmarks Específicos por Cargo com Métricas Econométricas Reais 2030
        self.role_specific_benchmarks = {
            "assistente_administrativo": {
                "title": "Assistente Administrativo / Operações de Escritório",
                "category": "Administração, Rotinas de Escritório & Suporte",
                "risk": 84,
                "augmentation": 58,
                "skills_radar_ideal": {"pensamento_analitico": 7, "orquestracao_ia": 8, "criatividade_inovacao": 6, "lideranca_influencia": 6, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 6},
                "declining_tasks": [
                    "Digitação manual de dados e preenchimento repetitivo de planilhas de controle",
                    "Agendamento manual de reuniões, arquivo físico de notas e triagem básica de e-mails",
                    "Lançamento de notas fiscais em ERP sem automação de OCR inteligente"
                ],
                "augmented_tasks": [
                    "Orquestração de agentes de automação de escritório (Power Automate, Zapier, copilotos)",
                    "Triagem automatizada de documentos e notas fiscais por visão computacional",
                    "Geração de atas de reunião e sínteses executivas instantâneas com IA"
                ],
                "human_core_tasks": [
                    "Gestão de clima organizacional e relacionamento interpessoal no ambiente de trabalho",
                    "Resolução de problemas operacionais imprevistos que exigem bom senso e tato",
                    "Mediação de prioridades com lideranças e atendimento com empatia"
                ],
                "declining_skills": [
                    "Digitação mecânica e preenchimento de formulários manuais",
                    "Organização manual de arquivos sem ferramentas de busca semântica"
                ],
                "emerging_skills_2030": [
                    "Automação Low-Code / No-Code de Processos (RPA & Power Automate)",
                    "Orquestração de Copilotos de Produtividade Pessoal (Copilot / Gemini)",
                    "Gestão Inteligente de Documentos e Dados de Escritório",
                    "Comunicação Interpessoal e Facilitação Operacional"
                ],
                "transition_pivots": [
                    "Analista de Automação de Processos de Negócio (BizOps)",
                    "Especialista em Suporte a Operações & People Experience",
                    "Assistente Executivo Aumentado por IA"
                ],
                "recommended_certifications": [
                    "Microsoft Certified: Power Platform Fundamentals",
                    "AI Productivity & Workflow Automation (Google / Coursera)",
                    "Gestão de Processos de Negócio (BPM)"
                ],
                "recommended_tools_2030": [
                    "Microsoft 365 Copilot / Google Workspace Gemini",
                    "Power Automate / Make / Zapier",
                    "Notion AI / ClickUp AI"
                ]
            },
            "analista_financeiro": {
                "title": "Analista Financeiro / FP&A / Controladoria",
                "category": "Finanças Corporativas, Controladoria & FP&A",
                "risk": 56,
                "augmentation": 88,
                "skills_radar_ideal": {"pensamento_analitico": 9, "orquestracao_ia": 9, "criatividade_inovacao": 7, "lideranca_influencia": 7, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 9},
                "declining_tasks": [
                    "Consolidação manual de extratos e conciliação de contas em planilhas estáticas",
                    "Confecção repetitiva de apresentações de slides de fechamento mensal",
                    "Cálculos manuais de variações orçamentárias descritivas"
                ],
                "augmented_tasks": [
                    "Modelagem financeira preditiva com simulações de Monte Carlo aceleradas por IA",
                    "Análise preditiva de fluxo de caixa e detecção de anomalias contábeis em tempo real",
                    "Dashboards dinâmicos conectados a copilotos de consulta em linguagem natural"
                ],
                "human_core_tasks": [
                    "Tomada de decisão estratégica sobre alocação de capital e investimentos de risco",
                    "Negociação de termos de crédito com instituições financeiras e parceiros",
                    "Storytelling executivo traduzindo dados complexos para a tomada de decisão da diretoria"
                ],
                "declining_skills": [
                    "Montagem mecânica de tabelas dinâmicas em Excel sem automação",
                    "Análise estática retrospectiva sem projeção preditiva"
                ],
                "emerging_skills_2030": [
                    "Modelagem Financeira Preditiva e Machine Learning Aplicado",
                    "Business Intelligence com IA e Análise de Dados (Python/PowerBI)",
                    "Gestão Estratégica de Riscos e Governança Corporativa",
                    "Storytelling Financeiro para Tomadores de Decisão"
                ],
                "transition_pivots": [
                    "Especialista em FP&A Preditivo & Inteligência de Negócios",
                    "Gerente de Controladoria e Planejamento Estratégico",
                    "Consultor(a) Financeiro de Fusões, Aquisições e Valuation"
                ],
                "recommended_certifications": [
                    "Financial Modeling & Valuation Analyst (CFI FMVA)",
                    "Data Analytics for Finance with Python (Wharton / Coursera)",
                    "Certificação em FP&A Estratégico & PowerBI Avançado"
                ],
                "recommended_tools_2030": [
                    "Copilotos Financeiros (BloombergGPT, FinChat AI, Excel Copilot)",
                    "PowerBI / Tableau com modelos preditivos integrados",
                    "Python (Pandas, Statsmodels) para econometria e forecasting"
                ]
            },
            "dev_senior": {
                "title": "Tech Lead / Arquiteto(a) de Software Sênior",
                "category": "Tecnologia, Arquitetura de Software & Liderança Técnica",
                "risk": 18,
                "augmentation": 96,
                "skills_radar_ideal": {"pensamento_analitico": 10, "orquestracao_ia": 10, "criatividade_inovacao": 9, "lideranca_influencia": 9, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 10},
                "declining_tasks": [
                    "Escrita manual de código repetitivo de boilerplate e CRUDs básicos",
                    "Code review focado apenas em estilo e sintaxe (já automatizado por linters de IA)",
                    "Configuração manual de scripts básicos de deploy e testes unitários padronizados"
                ],
                "augmented_tasks": [
                    "Orquestração de agentes de código autônomos (Claude Code, Gemini, Copilot Workspace)",
                    "Geração automatizada de diagramas de arquitetura e análise de conformidade de segurança",
                    "Refatoração de grandes codebases legados e migrações de stack com auxílio de IA"
                ],
                "human_core_tasks": [
                    "Decisões fundamentais de trade-off de arquitetura (consistência vs. disponibilidade, custo vs. escala)",
                    "Mentoria técnica, formação de novos engenheiros e desenvolvimento de lideranças",
                    "Alinhamento estratégico entre a capacidade técnica de engenharia e os objetivos de negócio"
                ],
                "declining_skills": [
                    "Desenvolvimento de código puramente manual sem assistência de ferramentas agênticas",
                    "Memorização de sintaxes e frameworks sem domínio dos fundamentos de arquitetura"
                ],
                "emerging_skills_2030": [
                    "Engenharia de Sistemas Agênticos e Orquestração de Modelos de IA",
                    "Arquitetura de Software Confiável, Segura e com Princípios de AI Safety",
                    "Liderança Técnica de Equipes Híbridas (Humanos + Agentes Autônomos)",
                    "Design de Microsserviços e Sistemas Distribuídos Resilientes"
                ],
                "transition_pivots": [
                    "Chief Technology Officer (CTO) / Diretor(a) de Engenharia",
                    "Principal AI Architect / Arquiteto de Sistemas Agênticos",
                    "Especialista em Cibersegurança e Resiliência Crítica"
                ],
                "recommended_certifications": [
                    "AWS Certified Solutions Architect — Professional",
                    "Designing and Building AI Agents (DeepLearning.AI / Stanford)",
                    "Liderança Executiva de Engenharia de Software"
                ],
                "recommended_tools_2030": [
                    "Agentes de Codificação Autônoma (Claude Code, Cursor, Antigravity)",
                    "Kubernetes, Docker, Terraform & Cloud Native",
                    "Plataformas de Observabilidade e Monitoramento de LLMs (LangSmith, OpenTelemetry)"
                ]
            },
            "dev_junior": {
                "title": "Desenvolvedor(a) Front-end / Júnior",
                "category": "Tecnologia e Engenharia de Software",
                "risk": 68,
                "augmentation": 88,
                "skills_radar_ideal": {"pensamento_analitico": 8, "orquestracao_ia": 9, "criatividade_inovacao": 7, "lideranca_influencia": 5, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 7},
                "declining_tasks": [
                    "Escrita manual de telas simples e conversão de layouts do Figma para HTML/CSS básico",
                    "Correção de bugs simples de formulários e sintaxe de componentes",
                    "Criação manual de testes unitários triviais e documentação básica"
                ],
                "augmented_tasks": [
                    "Uso de copilotos para gerar 80% do código repetitivo e componentes de interface",
                    "Prototipagem rápida de aplicações completas com auxílio de IA generativa",
                    "Refatoração acelerada de código e depuração interativa com agentes"
                ],
                "human_core_tasks": [
                    "Entendimento das regras de negócio do cliente e da experiência do usuário (UX)",
                    "Validação crítica de acessibilidade, segurança e comportamento em casos de borda",
                    "Comunicação com a equipe e integração contínua com a visão do produto"
                ],
                "declining_skills": [
                    "Codificação exclusivamente manual sem ferramentas de IA",
                    "Conhecimento superficial restrito a apenas uma biblioteca de interface"
                ],
                "emerging_skills_2030": [
                    "Engenharia de Prompt e Orquestração de Agentes de Desenvolvimento",
                    "Fundamentos Sólidos de Arquitetura de Software e TypeScript Avançado",
                    "Desenvolvimento Full-Stack Integrado a APIs de IA",
                    "Testes Automatizados e Práticas de CI/CD"
                ],
                "transition_pivots": [
                    "Desenvolvedor(a) Full-Stack Aumentado por IA",
                    "Engenheiro(a) de Integração de IA e Interfaces Conversacionais",
                    "Especialista em UX Engineering e Prototipagem Rápida"
                ],
                "recommended_certifications": [
                    "Full Stack Open (University of Helsinki)",
                    "AI-Assisted Software Development (Meta / Coursera)",
                    "Certificação Oficial em TypeScript e Nuvem (AWS Cloud Practitioner)"
                ],
                "recommended_tools_2030": [
                    "GitHub Copilot / Cursor / Gemini Code Assist",
                    "React / Next.js / TypeScript / TailwindCSS",
                    "Docker e Ferramentas de Testes Automatizados (Playwright, Jest)"
                ]
            },
            "advogado_junior": {
                "title": "Advogado(a) / Consultor(a) Jurídico",
                "category": "Direito, Regulação & Conformidade Empresarial",
                "risk": 52,
                "augmentation": 84,
                "skills_radar_ideal": {"pensamento_analitico": 10, "orquestracao_ia": 8, "criatividade_inovacao": 7, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 10},
                "declining_tasks": [
                    "Revisão manual exaustiva de contratos padrão de prestação de serviços e NDAs",
                    "Busca jurisprudencial tradicional em diários oficiais e compilação mecânica de julgados",
                    "Redação de petições iniciais padronizadas de cobrança e requerimentos simples"
                ],
                "augmented_tasks": [
                    "Análise preditiva de riscos contratuais com LLMs jurídicos especializados",
                    "Due diligence automatizada cruzando centenas de documentos em minutos",
                    "Pesquisa jurisprudencial semântica identificando tendências de julgamento de magistrados"
                ],
                "human_core_tasks": [
                    "Estratégia processual, sustentação oral e persuasão em audiências e tribunais",
                    "Aconselhamento ético em zonas cinzentas da legislação e negociações de alto valor",
                    "Construção de teses jurídicas inéditas para novas tecnologias e modelos de negócio"
                ],
                "declining_skills": [
                    "Leitura e conferência exclusivamente manual de cláusulas padrão",
                    "Pesquisa de leis sem ferramentas de busca semântica inteligente"
                ],
                "emerging_skills_2030": [
                    "Legal Tech & Orquestração de LLMs Jurídicos (Harvey AI, CoCounsel)",
                    "Compliance Digital, Privacidade de Dados (LGPD/GDPR) e Regulação de IA",
                    "Negociação Estratégica e Mediação de Disputas Complexas",
                    "Design de Contratos Inteligentes e Governança Jurídica"
                ],
                "transition_pivots": [
                    "Especialista em Direito Digital, Proteção de Dados e Regulação de IA",
                    "Diretor(a) de Compliance e Gestão de Riscos Corporativos",
                    "Consultor(a) Jurídico Estratégico em Operações Societárias e M&A"
                ],
                "recommended_certifications": [
                    "Legal Tech & AI for Lawyers (Harvard Law School Executive Education)",
                    "Certified Information Privacy Professional (CIPP/E / IAPP)",
                    "Compliance Empresarial e Governança Corporativa (FGV / Insper)"
                ],
                "recommended_tools_2030": [
                    "Plataformas de IA Jurídica (Harvey AI, Lexis+ AI, Jusbrasil IA)",
                    "Sistemas de Gestão Contratual Inteligente (CLM)",
                    "Ferramentas de Jurimetria e Análise Preditiva de Decisões"
                ]
            },
            "designer_grafico": {
                "title": "Designer Gráfico & Mídias Digitais",
                "category": "Design, Comunicação Visual & Criação",
                "risk": 64,
                "augmentation": 80,
                "skills_radar_ideal": {"pensamento_analitico": 7, "orquestracao_ia": 10, "criatividade_inovacao": 10, "lideranca_influencia": 7, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8},
                "declining_tasks": [
                    "Recorte manual de fotos de produtos e remoção repetitiva de fundos",
                    "Adaptação mecânica de formatos de banners para diferentes redes sociais",
                    "Criação de variações de posts estáticos padronizados sem conceito autoral"
                ],
                "augmented_tasks": [
                    "Geração de conceitos visuais e moodboards hiper-realistas com Midjourney e Firefly",
                    "Criação de animações e vídeos promocionais com ferramentas de IA generativa",
                    "Direção de arte multimodal combinando 3D, IA e identidade de marca em tempo recorde"
                ],
                "human_core_tasks": [
                    "Conceituação de identidade de marca e storytelling emocional com o público",
                    "Direção de arte estratégica garantindo coerência visual e sensibilidade estética",
                    "Julgamento crítico sobre adequação cultural, ética e impacto emocional da campanha"
                ],
                "declining_skills": [
                    "Execução puramente braçal de recortes e montagens estáticas",
                    "Dependência exclusiva de banco de imagens genérico"
                ],
                "emerging_skills_2030": [
                    "Direção de Arte Generativa e Engenharia de Prompt Visual",
                    "Design de Experiência do Usuário (UI/UX) e Design de Produto Digital",
                    "Motion Design e Produção Audiovisual com IA (Runway, Sora)",
                    "Estratégia de Branding e Posicionamento de Marca"
                ],
                "transition_pivots": [
                    "Diretor(a) de Criação e Arte Generativa",
                    "Product Designer (UI/UX) de Produtos Digitais",
                    "Especialista em Identidade de Marca e Storytelling Multimodal"
                ],
                "recommended_certifications": [
                    "Generative AI for Visual Designers (Adobe Certified / Parsons)",
                    "UX Design Professional Certificate (Google / Coursera)",
                    "Branding & Estratégia de Marca (Miami Ad School)"
                ],
                "recommended_tools_2030": [
                    "Midjourney / Adobe Firefly / Stable Diffusion / DALL-E",
                    "Figma com plugins de IA generativa",
                    "Runway Gen-3 / Sora / After Effects para Motion Design"
                ]
            },
            "atendente_sac": {
                "title": "Atendente de SAC / Contact Center",
                "category": "Atendimento, Suporte ao Cliente & Operações",
                "risk": 88,
                "augmentation": 52,
                "skills_radar_ideal": {"pensamento_analitico": 6, "orquestracao_ia": 7, "criatividade_inovacao": 5, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 6},
                "declining_tasks": [
                    "Resolução de dúvidas frequentes (FAQ) seguindo scripts padronizados",
                    "Emissão de 2ª via de faturas e consultas de status de pedidos",
                    "Triagem mecânica de chamados e preenchimento de formulários de ticket"
                ],
                "augmented_tasks": [
                    "Uso de copiloto de atendimento que sugere respostas e resume o histórico do cliente em tempo real",
                    "Análise em tempo real do tom de voz e sentimento do cliente durante o atendimento",
                    "Automação de tarefas pós-chamada (registro de ata e atualização de CRM)"
                ],
                "human_core_tasks": [
                    "Gestão de crises e atendimento a clientes altamente frustrados com empatia genuína",
                    "Mediação de casos atípicos que fogem às regras automáticas do sistema",
                    "Construção de conexão emocional e retenção de contas estratégicas"
                ],
                "declining_skills": [
                    "Repetição de scripts engessados sem personalização",
                    "Atendimento mecânico e transacional de dúvidas simples"
                ],
                "emerging_skills_2030": [
                    "Suporte Avançado a Sucesso do Cliente (Customer Success)",
                    "Gestão de Experiência do Cliente (CX) e Análise de Feedback",
                    "Inteligência Emocional, Comunicação Não-Violenta e Desescalada de Conflitos",
                    "Operação de Plataformas de Atendimento com IA (Zendesk AI, Salesforce Agentforce)"
                ],
                "transition_pivots": [
                    "Analista de Customer Success (Sucesso do Cliente)",
                    "Especialista em Treinamento e Curadoria de Chatbots de IA",
                    "Supervisor(a) de Experiência do Cliente e Retenção"
                ],
                "recommended_certifications": [
                    "Customer Success Specialist Certification (Gainsight / Hubspot)",
                    "Gestão da Experiência do Cliente — CX Management",
                    "Comunicação Assertiva e Resolução de Conflitos"
                ],
                "recommended_tools_2030": [
                    "Salesforce Agentforce / Zendesk AI",
                    "Intercom Copilot / Hubspot Service Hub",
                    "Plataformas de Análise de Sentimento em Tempo Real"
                ]
            },
            "gerente_projetos": {
                "title": "Gerente de Projetos / Scrum Master",
                "category": "Gestão, Métodos Ágeis & Liderança de Entregas",
                "risk": 34,
                "augmentation": 92,
                "skills_radar_ideal": {"pensamento_analitico": 9, "orquestracao_ia": 9, "criatividade_inovacao": 8, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9},
                "declining_tasks": [
                    "Atualização manual de status de tarefas em quadros Kanban / Jira",
                    "Cálculo manual de métricas de velocidade e geração de relatórios de sprint",
                    "Agendamento de reuniões de alinhamento e compilação de atas"
                ],
                "augmented_tasks": [
                    "Previsão de riscos de prazo e gargalos de entrega com algoritmos preditivos",
                    "Alocação otimizada de recursos da equipe com base em dados de capacidade gerados por IA",
                    "Resumos automáticos de status de múltiplos squads em tempo real"
                ],
                "human_core_tasks": [
                    "Liderança servidora, motivação de equipe e resolução de conflitos humanos",
                    "Negociação de expectativas e prioridades com stakeholders e executivos C-Level",
                    "Julgamento sobre trade-offs estratégicos de escopo, qualidade e tempo"
                ],
                "declining_skills": [
                    "Acompanhamento puramente burocrático de cronogramas sem foco em valor",
                    "Preenchimento manual de relatórios de progresso"
                ],
                "emerging_skills_2030": [
                    "Gestão Ágil Aumentada por IA e Análise Preditiva de Entregas",
                    "Liderança Estratégica de Times Multidisciplinares e Remotos",
                    "Gestão de Mudanças Organizacionais (Change Management)",
                    "Alinhamento de Estratégia de Negócios com OKRs Dinâmicos"
                ],
                "transition_pivots": [
                    "Product Manager (PM) / Head de Produto",
                    "Diretor(a) de Transformação Ágil e Eficiência Organizacional",
                    "Agile Coach e Consultor(a) de Liderança de Engenharia"
                ],
                "recommended_certifications": [
                    "PMP (Project Management Professional) / PMI-ACP",
                    "Professional Scrum Master (PSM II / Scrum.org)",
                    "AI-Driven Project Management (PMI)"
                ],
                "recommended_tools_2030": [
                    "Jira com IA integrada / Monday.com AI",
                    "Plataformas de Análise Preditiva de Projetos (ClickUp Brain)",
                    "Miro / Mural com geração de diagramas por IA"
                ]
            },
            "medico_saude": {
                "title": "Médico(a) / Profissional de Saúde",
                "category": "Saúde, Medicina & Cuidados Clínicos",
                "risk": 22,
                "augmentation": 96,
                "skills_radar_ideal": {"pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 7, "lideranca_influencia": 9, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 10},
                "declining_tasks": [
                    "Preenchimento burocrático manual de prontuários e guias de convênio",
                    "Busca mecânica em tabelas de posologia e interações medicamentosas",
                    "Triagem básica de sinais vitais que já pode ser realizada por biossensores"
                ],
                "augmented_tasks": [
                    "Apoio a diagnósticos complexos por visão computacional e IA multimodal",
                    "Uso de escribas médicos inteligentes de voz para transcrição automática de consultas",
                    "Medicina de precisão cruzando histórico clínico com dados genômicos e biossensores"
                ],
                "human_core_tasks": [
                    "Empatia, escuta clínica aprofundada e construção de relação médico-paciente de confiança",
                    "Decisões bioéticas críticas em situações delicadas e de alta incerteza",
                    "Comunicação humanizada de diagnósticos e adesão do paciente ao tratamento"
                ],
                "declining_skills": [
                    "Memorização passiva de bulas sem verificação em sistemas inteligentes",
                    "Atendimento médico transacional e impessoal focado apenas em sintomas isolados"
                ],
                "emerging_skills_2030": [
                    "Interpretação e Auditoria Clínica de Diagnósticos Assistidos por IA",
                    "Telemedicina Avançada e Monitoramento Remoto Contínuo",
                    "Medicina de Precisão, Genômica e Terapias Personalizadas",
                    "Bioética Digital e Comunicação Clínica Empática"
                ],
                "transition_pivots": [
                    "Médico(a) Especialista em Saúde Digital e Telemedicina",
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
            "vendedor_comercial": {
                "title": "Especialista Comercial / Vendas & Negociação",
                "category": "Vendas, Marketing & Expansão de Negócios",
                "risk": 50,
                "augmentation": 86,
                "skills_radar_ideal": {"pensamento_analitico": 7, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8},
                "declining_tasks": [
                    "Envio manual de e-mails frios padronizados de prospecção",
                    "Preenchimento e atualização manual de etapas no CRM",
                    "Elaboração mecânica de propostas comerciais a partir de templates básicos"
                ],
                "augmented_tasks": [
                    "Qualificação preditiva de leads baseada em dados de intenção de compra",
                    "Copilotos de vendas que analisam conversas e sugerem objeções e próximos passos",
                    "Personalização hiper-segmentada de propostas comerciais geradas por IA"
                ],
                "human_core_tasks": [
                    "Construção de relacionamentos de alta confiança e negociações de grandes contas (Enterprise)",
                    "Leitura sutil de linguagem corporal, tom emocional e interesses ocultos na negociação",
                    "Alinhamento de valor estratégico e resolução de impasses comerciais complexos"
                ],
                "declining_skills": [
                    "Abordagens genéricas de telemarketing e spam de e-mails",
                    "Venda transacional focada apenas em preço sem proposta de valor consultiva"
                ],
                "emerging_skills_2030": [
                    "Venda Consultiva Aumentada por IA e Inteligência de Contas (ABM)",
                    "Negociação Estratégica de Alto Impacto e Fechamento de Grandes Contas",
                    "Gestão de Relacionamento no CRM com Copilotos Inteligentes",
                    "Comunicação Persuasiva e Storytelling Comercial"
                ],
                "transition_pivots": [
                    "Executivo(a) de Contas Estratégicas (Enterprise Account Executive)",
                    "Diretor(a) Comercial / Head de Receita (CRO)",
                    "Consultor(a) de Estratégia de Go-To-Market e Parcerias"
                ],
                "recommended_certifications": [
                    "Salesforce Certified Sales Representative",
                    "Metodologias de Venda Consultiva (SPIN Selling / Challenger Sale)",
                    "AI in Sales & Revenue Operations (Hubspot Academy)"
                ],
                "recommended_tools_2030": [
                    "Gong.io / Chorus.ai (Inteligência de Conversas Comerciais)",
                    "Salesforce Einstein / Hubspot AI",
                    "Apollo.io / Clay para Prospecção Inteligente"
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
            "source": "Kaggle (AI Impact on Jobs 2030) + World Economic Forum (WEF 2025/2030)",
            "net_job_creation": "+78 milhões de postos líquidos",
            "skills_disrupted": "39% das competências essenciais transformadas até 2030"
        })

    def list_available_occupations(self) -> List[Dict[str, str]]:
        return [
            {"id": "dev_junior", "title": "Desenvolvedor Front-end Júnior", "category": "Tecnologia e Engenharia de Software"},
            {"id": "dev_senior", "title": "Tech Lead & Arquiteta de Software Sênior", "category": "Tecnologia e Arquitetura de Software"},
            {"id": "assistente_adm", "title": "Assistente Administrativa", "category": "Administração e Suporte de Escritório"},
            {"id": "analista_financeiro", "title": "Analista Financeiro / FP&A", "category": "Finanças Corporativas e Controladoria"},
            {"id": "advogado_junior", "title": "Advogada Associada / Contratos", "category": "Direito e Conformidade Regulatória"},
            {"id": "designer_grafico", "title": "Designer Gráfico & Mídias Digitais", "category": "Design e Criação Visual"},
            {"id": "atendente_sac", "title": "Operadora de Atendimento ao Cliente / SAC", "category": "Atendimento e Experiência do Cliente"},
            {"id": "gerente_projetos", "title": "Gerente de Projetos Ágeis / Scrum Master", "category": "Gestão e Liderança de Projetos"}
        ]

    def match_occupation(self, role: str, domain: str = "", cv_text: str = "") -> Dict[str, Any]:
        """Recupera o benchmark mais específico e diferenciado para o cargo analisado."""
        clean_role = role.strip() if role else "Profissional"
        text_context = f"{clean_role} {domain} {cv_text}".lower()

        # 1. Match por palavras-chave em benchmarks específicos de cargo
        if any(w in text_context for w in ["assistente adm", "auxiliar adm", "secretár", "escritório", "rotinas de escritório", "contas a pagar"]):
            return self._build_benchmark("assistente_administrativo", clean_role)
        elif any(w in text_context for w in ["financeir", "fp&a", "controlador", "balanço", "orçamento", "contábil", "contador", "investimento"]):
            return self._build_benchmark("analista_financeiro", clean_role)
        elif any(w in text_context for w in ["tech lead", "arquiteto de software", "arquiteta", "líder técnico", "engenheiro de software sênior", "cto", "dev sênior"]):
            return self._build_benchmark("dev_senior", clean_role)
        elif any(w in text_context for w in ["desenvolvedor", "programador", "front", "react", "júnior", "fullstack", "dev júnior", "html"]):
            return self._build_benchmark("dev_junior", clean_role)
        elif any(w in text_context for w in ["advogad", "direito", "jurídic", "contrato", "oab", "contencioso", "compliance"]):
            return self._build_benchmark("advogado_junior", clean_role)
        elif any(w in text_context for w in ["designer", "design", "figma", "photoshop", "mídia digital", "banner", "criação visual", "arte"]):
            return self._build_benchmark("designer_grafico", clean_role)
        elif any(w in text_context for w in ["sac", "atendente", "telemarketing", "contact center", "chamados", "suporte ao cliente"]):
            return self._build_benchmark("atendente_sac", clean_role)
        elif any(w in text_context for w in ["scrum", "gerente de projeto", "project manager", "ágil", "kanban", "squad"]):
            return self._build_benchmark("gerente_projetos", clean_role)
        elif any(w in text_context for w in ["médic", "saúde", "hospital", "clínic", "enferm", "nutri", "psicól", "paciente"]):
            return self._build_benchmark("medico_saude", clean_role)
        elif any(w in text_context for w in ["vendedor", "comercial", "vendas", "sdr", "negociação", "prospecção"]):
            return self._build_benchmark("vendedor_comercial", clean_role)

        # 2. Match nas ocupações da base WEF JSON
        for occ in self.benchmark_data.get("occupations", []):
            if occ["title"].lower() in clean_role.lower() or clean_role.lower() in occ["title"].lower():
                return occ

        # 3. Fallback inteligente e dinâmico (não estático)
        return self._synthesize_dynamic_domain(clean_role, domain or "Sua Área", text_context)

    def _build_benchmark(self, key: str, custom_title: str) -> Dict[str, Any]:
        """Constrói o objeto de benchmark com os dados do cargo."""
        data = self.role_specific_benchmarks.get(key, self.role_specific_benchmarks["assistente_administrativo"])
        return {
            "id": key,
            "title": custom_title if custom_title and len(custom_title) > 2 else data["title"],
            "category": data["category"],
            "automation_risk_score": data["risk"],
            "augmentation_potential_score": data["augmentation"],
            "skills_radar_ideal": data["skills_radar_ideal"],
            "declining_tasks": data["declining_tasks"],
            "augmented_tasks": data["augmented_tasks"],
            "human_core_tasks": data["human_core_tasks"],
            "declining_skills": data["declining_skills"],
            "emerging_skills_2030": data["emerging_skills_2030"],
            "transition_pivots": data["transition_pivots"],
            "recommended_certifications": data["recommended_certifications"],
            "recommended_tools_2030": data["recommended_tools_2030"]
        }

    def _synthesize_dynamic_domain(self, role: str, domain: str, text_context: str) -> Dict[str, Any]:
        """Gera um benchmark dinâmico e calibrado para cargos não catalogados."""
        # Estima risco e potencial com base na natureza da função
        is_operational = any(w in text_context for w in ["operac", "manual", "rotina", "cadastr", "digit", "suport"])
        is_leadership = any(w in text_context for w in ["gerent", "diret", "líder", "coorden", "estratég"])
        is_creative = any(w in text_context for w in ["criat", "art", "inov", "design", "conteúdo"])

        if is_operational:
            base_risk = 74
            base_aug = 65
        elif is_leadership:
            base_risk = 25
            base_aug = 94
        elif is_creative:
            base_risk = 58
            base_aug = 82
        else:
            base_risk = 45
            base_aug = 88

        return {
            "id": "custom_role",
            "title": role,
            "category": f"Setor de {domain}",
            "automation_risk_score": base_risk,
            "augmentation_potential_score": base_aug,
            "skills_radar_ideal": {"pensamento_analitico": 8, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 8},
            "declining_tasks": [
                f"Execução mecânica e repetitiva de tarefas operacionais em {role}",
                f"Processamento manual e compilação de documentos padrão de {domain}",
                "Atividades transacionais que não demandam pensamento crítico"
            ],
            "augmented_tasks": [
                f"Adoção de copilotos de IA generativa para acelerar a rotina de {role}",
                f"Análise preditiva de dados e geração de relatórios inteligentes em {domain}",
                "Triagem e síntese assistida por agentes inteligentes especializados"
            ],
            "human_core_tasks": [
                "Julgamento ético, bom senso e tomada de decisão estratégica em cenários complexos",
                "Construção de relacionamentos interpessoais de alta confiança e liderança",
                "Visão sistêmica conectando o conhecimento técnico aos objetivos do negócio"
            ],
            "declining_skills": [
                "Execução puramente manual sem assistência de ferramentas digitais",
                "Processamento mecânico sem visão analítica ou estratégica"
            ],
            "emerging_skills_2030": [
                f"Orquestração de IA Aplicada a {domain}",
                "Pensamento Crítico e Julgamento Ético",
                "Comunicação Estratégica e Liderança Interpessoal",
                "Capacidade de Aprendizado Contínuo (Lifelong Learning)"
            ],
            "transition_pivots": [
                f"Especialista em Inovação e Inteligência de Dados em {role}",
                f"Consultor(a) Estratégico em {domain}",
                f"Líder de Transformação Digital da Área"
            ],
            "recommended_certifications": [
                f"Inteligência Artificial Aplicada a {domain}",
                "Liderança Estratégica e Tomada de Decisão",
                "Gestão de Projetos e Inovação"
            ],
            "recommended_tools_2030": [
                f"Copilotos de IA especializados para {domain}",
                "Ferramentas de Automação de Rotinas da Área",
                "Plataformas de Análise de Indicadores e Tomada de Decisão"
            ]
        }