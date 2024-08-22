import pytest
from promptarchitect.prompting import EngineeredPrompt
from promptarchitect.specification import (
    EngineeredPromptMetadata,
    EngineeredPromptSpecification,
)

valid_prompt_content = """
---
provider: openai
model: gpt-4o
input: input.txt
output: output.txt
---
This is a test prompt.
"""


# Define fixtures to use in your tests
@pytest.fixture
def valid_prompt_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "prompt.txt"
    p.write_text(valid_prompt_content)
    return p


@pytest.fixture
def valid_specification():
    specification = EngineeredPromptSpecification(
        metadata=EngineeredPromptMetadata(
            provider="openai",
            model="gpt-4o-mini",
            input="input.txt",
        ),
        prompt="Give a list of 5 blog post titles for a post about {{input}}",
    )

    return specification


def test_initialize_specification(valid_specification):
    engineered_prompt = EngineeredPrompt(specification=valid_specification)

    assert engineered_prompt.specification == valid_specification


def test_initialize__from_file(valid_prompt_file):
    engineered_prompt = EngineeredPrompt(prompt_file=str(valid_prompt_file))

    assert engineered_prompt.specification.metadata.provider == "openai"
    assert engineered_prompt.specification.metadata.model == "gpt-4o"


def test_initialize__from_file_to_specification(valid_prompt_file):
    engineered_prompt = EngineeredPrompt(
        EngineeredPromptSpecification.from_file(str(valid_prompt_file))
    )

    assert engineered_prompt.specification.metadata.provider == "openai"
    assert engineered_prompt.specification.metadata.model == "gpt-4o"


def test_initialize_errors(valid_prompt_file):
    # Test that ValueError is raised when both specification and prompt_file are None
    with pytest.raises(ValueError):
        EngineeredPrompt()

    # Test that ValueError is raised when both specification and prompt_file are provided
    with pytest.raises(ValueError):
        EngineeredPrompt(
            specification=EngineeredPromptSpecification.from_file(
                str(valid_prompt_file)
            ),
            prompt_file=str(valid_prompt_file),
        )


def test_run(valid_specification):
    engineered_prompt = EngineeredPrompt(specification=valid_specification)
    result = engineered_prompt.run("Prompt testing")

    assert result is not None


def test_run_errors(valid_prompt_file):
    engineered_prompt = EngineeredPrompt(prompt_file=valid_prompt_file)

    # Test that ValueError is raised when both input_text, input_file are both provided
    # besides the prompt file
    with pytest.raises(ValueError):
        engineered_prompt.run(input_text="Prompt testing", input_file="input.txt")
