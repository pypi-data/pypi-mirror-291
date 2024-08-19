import time

import pytest  # noqa: F401
from promptarchitect.engineered_prompt import EngineeredPrompt

# Sample prompt data to use in tests
valid_prompt_content_ollama = """
---
provider: ollama
model: gemma2
output: output.txt
---
What's the capital of The Netherlands?
"""

valid_prompt_content_claude = """
---
provider: anthropic
model: claude-3-5-sonnet-20240620
max_tokens: 100
output: output.txt
---
# Answer this question: What's the capital of The Netherlands?
"""

valid_prompt_content_openai = """
---
provider: openai
model: gpt-4o-mini
max_tokens: 100
output: output.txt
---
# Answer this question: What's the capital of The Netherlands?
"""


# Define fixtures to use in your tests
@pytest.fixture
def valid_prompt_file(tmp_path, request):
    # Get the prompt content passed from the test
    prompt_content = request.param

    # Create the temporary directory and file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "prompt.txt"

    # Write the selected prompt content to the file
    p.write_text(prompt_content)
    return p


@pytest.mark.parametrize(
    "valid_prompt_file",
    [valid_prompt_content_ollama, valid_prompt_content_claude],
    indirect=True,
)
def test_execute(valid_prompt_file):
    ep = EngineeredPrompt(prompt_file_path=str(valid_prompt_file))

    # Test with input_text
    response_text = ep.execute()

    assert "Amsterdam" in response_text, f"Unexpected response: {response_text}"


# Helper function to create a dummy EngineeredPrompt instance
def create_engineered_prompt():
    prompt_file_path = "dummy_prompt_file.json"
    output_path = "text"
    return EngineeredPrompt(prompt_file_path, output_path)


def test_store_to_cache(valid_prompt_file, tmp_path):
    ep = EngineeredPrompt(
        prompt_file_path=str(valid_prompt_file), output_path=str(tmp_path)
    )
    ep.prompt_file.metadata["output"] = "output"
    ep.store_to_cache()
    cache_file = tmp_path / "cache/output.json"
    assert cache_file.exists()


def test_load_from_cache(valid_prompt_file, tmp_path):
    # Set up initial EngineeredPrompt and store to cache
    ep = EngineeredPrompt(
        prompt_file_path=str(valid_prompt_file), output_path=str(tmp_path)
    )
    ep.store_to_cache()

    # Verify that the cache file was created
    cache_file = tmp_path / "cache/output.txt.json"
    assert cache_file.exists(), "Cache file was not created"

    # Create a new instance of EngineeredPrompt and load from cache
    new_ep = EngineeredPrompt(
        prompt_file_path=str(valid_prompt_file), output_path=str(tmp_path)
    )

    # Debugging output before load
    print(f"Attempting to load from cache: {cache_file}")

    # Assert that the cache was loaded successfully
    assert new_ep.load_from_cache(), "Failed to load from cache"

    # Optionally, assert that the loaded metadata matches the stored metadata
    assert new_ep.prompt_file.metadata["output"] == "output.txt"


@pytest.mark.parametrize(
    "valid_prompt_file",
    [valid_prompt_content_ollama],
    indirect=True,
)
def test_context_manager_caching(valid_prompt_file, tmp_path):
    output_path = str(tmp_path)
    cache_expiration_time = 2  # 2 seconds for quick expiration testing

    # First execution, should execute and store in cache
    with EngineeredPrompt(
        prompt_file_path=str(valid_prompt_file),
        output_path=output_path,
        cache_expiration=cache_expiration_time,
    ) as ep:
        response_text = ep.execute()
        assert "Amsterdam" in response_text

    # Ensure cache file exists
    cache_file = tmp_path / "cache" / "output.txt.json"
    assert (
        cache_file.exists()
    ), "Cache file should have been created after the first execution."

    # Cached execution, should load from cache and skip execution
    with EngineeredPrompt(
        prompt_file_path=str(valid_prompt_file),
        output_path=output_path,
        cache_expiration=cache_expiration_time,
    ) as ep:
        response_text = ep.execute()
        assert "Amsterdam" in response_text
        assert cache_file.exists(), "Cache file should still exist."

    # Expire the cache by waiting
    time.sleep(cache_expiration_time + 1)

    # After cache expiration, should re-execute and update cache
    with EngineeredPrompt(
        prompt_file_path=str(valid_prompt_file),
        output_path=output_path,
        cache_expiration=cache_expiration_time,
    ) as ep:
        response_text = ep.execute()
        assert "Amsterdam" in response_text
        assert cache_file.exists(), "Cache file should be updated after re-execution."


def test_to_dict(valid_prompt_file):
    ep = EngineeredPrompt(prompt_file_path=str(valid_prompt_file), output_path="text")
    ep_dict = ep.to_dict()
    assert isinstance(ep_dict, dict)
    assert ep_dict["prompt_file_path"] == str(valid_prompt_file)


def test_from_dict(valid_prompt_file):
    data = {
        "provider": "openai",
        "prompt_file_path": str(valid_prompt_file),
        "output_path": "text",
        "input_file": None,
        "input_text": "",
        "latency": 0.0,
        "cost": 0.0,
        "errors": {},
        "completion": None,
        "completion_type": None,
        "response_message": "",
        "response_text": "",
    }
    ep = EngineeredPrompt.from_dict(data)
    assert ep.prompt_file_path == str(valid_prompt_file)
    assert ep.output_path == "text"
