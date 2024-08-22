"""
This module contains the `EngineeredPrompt` class that represents a validated prompt and associated input.
"""

import logging
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
    ):
        """Initialize the engineered prompt with the specification.

        Parameters
        ----------
        specification : EngineeredPromptSpecification
            The specification for the prompt.

        prompt_file : str
            The path to a prompt file.
        """

        if specification is None and prompt_file is None:
            raise ValueError("Either specification or prompt_file must be provided.")

        if specification is not None and prompt_file is not None:
            raise ValueError(
                "Only one of specification or prompt_file can be provided."
            )

        if prompt_file is not None:
            self.specification = EngineeredPromptSpecification.from_file(prompt_file)
        else:
            self.specification = specification

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

        self.completion = create_completion(
            self.specification.metadata.provider,
            self.specification.metadata.model,
            self.specification.metadata,
            self.specification.metadata.system_role,
        )

        rendered_input = self.render(input_text, input_file, properties)

        return self.completion.completion(rendered_input)

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

        if input_text is None and input_file is None:
            raise ValueError("Either input_text or input_file must be provided.")

        if input_text is not None and input_file is not None:
            raise ValueError("Only one of input_text or input_file can be provided.")

        if input_file is not None and properties is not None:
            raise ValueError(
                "Properties are not supported when loading input from file."
            )

        if input_file is not None:
            input_sample = PromptInput.from_file(input_file)

            properties = input_sample.properties
            input_text = input_sample.input

        template_properties = properties.copy() if properties is not None else {}
        template_properties["input"] = input_text

        return chevron.render(self.specification.prompt, template_properties)
