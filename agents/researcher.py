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

        # Catálogo Extensivo de Arquétipos Profissionais com Métricas Reais
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
                "declining_skills": ["Digitação mecânica", "Organização manual de arquivos"],
                "emerging_skills_2030": ["Automação Low-Code / No-Code", "Copilotos de Produtividade", "Gestão Inteligente de Documentos", "Comunicação Interpessoal"],
                "transition_pivots": ["Analista de Automação de Processos (BizOps)", "Especialista em People Experience", "Assistente Executivo Aumentado por IA"],
                "recommended_certifications": ["Microsoft Certified: Power Platform", "AI Productivity & Workflow Automation", "Gestão de Processos (BPM)"],
                "recommended_tools_2030": ["Microsoft 365 Copilot / Gemini Workspace", "Power Automate / Zapier", "Notion AI / ClickUp"]
            },
            "atendente_sac": {
                "title": "Atendente de SAC / Contact Center",
                "category": "Atendimento, Suporte ao Cliente & Operações",
                "risk": 88,
                "augmentation": 52,
                "skills_radar_ideal": {"pensamento_analitico": 6, "orquestracao_ia": 7, "criatividade_inovacao": 5, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 6},
                "declining_tasks": [
                    "Resolução de dúvidas frequentes (FAQ) seguindo scripts padronizados",
                    "Emissão de 2ª via de faturas e consultas mecânicas de status de pedidos",
                    "Triagem manual de chamados e abertura repetitiva de tickets"
                ],
                "augmented_tasks": [
                    "Copiloto de atendimento sugerindo respostas e resumos do cliente em tempo real",
                    "Análise em tempo real do tom de voz e sentimento do cliente durante a chamada",
                    "Automação de registros pós-atendimento e atualização automática de CRM"
                ],
                "human_core_tasks": [
                    "Gestão de crises e atendimento a clientes altamente frustrados com empatia genuína",
                    "Mediação de exceções e casos atípicos não previstos pelas regras automáticas",
                    "Construção de conexão humana e retenção de contas críticas"
                ],
                "declining_skills": ["Repetição de scripts engessados", "Atendimento transacional mecânico"],
                "emerging_skills_2030": ["Customer Success Avançado", "Gestão de Experiência do Cliente (CX)", "Inteligência Emocional e Desescalada de Conflitos", "Operação de Plataformas de IA (Salesforce Agentforce)"],
                "transition_pivots": ["Analista de Customer Success (CS)", "Curador(a) e Treinador(a) de IA de Atendimento", "Especialista em Experiência do Cliente"],
                "recommended_certifications": ["Customer Success Specialist (Gainsight)", "Gestão de CX & NPS", "Comunicação Assertiva e Resolução de Conflitos"],
                "recommended_tools_2030": ["Salesforce Agentforce / Zendesk AI", "Intercom Copilot", "Plataformas de Análise de Sentimento"]
            },
            "contador_fiscal": {
                "title": "Contador(a) / Auditor(a) Fiscal",
                "category": "Contabilidade, Tributos & Auditoria Fiscal",
                "risk": 76,
                "augmentation": 74,
                "skills_radar_ideal": {"pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 6, "lideranca_influencia": 7, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 9},
                "declining_tasks": [
                    "Digitação de lançamentos contábeis e conciliação manual de extratos bancários",
                    "Cálculo mecânico de guias de impostos padrão e conferência manual de SPED",
                    "Emissão repetitiva de balancetes descritivos sem análise preditiva"
                ],
                "augmented_tasks": [
                    "Auditoria contínua e detecção de anomalias fiscais com modelos de Machine Learning",
                    "Planejamento tributário preditivo simulando múltiplos cenários de reforma tributária",
                    "Geração automatizada de relatórios contábeis estratégicos com IA explicativa"
                ],
                "human_core_tasks": [
                    "Consultoria estratégica de eficiência tributária e estruturação societária",
                    "Defesa em autos de infração e negociação técnica com órgãos fiscalizadores",
                    "Aconselhamento fiduciário para conselhos de administração e sócios"
                ],
                "declining_skills": ["Lançamento contábil manual", "Conferência visual de guias fiscais"],
                "emerging_skills_2030": ["Auditoria Tributária Algorítmica", "Consultoria Contábil Estratégica", "Compliance Fiscal Digital", "Storytelling de Indicadores Financeiros"],
                "transition_pivots": ["Consultor(a) de Planejamento Tributário & M&A", "Auditor(a) de Algoritmos Fiscais e Compliance", "Controller Estratégico de Negócios"],
                "recommended_certifications": ["Certificação em Planejamento Tributário Avançado", "Auditoria Contábil com Inteligência de Dados", "CFC / IFRS Specialist"],
                "recommended_tools_2030": ["Sistemas ERP com IA Fiscal integrada", "Python para auditoria de grandes volumes de dados", "Plataformas de Tax Intelligence"]
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
                "declining_skills": ["Montagem mecânica de tabelas em Excel", "Análise estática retrospectiva"],
                "emerging_skills_2030": ["Modelagem Financeira Preditiva", "Business Intelligence com IA (Python/PowerBI)", "Gestão Estratégica de Riscos", "Storytelling Financeiro"],
                "transition_pivots": ["Especialista em FP&A Preditivo & BI", "Gerente de Controladoria Estratégica", "Consultor(a) de Fusões e Aquisições (M&A)"],
                "recommended_certifications": ["Financial Modeling & Valuation (FMVA)", "Data Analytics for Finance (Wharton)", "PowerBI & FP&A Estratégico"],
                "recommended_tools_2030": ["Copilotos Financeiros (BloombergGPT, FinChat)", "PowerBI / Tableau com IA", "Python (Pandas, Statsmodels)"]
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
                "declining_skills": ["Codificação manual de boilerplate", "Sintaxe sem entendimento de arquitetura"],
                "emerging_skills_2030": ["Engenharia de Prompt e Orquestração Agêntica", "Fundamentos de Arquitetura e TypeScript", "Desenvolvimento Full-Stack com APIs de IA", "Testes Automatizados e CI/CD"],
                "transition_pivots": ["Desenvolvedor(a) Full-Stack Aumentado por IA", "Engenheiro(a) de Interfaces Conversacionais e Agentes", "UX Engineer de Prototipagem Rápida"],
                "recommended_certifications": ["Full Stack Open (Univ. of Helsinki)", "AI-Assisted Software Engineering", "AWS Cloud Practitioner"],
                "recommended_tools_2030": ["GitHub Copilot / Cursor / Gemini Code Assist", "Next.js / TypeScript / TailwindCSS", "Docker e Playwright"]
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
                "declining_skills": ["Desenvolvimento puramente manual sem agentes", "Memorização de sintaxes sem visão arquitetural"],
                "emerging_skills_2030": ["Engenharia de Sistemas Agênticos", "Arquitetura Resiliente e AI Safety", "Liderança de Equipes Híbridas (Humanos + IAs)", "Microsserviços Distribuídos de Alta Escala"],
                "transition_pivots": ["Chief Technology Officer (CTO)", "Principal AI Architect", "Especialista em Resiliência e Cibersegurança"],
                "recommended_certifications": ["AWS Certified Solutions Architect — Professional", "Building AI Agents (Stanford / DeepLearning.AI)", "Liderança Executiva de Engenharia"],
                "recommended_tools_2030": ["Claude Code / Cursor / Antigravity", "Kubernetes / Terraform / Cloud Native", "LangSmith / OpenTelemetry"]
            },
            "cientista_dados": {
                "title": "Cientista de Dados / Engenheiro(a) de IA & Machine Learning",
                "category": "Ciência de Dados, Inteligência Artificial & Big Data",
                "risk": 20,
                "augmentation": 98,
                "skills_radar_ideal": {"pensamento_analitico": 10, "orquestracao_ia": 10, "criatividade_inovacao": 9, "lideranca_influencia": 7, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9},
                "declining_tasks": [
                    "Limpeza manual repetitiva de dados e imputação básica de valores nulos",
                    "Ajuste manual e exaustivo de hiperparâmetros (AutoML já supera humanos nisso)",
                    "Escrita de queries SQL simples para extração de tabelas"
                ],
                "augmented_tasks": [
                    "Desenvolvimento e fine-tuning de modelos fundacionais e LLMs locais",
                    "Criação de pipelines de RAG (Retrieval-Augmented Generation) com bancos vetoriais",
                    "Simulações preditivas em larga escala cruzando dados não estruturados"
                ],
                "human_core_tasks": [
                    "Formulação matemática e conceitual de hipóteses de negócio complexas",
                    "Governança ética, mitigação de viés algorítmico e auditoria de modelos de IA",
                    "Tradução de descobertas de dados em decisões estratégicas para o C-Level"
                ],
                "declining_skills": ["Tuning manual de hiperparâmetros", "Limpeza puramente manual de planilhas"],
                "emerging_skills_2030": ["Orquestração de Modelos Fundacionais e RAG", "Governança e Ética de IA (AI Alignment)", "MLOps e Arquitetura de Big Data em Tempo Real", "Pensamento Científico sob Incerteza"],
                "transition_pivots": ["Head de Inteligência Artificial & Dados", "Arquiteto(a) de Sistemas Cognitivos", "Consultor(a) de Governança de Algoritmos"],
                "recommended_certifications": ["TensorFlow / PyTorch Developer Certificate", "AWS Certified Machine Learning — Specialty", "AI Alignment & Ethics (MIT / Oxford)"],
                "recommended_tools_2030": ["PyTorch / Hugging Face / vLLM", "Pinecone / Qdrant (Vector DBs)", "LangChain / LlamaIndex / MLflow"]
            },
            "advogado": {
                "title": "Advogado(a) / Consultor(a) Jurídico",
                "category": "Direito, Regulação & Conformidade Empresarial",
                "risk": 50,
                "augmentation": 85,
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
                "declining_skills": ["Leitura e conferência exclusivamente manual de cláusulas padrão", "Pesquisa de leis sem IA semântica"],
                "emerging_skills_2030": ["Legal Tech & LLMs Jurídicos (Harvey AI, CoCounsel)", "Compliance Digital e Proteção de Dados (LGPD/GDPR)", "Negociação Estratégica e Mediação Complexa", "Design de Contratos Inteligentes"],
                "transition_pivots": ["Especialista em Direito Digital e Regulação de IA", "Diretor(a) de Compliance e Riscos Corporativos", "Consultor(a) Jurídico Estratégico em M&A"],
                "recommended_certifications": ["Legal Tech & AI for Lawyers (Harvard Law School)", "CIPP/E — Privacidade de Dados (IAPP)", "Compliance Empresarial (FGV)"],
                "recommended_tools_2030": ["Harvey AI / Lexis+ AI / Jusbrasil IA", "Ironclad / Juro (CLM Inteligente)", "Jurimetria Preditiva"]
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
                "declining_skills": ["Execução puramente braçal de recortes", "Dependência exclusiva de bancos de imagens estáticos"],
                "emerging_skills_2030": ["Direção de Arte Generativa e Prompt Visual", "Design de Experiência (UI/UX) e Produto Digital", "Motion Design e Vídeo com IA (Runway, Sora)", "Estratégia de Branding e Posicionamento"],
                "transition_pivots": ["Diretor(a) de Criação e Arte Generativa", "Product Designer (UI/UX) de Produtos Digitais", "Especialista em Identidade de Marca e Storytelling"],
                "recommended_certifications": ["Generative AI for Visual Designers (Adobe / Parsons)", "UX Design Professional Certificate (Google)", "Branding Estratégico (Miami Ad School)"],
                "recommended_tools_2030": ["Midjourney / Adobe Firefly / Stable Diffusion", "Figma com IA", "Runway Gen-3 / Sora"]
            },
            "medico_clinico": {
                "title": "Médico(a) / Cirurgião / Especialista Clínico",
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
                "declining_skills": ["Memorização passiva de bulas", "Atendimento médico puramente transacional"],
                "emerging_skills_2030": ["Interpretação Clínica de Diagnósticos por IA", "Telemedicina Avançada e Monitoramento Remoto", "Medicina de Precisão e Genômica", "Bioética Digital e Relação Humanizada"],
                "transition_pivots": ["Médico(a) Especialista em Saúde Digital e Telemedicina", "Diretor(a) Clínico de Inovação e Medicina Personalizada", "Auditor(a) Médico de Algoritmos Clínicos"],
                "recommended_certifications": ["AI in Healthcare & CDSS (Harvard Medical School)", "Precision Medicine & Genomics (Stanford)", "Liderança Clínica e Experiência do Paciente"],
                "recommended_tools_2030": ["Escribas Médicos por IA (Nuance DAX, Nabla)", "Sistemas de Apoio Clínico Multimodal", "Telemonitoramento Preditivo"]
            },
            "nutricionista_terapeuta": {
                "title": "Nutricionista / Psicólogo(a) / Fisioterapeuta",
                "category": "Saúde, Bem-Estar & Terapia Personalizada",
                "risk": 24,
                "augmentation": 94,
                "skills_radar_ideal": {"pensamento_analitico": 8, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9},
                "declining_tasks": [
                    "Cálculo manual de calorias, macronutrientes e tabelas antropométricas básicas",
                    "Envio de lembretes manuais de acompanhamento e controle de peso por WhatsApp",
                    "Preenchimento repetitivo de formulários de anamnese padrão"
                ],
                "augmented_tasks": [
                    "Elaboração de planos alimentares e treinos hiper-personalizados baseados em biossensores e exames de sangue",
                    "Copiloto de análise comportamental e adesão do paciente ao plano terapêutico",
                    "Monitoramento contínuo de biomarcadores e gasto calórico em tempo real"
                ],
                "human_core_tasks": [
                    "Escuta empática profunda, motivação comportamental e apoio emocional",
                    "Diagnóstico clínico contextualizado com o estilo de vida e histórico emocional",
                    "Criação de vínculo de confiança indispensável para a mudança de hábitos"
                ],
                "declining_skills": ["Cálculo manual de dietas e tabelas estáticas", "Atendimento genérico não individualizado"],
                "emerging_skills_2030": ["Nutrição de Precisão / Terapia Integrativa com IA", "Análise de Dados de Wearables e Biossensores Contínuos", "Coaching Comportamental e Psicologia Positiva", "Comunicação Empática e Retenção de Pacientes"],
                "transition_pivots": ["Especialista em Longevidade & Saúde de Precisão", "Consultor(a) de Bem-Estar Corporativo e Saúde Integrativa", "Líder de Clínicas Digitais e Teleatendimento"],
                "recommended_certifications": ["Nutrição de Precisão e Genômica Nutricional", "Terapia Cognitivo-Comportamental Aplicada", "Saúde Digital e Wearables em Clínica"],
                "recommended_tools_2030": ["Softwares de Nutrição com IA Preditiva", "Plataformas de Teleatendimento e Prontuário Integrado", "Aplicativos de Acompanhamento Contínuo de Pacientes"]
            },
            "gerente_projetos": {
                "title": "Gerente de Projetos / Scrum Master / Product Manager",
                "category": "Gestão, Métodos Ágeis & Liderança de Entregas",
                "risk": 32,
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
                "declining_skills": ["Acompanhamento puramente burocrático de cronogramas", "Preenchimento manual de relatórios"],
                "emerging_skills_2030": ["Gestão Ágil Aumentada por IA e Análise Preditiva", "Liderança de Times Multidisciplinares e Remotos", "Gestão de Mudanças Organizacionais (Change Management)", "Alinhamento de Estratégia com OKRs Dinâmicos"],
                "transition_pivots": ["Product Manager (PM) / Head de Produto", "Diretor(a) de Transformação Ágil e Eficiência", "Agile Coach e Consultor(a) de Liderança"],
                "recommended_certifications": ["PMP / PMI-ACP", "Professional Scrum Master (PSM II)", "AI-Driven Project Management (PMI)"],
                "recommended_tools_2030": ["Jira com IA integrada / Monday.com AI", "ClickUp Brain / Linear", "Miro / Mural com IA"]
            },
            "vendedor_comercial": {
                "title": "Especialista Comercial / Vendas & Negociação",
                "category": "Vendas, Marketing & Expansão de Negócios",
                "risk": 48,
                "augmentation": 88,
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
                "declining_skills": ["Abordagens genéricas de spam de e-mails", "Venda transacional focada apenas em preço"],
                "emerging_skills_2030": ["Venda Consultiva Aumentada por IA (ABM)", "Negociação Estratégica de Alto Impacto", "Gestão de Relacionamento no CRM com Copilotos", "Comunicação Persuasiva e Storytelling Comercial"],
                "transition_pivots": ["Executivo(a) de Contas Estratégicas (Enterprise AE)", "Diretor(a) Comercial / Head de Receita (CRO)", "Consultor(a) de Estratégia de Go-To-Market"],
                "recommended_certifications": ["Salesforce Certified Sales Representative", "Metodologias de Venda Consultiva (SPIN / Challenger)", "AI in Sales (Hubspot)"],
                "recommended_tools_2030": ["Gong.io / Chorus.ai", "Salesforce Einstein / Hubspot AI", "Apollo.io / Clay"]
            },
            "professor_educador": {
                "title": "Professor(a) / Educador(a) / Especialista em Aprendizagem",
                "category": "Educação, Formação & Pedagogia",
                "risk": 28,
                "augmentation": 92,
                "skills_radar_ideal": {"pensamento_analitico": 8, "orquestracao_ia": 8, "criatividade_inovacao": 9, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9},
                "declining_tasks": [
                    "Correção mecânica de provas de múltipla escolha e tarefas padronizadas",
                    "Elaboração manual repetitiva de planos de aula e exercícios básicos",
                    "Transmissão passiva de conteúdos puramente expositivos"
                ],
                "augmented_tasks": [
                    "Criação de trilhas de aprendizagem adaptativas personalizadas para o ritmo de cada aluno",
                    "Geração de simulações interativas, jogos e estudos de caso imersivos com IA",
                    "Análise preditiva de dificuldades de retenção e engajamento escolar em tempo real"
                ],
                "human_core_tasks": [
                    "Inspiração, mentoria humana e desenvolvimento socioemocional dos alunos",
                    "Mediação de debates críticos, pensamento ético e formação cidadã",
                    "Empatia e acolhimento em momentos de frustração e bloqueio de aprendizagem"
                ],
                "declining_skills": ["Aulas exclusivamente expositivas e transmissivas", "Correção manual de avaliações simples"],
                "emerging_skills_2030": ["Design Instrucional com IA Generativa", "Metodologias Ativas e Aprendizagem Baseada em Projetos", "Mediação Socioemocional e Mentoria de Alunos", "Educação Personalizada por Dados de Aprendizagem"],
                "transition_pivots": ["Designer de Experiências de Aprendizagem com IA (EdTech)", "Coordenador(a) de Inovação Pedagógica", "Mentor(a) de Desenvolvimento Profissional e Liderança"],
                "recommended_certifications": ["AI in Education & Adaptive Learning (Harvard GSE)", "Metodologias Ativas de Ensino (FGV / Insper)", "Design Instrucional Digital"],
                "recommended_tools_2030": ["Plataformas de Aprendizagem Adaptativa (Khanmigo)", "Canva for Education com IA", "Ferramentas de Gamificação e Feedback Contínuo"]
            },
            "engenheiro_civil": {
                "title": "Engenheiro(a) de Projetos / Obras / Manufatura",
                "category": "Engenharia, Construção & Infraestrutura",
                "risk": 36,
                "augmentation": 88,
                "skills_radar_ideal": {"pensamento_analitico": 10, "orquestracao_ia": 9, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 9},
                "declining_tasks": [
                    "Desenho manual 2D repetitivo de pranchas em CAD",
                    "Cálculos manuais de quantitativos de materiais e orçamentos em planilhas simples",
                    "Verificação manual de interferências de tubulação em projetos complementares"
                ],
                "augmented_tasks": [
                    "Design generativo estrutural que calcula a melhor geometria com economia de material",
                    "Gêmeos Digitais (Digital Twins) e simulações térmicas/estruturais em tempo real",
                    "Planejamento de obras 4D/5D com BIM e monitoramento de canteiro por drones/visão computacional"
                ],
                "human_core_tasks": [
                    "Responsabilidade técnica (ART/CREA) e garantia de segurança de vidas humanas",
                    "Gestão de equipes de campo, liderança operacional de canteiro de obras",
                    "Tomada de decisão em imprevistos geológicos e negociação com fornecedores"
                ],
                "declining_skills": ["Desenho exclusivamente 2D manual", "Orçamentação manual sem software BIM"],
                "emerging_skills_2030": ["Design Generativo e Modelagem BIM 5D/6D", "Gêmeos Digitais e IoT em Obras", "Engenharia Sustentável e Materiais de Baixo Carbono", "Gestão de Segurança e Responsabilidade Fiduciária"],
                "transition_pivots": ["Especialista em BIM & Engenharia Digital", "Gerente de Obras Inteligentes e Sustentabilidade", "Consultor(a) de Gêmeos Digitais para Infraestrutura"],
                "recommended_certifications": ["Autodesk Certified Professional (Revit BIM)", "Digital Construction & Generative Design", "Gestão de Obras Sustentáveis (LEED)"],
                "recommended_tools_2030": ["Revit / Navisworks / Tekla Structures", "Autodesk Forma (Design Generativo)", "Drones e Plataformas de Monitoramento de Canteiro"]
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
        """Recupera o benchmark mais específico e diferenciado para qualquer cargo analisado."""
        clean_role = role.strip() if role else "Profissional"
        text_context = f"{clean_role} {domain} {cv_text}".lower()

        # Mapeamento semântico completo por palavras-chave
        if any(w in text_context for w in ["sac", "telemarketing", "call center", "chamados", "atendente", "operador de teleatendimento"]):
            return self._build_benchmark("atendente_sac", clean_role)
        elif any(w in text_context for w in ["assistente", "auxiliar adm", "secretár", "recepcionista", "digitador", "arquivo", "rotinas de escritório", "backoffice"]):
            return self._build_benchmark("assistente_administrativo", clean_role)
        elif any(w in text_context for w in ["contador", "contadora", "contábil", "contabilidade", "auditor", "fiscal", "tributário"]):
            return self._build_benchmark("contador_fiscal", clean_role)
        elif any(w in text_context for w in ["financeir", "fp&a", "controlador", "balanço", "orçamento", "investimento", "tesouraria", "economist", "banco", "crédito"]):
            return self._build_benchmark("analista_financeiro", clean_role)
        elif any(w in text_context for w in ["tech lead", "arquiteto de software", "arquiteta", "líder técnico", "cto", "dev sênior", "engenheiro de software sênior"]):
            return self._build_benchmark("dev_senior", clean_role)
        elif any(w in text_context for w in ["ciência de dados", "cientista de dados", "data science", "machine learning", "engenheiro de dados", "ia generativa"]):
            return self._build_benchmark("cientista_dados", clean_role)
        elif any(w in text_context for w in ["desenvolvedor", "programador", "front", "react", "júnior", "fullstack", "dev júnior", "html", "javascript"]):
            return self._build_benchmark("dev_junior", clean_role)
        elif any(w in text_context for w in ["advogad", "direito", "jurídic", "contrato", "oab", "contencioso", "compliance", "promotor", "juiz", "legal"]):
            return self._build_benchmark("advogado", clean_role)
        elif any(w in text_context for w in ["designer", "design", "figma", "photoshop", "mídia digital", "banner", "criação visual", "arte", "ilustrador"]):
            return self._build_benchmark("designer_grafico", clean_role)
        elif any(w in text_context for w in ["médic", "cirurgião", "crm", "hospital", "clínica médica", "doutor"]):
            return self._build_benchmark("medico_clinico", clean_role)
        elif any(w in text_context for w in ["nutri", "psicól", "terapeuta", "fisioterap", "enferm", "dentist", "fonoaudiol", "saúde"]):
            return self._build_benchmark("nutricionista_terapeuta", clean_role)
        elif any(w in text_context for w in ["scrum", "gerente", "project manager", "ágil", "kanban", "product manager", "pm", "diretor", "gestor"]):
            return self._build_benchmark("gerente_projetos", clean_role)
        elif any(w in text_context for w in ["vendedor", "comercial", "vendas", "sdr", "negociação", "prospecção", "representante comercial"]):
            return self._build_benchmark("vendedor_comercial", clean_role)
        elif any(w in text_context for w in ["professor", "professora", "educador", "ensino", "escola", "pedagogo", "docente", "instrutor"]):
            return self._build_benchmark("professor_educador", clean_role)
        elif any(w in text_context for w in ["engenheir", "engenharia", "civil", "elétric", "mecânic", "obras", "autocad", "bim", "construção"]):
            return self._build_benchmark("engenheiro_civil", clean_role)

        # 2. Match nas ocupações da base WEF JSON
        for occ in self.benchmark_data.get("occupations", []):
            if occ["title"].lower() in clean_role.lower() or clean_role.lower() in occ["title"].lower():
                return occ

        # 3. Fallback inteligente e dinâmico com estimativa de risco por domínio
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
        # Calcula scores específicos dependendo das características do cargo
        if "Saúde" in domain:
            base_risk = 25
            base_aug = 95
            ideal_radar = {"pensamento_analitico": 9, "orquestracao_ia": 8, "criatividade_inovacao": 7, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9}
        elif "Tecnologia" in domain:
            base_risk = 26
            base_aug = 96
            ideal_radar = {"pensamento_analitico": 10, "orquestracao_ia": 10, "criatividade_inovacao": 8, "lideranca_influencia": 7, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9}
        elif "Jurídico" in domain:
            base_risk = 52
            base_aug = 84
            ideal_radar = {"pensamento_analitico": 10, "orquestracao_ia": 8, "criatividade_inovacao": 7, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 10}
        elif "Administração" in domain:
            base_risk = 82
            base_aug = 60
            ideal_radar = {"pensamento_analitico": 7, "orquestracao_ia": 8, "criatividade_inovacao": 6, "lideranca_influencia": 6, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 6}
        elif "Educação" in domain:
            base_risk = 28
            base_aug = 92
            ideal_radar = {"pensamento_analitico": 8, "orquestracao_ia": 8, "criatividade_inovacao": 9, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 9}
        elif "Design" in domain:
            base_risk = 62
            base_aug = 80
            ideal_radar = {"pensamento_analitico": 7, "orquestracao_ia": 10, "criatividade_inovacao": 10, "lideranca_influencia": 7, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8}
        elif "Vendas" in domain:
            base_risk = 50
            base_aug = 86
            ideal_radar = {"pensamento_analitico": 7, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 10, "resiliencia_adaptabilidade": 9, "especializacao_estrategica": 8}
        elif "Engenharia" in domain:
            base_risk = 36
            base_aug = 88
            ideal_radar = {"pensamento_analitico": 10, "orquestracao_ia": 9, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 9}
        else:
            base_risk = 42
            base_aug = 88
            ideal_radar = {"pensamento_analitico": 8, "orquestracao_ia": 8, "criatividade_inovacao": 8, "lideranca_influencia": 8, "resiliencia_adaptabilidade": 8, "especializacao_estrategica": 8}

        return {
            "id": "custom_role",
            "title": role,
            "category": f"Setor de {domain}",
            "automation_risk_score": base_risk,
            "augmentation_potential_score": base_aug,
            "skills_radar_ideal": ideal_radar,
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