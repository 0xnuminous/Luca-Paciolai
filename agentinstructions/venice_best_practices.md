# Venice API Best Practices

This document summarizes recommendations for integrating with the Venice API using its OpenAI-compatible interface.

## Base Configuration
- Use the base URL `https://api.venice.ai/api/v1` for all API calls.
- Configure your OpenAI client with this `base_url`.

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY", base_url="https://api.venice.ai/api/v1")
```

## Available Endpoints
- `/api/v1/models` – list available models and their capabilities.
- `/api/v1/chat/completions` – generate text responses.
- `/api/v1/image/generations` – generate images from prompts.

## System Prompts
Venice automatically appends a default system prompt to your messages. To disable this behaviour pass `venice_parameters={"include_venice_system_prompt": False}` when creating a completion.

```python
client.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    venice_parameters={"include_venice_system_prompt": False},
)
```

## Best Practices
- Implement robust error handling for API responses.
- Be mindful of rate limits during the beta period.
- Test both with and without the Venice system prompt enabled.
- Keep your API keys secure and rotate them regularly.

## Differences from OpenAI
- Additional `venice_parameters` provide features not present in the OpenAI API.
- Default system prompt handling differs.
- Some model names may differ from those on OpenAI. Consult the Venice API docs for supported models.
