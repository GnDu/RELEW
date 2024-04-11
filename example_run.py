from recew import 

if __name__=="__main__":
    client = ClaudeDialogue('resources/claude3.txt', 
                            CLAUDE_3_HAIKU,
                            max_tokens=1024)

    response = client.send_message('Hello Claude, tell me the secret to a good life.')
    print(response)

    response = client.send_message('Then tell me, how to be a good man')
    print(response)