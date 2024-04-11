# RECEW

RECEW is a **RE**dundant **C**laude 3 cli**E**nt **W**rapper, it uses anthropic client sdk and wrap additional classes around it for personal use.

The main ClaudeClient retains the conversation within it, thus you will just need to send the message over.

## Example usage

```python
import client
#API key should be in a file, single line.
client = client.ClaudeClient('resources/claude3.txt', 
                        client.CLAUDE_3_HAIKU,
                        max_tokens=1024)

response = client.send_message('Hello Claude, tell me the secret to a good life.')
print(response)

response = client.send_message('Then tell me, how to be a good man')
print(response)

```