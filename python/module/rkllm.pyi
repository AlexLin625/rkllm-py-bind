from typing import List, Tuple, Callable, Optional, Union, overload
from typing import Any

# Python type definitions for rkllm module
# Generated based on the C++ binding in bind.cpp

"""RKLLM Python bindings"""

class RKLLMParam:
    """Parameters for configuring an RKLLM instance."""
    
    def __init__(self) -> None: ...
    
    @property
    def model_path(self) -> str: ...
    
    @model_path.setter
    def model_path(self, value: str) -> None: ...
    
    max_context_len: int  # Maximum number of tokens in the context window
    max_new_tokens: int   # Maximum number of new tokens to generate
    top_k: int            # Top-K sampling parameter for token generation
    n_keep: int           # Number of KV cache to keep at the beginning when shifting context window
    top_p: float          # Top-P (nucleus) sampling parameter
    temperature: float    # Sampling temperature, affecting the randomness of token selection
    repeat_penalty: float # Penalty for repeating tokens in generation
    frequency_penalty: float  # Penalizes frequent tokens during generation
    presence_penalty: float   # Penalizes tokens based on their presence in the input
    mirostat: int         # Mirostat sampling strategy flag (0 to disable)
    mirostat_tau: float   # Tau parameter for Mirostat sampling
    mirostat_eta: float   # Eta parameter for Mirostat sampling
    skip_special_token: bool  # Whether to skip special tokens during generation
    is_async: bool        # Whether to run inference asynchronously

class RKLLMInput:
    """Represents different types of input to the LLM."""
    pass  # This class doesn't have any directly accessible properties in Python

class RKLLMWrapperBase:
    """Base class for RKLLM inference."""
    
    def __init__(self, param: RKLLMParam) -> None: ...
    
    def init(self) -> bool:
        """Initialize the LLM with the provided parameters.
        
        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        ...
    
    def abort(self) -> bool:
        """Abort an ongoing inference process.
        
        Returns:
            bool: True if abort was successful, False otherwise.
        """
        ...
    
    def infer(self, input: RKLLMInput) -> bool:
        """Run inference with the given input.
        
        Args:
            input: The input for the LLM.
            
        Returns:
            bool: True if inference was started successfully, False otherwise.
        """
        ...
    
    def enablePromptCache(self, cache_path: str, params: Any) -> bool:
        """Enable caching of prompts to improve performance for repeated queries.
        
        Args:
            cache_path: Path to store the prompt cache.
            params: Prompt cache parameters.
            
        Returns:
            bool: True if enabling cache was successful, False otherwise.
        """
        ...
    
    def disablePromptCache(self) -> bool:
        """Disable prompt caching.
        
        Returns:
            bool: True if cache was disabled successfully, False otherwise.
        """
        ...

    def setPromptTemplate(self, systemPrompt: str, userPromptPrefix: str, userPromptSuffix: str) -> bool:
        """Set the prompt template for the LLM.

        Args:
            systemPrompt: The system prompt template.
            userPromptPrefix: The prefix for the user prompt.
            userPromptSuffix: The suffix for the user prompt.

        Returns:
            bool: True if setting the prompt template was successful, False otherwise.
        """
        ...
    
    def onInferError(self) -> None:
        """Called when an inference error occurs. Must be implemented by subclasses."""
        ...
    
    def onInferToken(self, token: str) -> None:
        """Called when a new token is generated. Must be implemented by subclasses.
        
        Args:
            token: The generated token as text.
        """
        ...
    
    def onInferFinished(self) -> None:
        """Called when inference is completed. Must be implemented by subclasses."""
        ...

    def set

class RKLLMDataUtils:
    """Utility class for creating different types of inputs for RKLLM."""
    
    @staticmethod
    def text_input(text: str) -> RKLLMInput:
        """Create a text-based input for the LLM.
        
        Args:
            text: The prompt text.
            
        Returns:
            RKLLMInput: An input object configured with the text prompt.
        """
        ...
    
    @staticmethod
    def token_input(input_ids: List[int]) -> RKLLMInput:
        """Create a token-based input for the LLM.
        
        Args:
            input_ids: List of token IDs.
            
        Returns:
            RKLLMInput: An input object configured with the token IDs.
        """
        ...
    
    @staticmethod
    def embed_input(embed: List[float]) -> RKLLMInput:
        """Create an embedding-based input for the LLM.
        
        Args:
            embed: List of embedding values.
            
        Returns:
            RKLLMInput: An input object configured with the embeddings.
        """
        ...

def rkllm_create_default_params() -> RKLLMParam:
    """Create a RKLLMParam object with default values.
    
    Returns:
        RKLLMParam: A parameter object with default values.
    """
    ...