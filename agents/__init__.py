"""
Pacote de Agentes Universais para Diagnóstico de Carreira e Impacto de IA 2030.
Seguindo os princípios de agentes_universais.md.
"""

from .security_reviewer import SecurityReviewerAgent
from .resume_parser import ResumeParserAgent
from .researcher import ResearcherAgent
from .ai_evaluator import AIEvaluatorAgent
from .career_strategist import CareerStrategistAgent

__all__ = [
    "SecurityReviewerAgent",
    "ResumeParserAgent",
    "ResearcherAgent",
    "AIEvaluatorAgent",
    "CareerStrategistAgent",
]
