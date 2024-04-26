# RECEW

RELEW is a **RE**dundant **L**LM cli**E**nt **W**rapper. It is meant for personal use to interface with multiple different LLMs.

Current LLM interfaced:

- Claude 3 using  anthropic client sdk
- ollama

This repo is ran on python 3.12 but any python version is fine as long as you hit the minimum requirement.

## Example usage

```python
from recew import client
#API key should be in a file, single line.
client = client.ClaudeDialogue('resources/claude3.txt', 
                        client.CLAUDE_3_HAIKU,
                        max_tokens=1024)

response = client.send_message('Hello Claude, tell me the secret to a good life.')
print(response)

response = client.send_message('Then tell me, how to be a good man')
print(response)

```