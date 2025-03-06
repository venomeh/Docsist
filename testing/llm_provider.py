import os
from typing import Dict, List, Optional, Any, Union
import openai
from openai import OpenAI

class LLMProvider:
    """
    A universal adapter for different LLM providers that maintains OpenAI API compatibility
    """
    def __init__(self, provider: str = "deepseek"):
        """
        Initialize the LLM provider
        
        Args:
            provider: The provider to use (deepseek, groq, openai, etc.)
        """
        self.provider = provider.lower()
        
        # Configure the client based on the provider
        if self.provider == "openai":
            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            self.base_url = None
        elif self.provider == "deepseek":
            # DeepSeek offers an OpenAI-compatible API
            self.client = OpenAI(
                api_key=os.environ.get("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com/v1"
            )
        elif self.provider == "groq":
            # For Groq, we can use their Python client which is OpenAI-compatible
            import groq
            self.client = groq.Client(api_key=os.environ.get("GROQ_API_KEY"))
        elif self.provider == "ollama":
            # For local Ollama, we use OpenAI client with custom base URL
            self.client = OpenAI(
                api_key="ollama",  # Ollama doesn't need a real API key
                base_url="http://localhost:11434/v1"
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        # Set default models based on provider
        self.models = self._get_default_models()
    
    def _get_default_models(self) -> Dict[str, str]:
        """Get the default models for the current provider"""
        if self.provider == "openai":
            return {
                "chat": "gpt-3.5-turbo",
                "embedding": "text-embedding-ada-002"
            }
        elif self.provider == "deepseek":
            return {
                "chat": "deepseek-chat",
                "embedding": "deepseek-embedding"
            }
        elif self.provider == "groq":
            return {
                "chat": "llama3-70b-8192",
                "embedding": "llama3-70b-8192"  # Groq might not have a dedicated embedding model
            }
        elif self.provider == "ollama":
            return {
                "chat": "llama3",
                "embedding": "llama3"
            }
        return {}
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a chat completion using the configured provider
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model to use (defaults to provider's default chat model)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            Response dictionary with the same structure as OpenAI's response
        """
        model = model or self.models["chat"]
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response
        except Exception as e:
            print(f"Error in chat completion: {e}")
            # Return a minimal compatible response structure
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"Error: {str(e)}"
                        },
                        "index": 0
                    }
                ]
            }
    
    def get_embedding(
        self,
        text: Union[str, List[str]],
        model: Optional[str] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for the given text
        
        Args:
            text: Text or list of texts to embed
            model: Model to use (defaults to provider's default embedding model)
            
        Returns:
            List of embedding vectors
        """
        model = model or self.models["embedding"]
        
        try:
            if isinstance(text, str):
                text = [text]
                
            response = self.client.embeddings.create(
                model=model,
                input=text
            )
            
            # Extract embeddings from the response
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            print(f"Error in embedding: {e}")
            # Return empty embeddings as fallback
            return [[0.0] * 1536] * len(text if isinstance(text, list) else [text])