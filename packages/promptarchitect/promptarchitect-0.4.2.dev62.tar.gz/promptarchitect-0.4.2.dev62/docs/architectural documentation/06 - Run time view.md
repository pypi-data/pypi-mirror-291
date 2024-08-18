## 6. Runtime View

### 6.1 Overview

The runtime view describes the dynamic behavior of the system, focusing on how the system components interact during execution. With the addition of automatic caching and expiration, this section details the flow of control during prompt execution when caching is enabled, including how the system decides whether to use cached results or re-execute prompts.

## 6.2 Key Runtime Scenarios

### 6.2.1 Scenario Template String Substitution in Prompts

1. **Trigger**: A user initiates prompt execution and provides specific values to substitute into the template strings within the prompt file.
2. **Substitution**: The `PromptFile` class processes the prompt file, replacing the defined template strings (`number`, `type_of_media`, etc.) with the user-specified values.
3. **Execution**: The modified prompt is then executed by the Prompt Execution Engine, interacting with the specified AI model to generate the required output.
4. **Output**: The system produces the output based on the substituted template values and presents it to the user.

### 6.2.2 Caching Scenario

This scenario illustrates the process when a prompt is executed using the `EngineeredPrompt` class with caching enabled:

1. **Start Execution**:
   - The system begins by initializing the `EngineeredPrompt` within a Python `with` statement, triggering the setup of the caching context.

2. **Check Cache**:
   - The `CacheManager` component is invoked to check for an existing cache file corresponding to the current prompt. This check includes verifying the cache’s validity and whether it has expired based on the configured expiration time.

3. **Cache Hit**:
   - If a valid, non-expired cache entry is found, the system skips the prompt execution and directly loads the results from the cache.
   - **Outcome**: The results are returned immediately, reducing execution time and avoiding unnecessary API calls.

4. **Cache Miss or Expiration**:
   - If the cache does not exist, is invalid, or has expired, the system proceeds to execute the prompt normally.
   - **Outcome**: The results from this execution will be stored in the cache for future use.

5. **Execution and Storage**:
   - After executing the prompt, the results are automatically stored in the cache by the `CacheManager`, replacing any previous cache entry if it existed.

6. **Return Results**:
   - Finally, the execution results are returned to the calling process, either from cache or from the fresh execution.

#### Sequence Diagram

(Here, you would typically include a sequence diagram that visually represents the interactions described above.)

#### Considerations

- **Performance Impact**: This caching mechanism significantly improves performance by reducing the need to re-execute prompts, especially in scenarios where the same prompts are executed frequently with similar inputs.
- **Cache Expiration**: The expiration time is critical in ensuring that outdated or irrelevant data is not used, balancing between performance and data freshness.
- **Error Handling**: The system ensures that only successful executions are cached, maintaining the integrity and reliability of the cached data.

#### Example

Here is an example of how the runtime behavior changes with caching:

- **Without Caching**: Every time a prompt is executed, the system goes through the full execution process, regardless of whether similar inputs have been processed before.
- **With Caching**: If a prompt has been executed before and is within the cache expiration window, the system loads the results from cache, skipping re-execution and saving resources.

This runtime view highlights how caching is seamlessly integrated into the system’s operation, providing both efficiency and ease of use while ensuring data integrity.
