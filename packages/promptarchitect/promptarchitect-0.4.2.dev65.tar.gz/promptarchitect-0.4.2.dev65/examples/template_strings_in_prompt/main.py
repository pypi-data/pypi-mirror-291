from pathlib import Path

from promptarchitect import EngineeredPrompt

# Define the path to the prompt and input file
prompt_path = Path("generate_titles_ollama.prompt")

# Create the output directory if it does not exist
output_directory = Path(".")
output_directory.mkdir(exist_ok=True)


# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    prompt_file_path=str(prompt_path), output_path=output_directory
)

# The prompt file has two template strings we want to replace
# number and type_of_media
prompt.prompt_file.substitute_prompt(number="3", type_of_media="podcast")

# Execute the prompt
response = prompt.execute()

print("============= 3 podcast titles =============")
# See the response
print(response)

# Let's change the number and type_of_media and execute the prompt again
prompt.prompt_file.substitute_prompt(number="5", type_of_media="blog post")

# Execute the prompt again but with the new template strings
response = prompt.execute()

print("============= 5 blog post titles =============")
# See the response
print(response)
