from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """Enumeration of different task types for prompt engineering."""
    FINANCIAL = "financial"
    TRIP_PLANNING = "trip_planning"
    PDF_ANALYSIS = "pdf_analysis"
    HEALTH_ADVICE = "health_advice"
    PRODUCTIVITY = "productivity"
    GENERAL = "general"


@dataclass
class PromptTemplate:
    """Data class for structured prompt templates."""
    system_prompt: str
    user_prompt_template: str
    context_format: str
    instructions: List[str]
    output_format: Optional[str] = None


class PromptEngineer:
    """Prompt engineer with structured templates and context-aware prompting."""
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[TaskType, PromptTemplate]:
        """Initialize prompt templates for different task types."""
        return {
            TaskType.FINANCIAL: PromptTemplate(
                system_prompt="You are an expert financial advisor with deep knowledge of personal and business finance. You provide accurate, actionable financial advice based on the provided financial data.",
                user_prompt_template="Based on the following financial data, please answer this question: {query}",
                context_format="Financial Data:\n{context}",
                instructions=[
                    "Analyze the financial data thoroughly",
                    "Provide specific, actionable recommendations",
                    "Include relevant financial metrics and trends",
                    "Consider both short-term and long-term implications",
                    "If data is insufficient, clearly state what additional information is needed"
                ],
                output_format="Provide your analysis in a structured format with clear sections for analysis, recommendations, and next steps."
            ),
            
            TaskType.TRIP_PLANNING: PromptTemplate(
                system_prompt="You are a professional travel planner with extensive knowledge of destinations, logistics, and travel best practices. You create comprehensive, personalized travel itineraries.",
                user_prompt_template="Please help plan this trip: {query}",
                context_format="Travel Information:\n{context}",
                instructions=[
                    "Consider weather conditions and seasonal factors",
                    "Include safety considerations and local customs",
                    "Provide practical logistics (transportation, accommodation)",
                    "Suggest activities that match the traveler's interests",
                    "Include budget considerations and booking recommendations"
                ],
                output_format="Structure your response with sections for itinerary, logistics, recommendations, and important notes."
            ),
            
            TaskType.PDF_ANALYSIS: PromptTemplate(
                system_prompt="You are a document analysis expert who can extract key information, summarize content, and provide insights from various types of documents.",
                user_prompt_template="Please analyze this document content: {query}",
                context_format="Document Content:\n{context}",
                instructions=[
                    "Identify key themes and main points",
                    "Extract important facts and figures",
                    "Provide a clear summary of the content",
                    "Highlight any actionable items or recommendations",
                    "Note any areas that require further clarification"
                ],
                output_format="Provide your analysis with sections for summary, key points, insights, and recommendations."
            ),
            
            TaskType.HEALTH_ADVICE: PromptTemplate(
                system_prompt="You are a health and wellness expert who provides evidence-based advice on nutrition, fitness, and general wellness. Always recommend consulting healthcare professionals for medical concerns.",
                user_prompt_template="Please provide health advice for: {query}",
                context_format="Health Information:\n{context}",
                instructions=[
                    "Provide evidence-based recommendations",
                    "Consider individual health factors and preferences",
                    "Include safety considerations and contraindications",
                    "Suggest practical, sustainable approaches",
                    "Always recommend consulting healthcare professionals when appropriate"
                ],
                output_format="Structure your advice with sections for recommendations, safety considerations, and next steps."
            ),
            
            TaskType.PRODUCTIVITY: PromptTemplate(
                system_prompt="You are a productivity expert who helps optimize workflows, time management, and organizational systems for maximum efficiency and effectiveness.",
                user_prompt_template="Please help with this productivity challenge: {query}",
                context_format="Productivity Context:\n{context}",
                instructions=[
                    "Analyze the current workflow or situation",
                    "Identify bottlenecks and improvement opportunities",
                    "Suggest practical, implementable solutions",
                    "Consider tools and techniques that can help",
                    "Provide step-by-step action plans"
                ],
                output_format="Provide your recommendations with sections for analysis, solutions, implementation steps, and tools/resources."
            ),
            
            TaskType.GENERAL: PromptTemplate(
                system_prompt="You are a helpful AI assistant with broad knowledge and expertise. You provide accurate, informative, and helpful responses to user queries.",
                user_prompt_template="Please help with: {query}",
                context_format="Relevant Information:\n{context}",
                instructions=[
                    "Provide accurate and helpful information",
                    "Use the provided context when relevant",
                    "Be clear and concise in your explanations",
                    "Suggest additional resources when appropriate",
                    "Ask clarifying questions if needed"
                ]
            )
        }
    
    def create_structured_prompt(self, query: str, contexts: List[str], task_type: TaskType = TaskType.GENERAL) -> str:
        """Create a structured prompt with proper formatting and instructions."""
        template = self.templates[task_type]
        
        # Format context
        formatted_context = template.context_format.format(
            context="\n".join([f"- {ctx}" for ctx in contexts]) if contexts else "No specific context provided."
        )
        
        # Create user prompt
        user_prompt = template.user_prompt_template.format(query=query)
        
        # Build the complete prompt
        prompt_parts = [
            template.system_prompt,
            "",
            formatted_context,
            "",
            user_prompt,
            "",
            "Instructions:",
            *[f"- {instruction}" for instruction in template.instructions]
        ]
        
        if template.output_format:
            prompt_parts.extend([
                "",
                "Output Format:",
                template.output_format
            ])
        
        return "\n".join(prompt_parts)
    
    def create_financial_prompt(self, query: str, financial_data: List[str]) -> str:
        """Create a specialized financial analysis prompt."""
        return self.create_structured_prompt(query, financial_data, TaskType.FINANCIAL)
    
    def create_trip_prompt(self, query: str, travel_info: List[str]) -> str:
        """Create a specialized trip planning prompt."""
        return self.create_structured_prompt(query, travel_info, TaskType.TRIP_PLANNING)
    
    def create_pdf_prompt(self, query: str, document_content: List[str]) -> str:
        """Create a specialized PDF analysis prompt."""
        return self.create_structured_prompt(query, document_content, TaskType.PDF_ANALYSIS)
    
    def create_health_prompt(self, query: str, health_info: List[str]) -> str:
        """Create a specialized health advice prompt."""
        return self.create_structured_prompt(query, health_info, TaskType.HEALTH_ADVICE)
    
    def create_productivity_prompt(self, query: str, productivity_context: List[str]) -> str:
        """Create a specialized productivity prompt."""
        return self.create_structured_prompt(query, productivity_context, TaskType.PRODUCTIVITY)
    
    def create_general_prompt(self, query: str, context: List[str]) -> str:
        """Create a general-purpose prompt."""
        return self.create_structured_prompt(query, context, TaskType.GENERAL)


# Initialize global prompt engineer
prompt_engineer = PromptEngineer() 