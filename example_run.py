from src.client import ClaudeDialogue,ClaudeChatConfiguration, CLAUDE_3_HAIKU

LLM_MODEL = "ollama"

if __name__=="__main__":

    if LLM_MODEL=='claude':
        with open("resources/api_key", 'r') as f:
            api_key = f.read()

        client = ClaudeDialogue(model=CLAUDE_3_HAIKU, api_key=api_key)
        message_config = ClaudeChatConfiguration(max_tokens=1024, temperature=0.9)
        response = client.send_message(message_config, 'Hello Claude, tell me the secret to a good life.')
        print(response)

        response = client.send_message(message_config, 'Then tell me, how to be a good man')
        print(response)
    elif LLM_MODEL=='ollama':
        pass
    else:
        raise NotImplementedError(f"{LLM_MODEL} not implemented?")