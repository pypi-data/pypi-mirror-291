## 6.1 Key Runtime Scenarios

### Scenario 6: Template String Substitution in Prompts

1. **Trigger**: A user initiates prompt execution and provides specific values to substitute into the template strings within the prompt file.
2. **Substitution**: The `PromptFile` class processes the prompt file, replacing the defined template strings (`number`, `type_of_media`, etc.) with the user-specified values.
3. **Execution**: The modified prompt is then executed by the Prompt Execution Engine, interacting with the specified AI model to generate the required output.
4. **Output**: The system produces the output based on the substituted template values and presents it to the user.
