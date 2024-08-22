import pytest
from promptarchitect.engineered_prompt import EngineeredPrompt
from promptarchitect.specification import (
    EngineeredPromptSpecification,
    EngineeredPromptMetadata,
    Limits,
    PropertyTestSpecification,
)


@pytest.fixture
def valid_specification():
    specification = EngineeredPromptSpecification(
        metadata=EngineeredPromptMetadata(
            provider="openai",
            model="gpt-4o-mini",
            tests={
                "test_limits": PropertyTestSpecification(
                    unit="lines",
                    limit=Limits(min=1, max=5),
                )
            },
        ),
        prompt="Give a list of 5 blog post titles for a post about {{input}}",
    )

    return specification


def test_initialize(valid_specification):
    engineered_prompt = EngineeredPrompt(specification=valid_specification)

    assert engineered_prompt.specification == valid_specification


def test_run(valid_specification):
    engineered_prompt = EngineeredPrompt(specification=valid_specification)
    result = engineered_prompt.run("Prompt testing")

    assert result is not None
