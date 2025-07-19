import os
import re
from typing import List, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class HumanizeTextWithGroq:
    """
    A class to humanize AI-generated text using Groq API.
    Processes text paragraph by paragraph with multiple iterations for better humanization.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        """
        Initialize the humanizer with Groq API.
        
        Args:
            api_key: Groq API key (if None, will try to get from environment)
            model: Groq model to use for humanization
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be provided or set in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
    
    def _detect_paragraphs(self, text: str) -> List[str]:
        """
        Detect paragraphs in the text using various methods.
        
        Args:
            text: Input text to split into paragraphs
            
        Returns:
            List of paragraph strings
        """
        # Clean up the text first
        text = text.strip()
        
        # Split by double newlines first (most common paragraph separator)
        paragraphs = re.split(r'\n\s*\n', text)
        
        # If no double newlines found, split by single newlines
        if len(paragraphs) == 1:
            paragraphs = text.split('\n')
        
        # Further split very long paragraphs (more than 500 characters)
        final_paragraphs = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            # If paragraph is very long, try to split it at sentence boundaries
            if len(para) > 500:
                # Split by periods followed by space and capital letter (sentence boundaries)
                sentences = re.split(r'(?<=\.)\s+(?=[A-Z])', para)
                
                # Group sentences into smaller paragraphs (max ~300 chars each)
                current_chunk = ""
                for sentence in sentences:
                    if len(current_chunk + sentence) > 300 and current_chunk:
                        final_paragraphs.append(current_chunk.strip())
                        current_chunk = sentence + " "
                    else:
                        current_chunk += sentence + " "
                
                if current_chunk.strip():
                    final_paragraphs.append(current_chunk.strip())
            else:
                final_paragraphs.append(para)
        
        return [p for p in final_paragraphs if p.strip()]
    
    def _humanize_paragraph(self, paragraph: str, iteration: int = 1) -> str:
        """
        Humanize a single paragraph using Groq API.
        
        Args:
            paragraph: Paragraph text to humanize
            iteration: Current iteration number (affects the prompt strategy)
            
        Returns:
            Humanized paragraph text
        """
        # Different prompts for different iterations
        if iteration == 1:
            system_prompt = """You are an expert text humanizer. Your task is to rewrite AI-generated text to make it sound more natural, conversational, and human-like.

Key requirements:
1. Make the text easily readable (aim for Flesch Reading Ease score of 80+)
2. Use simple, clear language that flows naturally
3. Avoid robotic or overly formal language
4. Add natural transitions and conversational elements
5. Vary sentence length and structure
6. Remove AI-typical phrases like "Furthermore", "Moreover", "In conclusion"
7. Make it sound like a knowledgeable human wrote it
8. Preserve all important information and meaning

IMPORTANT: Only return the humanized text. Do not include any explanations, introductions, or phrases like "Here is the humanized text". Just provide the rewritten content directly.

Focus on making the text accessible and engaging while maintaining accuracy."""

        elif iteration == 2:
            system_prompt = """You are a skilled editor focused on making text more human and relatable. Refine the text further by:

1. Adding more personality and warmth to the writing
2. Using more conversational connectors ("And", "But", "So", "Plus")
3. Including rhetorical questions or direct reader engagement where appropriate
4. Simplifying complex sentences further
5. Adding subtle emotional context where relevant
6. Using more active voice
7. Making the tone more approachable and less academic

IMPORTANT: Only return the refined text. Do not include any explanations, introductions, or phrases like "Here is the refined text". Just provide the improved content directly.

Keep the core message intact while making it sound like natural human communication."""

        else:  # iteration 3+
            system_prompt = """You are a final polish editor. Make the text sound completely natural and human by:

1. Ensuring perfect flow between sentences
2. Adding natural speech patterns and rhythms
3. Using everyday language instead of formal terms
4. Making sure it sounds like spoken conversation when read aloud
5. Adding subtle emphasis and natural pauses
6. Removing any remaining artificial-sounding phrases
7. Ensuring the text feels warm and engaging

IMPORTANT: Only return the final polished text. Do not include any explanations, introductions, or phrases like "Here is the final version". Just provide the polished content directly.

This is the final pass - make it sound like a friendly, knowledgeable person explaining something."""

        user_prompt = f"Please humanize this text according to the guidelines above:\n\n{paragraph}"
        
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=2000
            )
            
            return completion.choices[0].message.content.strip()
        
        except Exception as e:
            # Return original paragraph if error occurs (silently handle errors)
            return paragraph
    
    def humanize_text(self, text: str, n_iterations: int = 2) -> str:
        """
        Humanize the entire text by processing paragraphs with multiple iterations.
        
        Args:
            text: Input text to humanize
            n_iterations: Number of humanization passes (1-5 recommended)
            
        Returns:
            Fully humanized text
        """
        if not text.strip():
            return text
        
        # Validate n_iterations
        n_iterations = max(1, min(n_iterations, 5))  # Limit between 1-5
        
        # Detect paragraphs
        paragraphs = self._detect_paragraphs(text)
        
        if not paragraphs:
            return text
        
        # Process each paragraph through multiple iterations
        humanized_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            current_paragraph = paragraph
            
            # Apply multiple iterations of humanization
            for iteration in range(1, n_iterations + 1):
                current_paragraph = self._humanize_paragraph(current_paragraph, iteration)
            
            humanized_paragraphs.append(current_paragraph)
        
        # Join paragraphs back together with double newlines
        result = '\n\n'.join(humanized_paragraphs)
        
        return result
    
    def quick_humanize(self, text: str) -> str:
        """
        Quick single-pass humanization for faster processing.
        
        Args:
            text: Input text to humanize
            
        Returns:
            Humanized text
        """
        return self.humanize_text(text, n_iterations=1)


# Example usage and testing
if __name__ == "__main__":
    # Test the humanizer
    sample_text = """
    Artificial intelligence represents a transformative technological advancement that has the potential to revolutionize numerous industries. Furthermore, machine learning algorithms enable systems to learn from data and improve their performance over time. Moreover, the implementation of AI solutions can significantly enhance operational efficiency and decision-making processes.

    In conclusion, organizations that strategically integrate artificial intelligence into their workflows will likely gain competitive advantages. Additionally, the continuous evolution of AI technologies suggests that future applications will be even more sophisticated and capable.
    """
    
    try:
        # Initialize the humanizer
        humanizer = HumanizeTextWithGroq()
        
        print("Original text:")
        print(sample_text)
        print("\n" + "="*50 + "\n")
        
        # Humanize with 2 iterations
        humanized = humanizer.humanize_text(sample_text, n_iterations=2)
        
        print("Humanized text:")
        print(humanized)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have GROQ_API_KEY set in your environment variables.")