import json
from src.client import ClaudeDialogue,ClaudeChatConfiguration, OllamaDialogue, OllamaChatConfiguration, CLAUDE_3_HAIKU

MODE='OLLAMA'

LLM_MODEL = "ollama"

if __name__=="__main__":

<<<<<<< HEAD
    if LLM_MODEL=='claude':
=======
    if MODE=='CLAUDE':
        print('=== CLAUDE3 ===')
>>>>>>> 0664b534ec9c9d6f61ce6e845db94eacbe3a155a
        with open("resources/api_key", 'r') as f:
            api_key = f.read()

        client = ClaudeDialogue(model=CLAUDE_3_HAIKU, api_key=api_key)
        message_config = ClaudeChatConfiguration(max_tokens=1024, temperature=0.9)
        response = client.send_message(message_config, 'Hello Claude, tell me the secret to a good life.')
        print(response)

        response = client.send_message(message_config, 'Then tell me, how to be a good man')
        print(response)
<<<<<<< HEAD
    elif LLM_MODEL=='ollama':
        pass
    else:
        raise NotImplementedError(f"{LLM_MODEL} not implemented?")
=======
    elif MODE=='OLLAMA':
        print('=== OLLAMA ===')
        with open("resources/ollama_config.json", 'r') as f:
            ollama_config = json.load(f)
        client = OllamaDialogue(ollama_url=ollama_config['url'], modelfile=ollama_config['modelfile'])
        message_config = OllamaChatConfiguration(temperature=0.9, num_ctx=1024)
        response = client.send_message(message_config, 'Hello Phi, tell me the secret to a good life.')
        print(response)

        response = client.send_message(message_config, 'Then tell me, how to be a good man')
        print(response)
    else:
        raise NotImplementedError(f'{MODE} is not implemented')
>>>>>>> 0664b534ec9c9d6f61ce6e845db94eacbe3a155a
