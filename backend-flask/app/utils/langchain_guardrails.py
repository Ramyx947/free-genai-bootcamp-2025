"""LangChain-based guardrails for Romanian language learning."""

import re
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from flask import current_app, has_app_context


class LangChainRomanianGuardrails:
    """Guardrails implementation using LangChain for Romanian language learning."""

    def __init__(self, api_key=None):
        """Initialize the guardrails with Romanian language rules."""
        # Common Romanian diacritic words that are often misspelled
        self.diacritic_words = {
            "tara": "țară",
            "Bucuresti": "București",
            "Timisoara": "Timișoara",
            "Iasi": "Iași",
            "Brasov": "Brașov",
            "romana": "română",
            "Constanta": "Constanța",
            "Romaniei": "României",
        }

        # Formality mappings (informal -> formal)
        self.formality_mappings = {
            "tu ești": "dumneavoastră sunteți",
            "tu ai": "dumneavoastră aveți",
            "tu vrei": "dumneavoastră vreți",
            "tu poți": "dumneavoastră puteți",
            "tu mergi": "dumneavoastră mergeți",
            "tu vii": "dumneavoastră veniți",
        }

        # Initialize LangChain components
        if api_key is None and has_app_context():
            api_key = current_app.config.get("OPENAI_API_KEY")

        self.llm = ChatOpenAI(
            temperature=0.1, model="gpt-3.5-turbo", api_key=api_key or "sk-test-key"
        )

        # Formality correction chain
        formality_template = PromptTemplate.from_template(
            """You are a Romanian language expert.
            Convert the following text to {formality} Romanian:

            Text: {text}
            Converted text:"""
        )

        self.formality_chain = formality_template | self.llm | StrOutputParser()

        # Content moderation chain
        moderation_template = PromptTemplate.from_template(
            """You are a content moderator for a Romanian language learning application.
            Analyze the following text and determine if it contains inappropriate content.
            If the text is safe, respond with "SAFE".
            If the text contains inappropriate content, respond with "UNSAFE: <reason>".
            Text: {text}
            Moderation result:"""
        )

        self.moderation_chain = moderation_template | self.llm | StrOutputParser()

    def validate_input(self, text: str) -> bool:
        """Validate user input for Romanian language learning queries."""
        if not text or len(text.strip()) == 0:
            raise ValueError("Input text cannot be empty")

        # Check for minimum length
        if len(text.split()) < 2:
            raise ValueError("Input text is too short")

        # Check for maximum length
        if len(text.split()) > 500:
            raise ValueError("Input text is too long (maximum 500 words)")

        # Run content moderation
        moderation_result = self.moderation_chain.invoke({"text": text})

        if moderation_result.startswith("UNSAFE"):
            reason = (
                moderation_result.split(":", 1)[1].strip()
                if ":" in moderation_result
                else "inappropriate content"
            )
            raise ValueError(f"Input contains {reason}")

        return True

    def process_output(self, text: str, formal: bool = True) -> str:
        """Process AI output to ensure quality and appropriate formality."""
        if not text:
            return "No response generated"

        # Fix diacritics
        for word, correct in self.diacritic_words.items():
            text = re.sub(r"\b" + word + r"\b", correct, text, flags=re.IGNORECASE)

        # Apply formality correction if needed
        if formal:
            try:
                text = self.formality_chain.invoke(
                    {"text": text, "formality": "formal"}
                )
            except Exception:
                # Fallback to simple replacement if LangChain fails
                for informal, formal_text in self.formality_mappings.items():
                    text = text.replace(informal, formal_text)

        return text
