from pathlib import Path

from promptarchitect import EngineeredPrompt

# Create the output directory if it does not exist
output_directory = Path("output_directory")
output_directory.mkdir(exist_ok=True)

# Define the path to the prompt and input file
prompt_path = Path("prompts/generate_titles_openai.prompt")
input_file_path = Path("input/podcast_description.txt")

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    prompt_file_path=str(prompt_path), output_path="output_directory"
)

# Execute the prompt
response = prompt.execute()

print(response)
