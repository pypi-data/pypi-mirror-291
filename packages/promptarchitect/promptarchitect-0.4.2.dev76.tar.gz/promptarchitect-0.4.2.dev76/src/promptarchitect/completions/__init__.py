from promptarchitect.completions.core import Completion
from promptarchitect.ollama_completion import OllamaCompletion
from promptarchitect.openai_completion import OpenAICompletion
from promptarchitect.claude_completion import ClaudeCompletion


def create_completion(provider: str, model: str, system_role: str) -> Completion:
    if provider == "ollama":
        return OllamaCompletion(system_role, model)
    elif provider == "openai":
        return OpenAICompletion(system_role, model)
    elif provider == "claude":
        return ClaudeCompletion(system_role, model)
    else:
        raise ValueError(f"Provider {provider} is not supported.")
