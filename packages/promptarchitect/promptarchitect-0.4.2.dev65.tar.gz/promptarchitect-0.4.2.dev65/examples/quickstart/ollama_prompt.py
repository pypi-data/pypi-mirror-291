from pathlib import Path

from promptarchitect import EngineeredPrompt

# Create the output directory if it does not exist
output_directory = Path("output_directory")
output_directory.mkdir(exist_ok=True)

# Define the path to the prompt and input file
prompt_path = Path("prompts/generate_titles_ollama.prompt")

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    prompt_file_path=str(prompt_path), output_path="output_directory"
)

# Download the model in this case gemma2, but you can use any other model
# supported by Ollama (see https://ollama.com/library)
# Only the first time you run the prompt you need to download the model
prompt.completion.download_model("gemma2")
# Execute the prompt
response = prompt.execute()

print(response)
