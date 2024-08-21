from pathlib import Path

from promptarchitect import EngineeredPrompt

# Define the path to the prompt and input file
prompt_path = Path("prompts/generate_titles_ollama.prompt")

# Create the output directory if it does not exist
output_directory = Path("output_directory")
output_directory.mkdir(exist_ok=True)

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    prompt_file_path=str(prompt_path), output_path="output_directory"
)

# Get metadata from the prompt file
# Including custom metadata set in the prompt file
if prompt.prompt_file.metadata.get("my_key"):
    print("Metadata key exists, and we can use it to control our flow")

# Get all the metadata from the prompt file
print(prompt.prompt_file.metadata)
