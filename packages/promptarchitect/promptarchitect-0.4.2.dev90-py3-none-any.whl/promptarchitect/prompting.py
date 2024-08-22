"""
This module contains the `EngineeredPrompt` class that represents a validated prompt and associated input.
"""

import json
import logging
import os
from functools import cache
from typing import Dict, Optional

import chevron
from pydantic import BaseModel

from promptarchitect.completions import create_completion
from promptarchitect.specification import EngineeredPromptSpecification, PromptInput

logger = logging.getLogger(__name__)


class PromptOutput(BaseModel):
    response: str
    input_tokens: int
    output_tokens: int
    completion: object


class EngineeredPrompt:
    """
    The engineered prompt. A validated, well thought-out prompt that is easy to use in your application.

    We support running and rendering the prompt in the specification in your application.
    This class is also used during validation to run the prompt.

    Attributes
    ----------
    specification : EngineeredPromptSpecification
        The specification for the prompt.
    """

    def __init__(
        self,
        specification: EngineeredPromptSpecification = None,
        prompt_file: str = None,
        output_path: str = None,
    ):
        """Initialize the engineered prompt with the specification.

        Parameters
        ----------
        specification : EngineeredPromptSpecification
            The specification for the prompt.

        prompt_file : str
            The path to a prompt file.

        output_path : str
            The path to the output directory if you want to save the response to a file.
        """

        # Convert in the case of a Path object
        self.prompt_file = str(prompt_file) if prompt_file is not None else None
        self.output_path = str(output_path) if output_path is not None else None

        if specification is None and prompt_file is None:
            raise ValueError("Either specification or prompt_file must be provided.")

        if specification is not None and prompt_file is not None:
            raise ValueError(
                "Only one of specification or prompt_file can be provided."
            )

        if self.prompt_file is not None:
            self.specification = EngineeredPromptSpecification.from_file(
                self.prompt_file
            )
        else:
            self.specification = specification

        # Initialize the completion, so for Open Source models we can download the model
        self.completion = create_completion(
            self.specification.metadata.provider,
            self.specification.metadata.model,
            self.specification.metadata,
            self.specification.metadata.system_role,
        )

    def execute(
        self,
        input_text: Optional[str] = None,
        input_file: Optional[str] = None,
        properties: Optional[Dict[str, object]] = None,
    ) -> str:
        """
        Executes the prompt with the input text or input file.

        The output of this operation is not cached.

        This function is for backwards compatibility with the previous version of the library.

        Returns
        -------
        str
            The output of the prompt.
        """

        return self.run(input_text, input_file, properties)

    @cache
    def run(
        self,
        input_text: Optional[str] = None,
        input_file: Optional[str] = None,
        properties: Optional[Dict[str, object]] = None,
    ) -> str:
        """
        Runs the prompt with the input text or input file.

        The output of this operation is automatically cached until the application is closed.

        Parameters
        ----------
        input_text : str, optional
            The input text to the prompt.
        input_file : str, optional
            The path to the input file.

        Returns
        -------
        str
            The output of the prompt.
        """

        rendered_input = self.render(input_text, input_file, properties)

        response = self.completion.completion(rendered_input)

        if self.output_path is not None:
            output_file = os.path.join(
                self.output_path, self.specification.metadata.output
            )
            self.write_output_to_file(response, output_file)

        return response

    def write_output_to_file(self, response: str, output_file: str):
        """
        Writes the response to a file in the format as specified in the specification.

        Parameters
        ----------
        response : str
            The response from the prompt.
        output_file : str
            The path to the output file.
        """

        try:
            # Create base path if it does not exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            # Check the output format in the specification
            if self.specification.metadata.output_format == "json":
                # Write the response to a JSON file
                with open(output_file, "w") as file:
                    json.dump({"response": response}, file)

            else:
                # Consider the output format to be text
                with open(output_file, "w") as file:
                    file.write(response)

        except Exception as e:
            logger.error(f"Error writing output to file: {e}")

    def render(
        self,
        input_text: Optional[str] = None,
        input_file: Optional[str] = None,
        properties: Optional[Dict[str, object]] = None,
    ) -> str:
        """
        Render the prompt with the input_text

        We'll read the input_file if is is provided. The input file will provide this method
        with the input_text and properties. If you specify the input_text you can optionally
        include extra properties you need to render the prompt.

        Specifying properties with an `input_file` is not supported. You also can't provide
        both `input_text` and `input_file`. You must provide one or the other.

        Parameters
        ----------
        input_text : str, optional
            The input text to the prompt.
        input_file : str, optional
            The path to the input file.
        properties : Dict[str, object], optional
            Additional properties for the prompt input.

        Returns
        -------
        str
            The rendered prompt.
        """
        input_text, properties = self._determine_input_text_order(
            input_text, input_file
        )

        prompt = self.specification.prompt
        # Add a input property to prompt if it is not already in the prompt
        # Otherwise the input will not be rendered in the prompt
        if "{{input}}" not in self.specification.prompt:
            prompt = f"{self.specification.prompt} {{{{input}}}}"

        # We'll render the prompt with the input_text and properties
        template_properties = properties.copy() if properties is not None else {}
        template_properties["input"] = input_text

        return chevron.render(prompt, template_properties)

    def _determine_input_text_order(self, input_text: str, input_file: str) -> str:
        # One of the input_text, input_file or the input must be provided in the specification

        # If none of the input_text, input_file or specification are provided, we'll raise an error
        if (
            input_text is None
            and input_file is None
            and self.specification.metadata.input is None
        ):
            raise ValueError(
                "Either input_text, input_file or input specification in the prompt must be provided."
            )

        if (
            input_text is None
            and input_file is None
            and self.specification.metadata.input is None
        ):
            raise ValueError(
                "Either input_text, input_file or input in the metadata must be provided."
            )

        if input_text is not None and input_file is not None:
            raise ValueError("Only one of input_text or input_file can be provided.")

        # This is the order to pick the input for the rendering of the prompt
        # 1. input_text
        # 2. input_file
        # 3. self.specification.metadata.input

        properties = {}
        if input_text is None:
            input_file = (
                input_file
                if input_file is not None
                else self.specification.metadata.input
            )

            if input_file is not None:
                prompt_input = PromptInput.from_file(input_file)

                properties = prompt_input.properties
                input_text = prompt_input.input

        return input_text, properties
