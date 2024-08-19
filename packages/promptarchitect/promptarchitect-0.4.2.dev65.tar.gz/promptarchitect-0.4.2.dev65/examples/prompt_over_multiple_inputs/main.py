from pathlib import Path

from promptarchitect import EngineeredPrompt

# Create the output directory if it does not exist
output_directory = Path("output_directory")
output_directory.mkdir(exist_ok=True)

# Read all prompts from the prompts directory
# And sort them by name
input_files = sorted(Path("input").glob("*.txt"))

# We will read all input files from the input directory
# And use each input file as the input for the prompt
# We'll repeat this process for each input file

# Get all input files from the input directory
for input_file_path in input_files:
    # Create a prompt file for each input file
    # And execute the prompt using the EngineeredPrompt class

    # Initialize the EngineeredPrompt with the prompt file
    # Make sure the different output files are saved in different directories
    output_directory = Path("output_directory") / input_file_path.stem
    prompt = EngineeredPrompt(
        prompt_file_path="prompts/01 - Generate titles.prompt",
        output_path=output_directory,
    )

    # Execute the prompt
    response = prompt.execute(input_file=input_file_path)

    # Show the response from the model
    print(response)
