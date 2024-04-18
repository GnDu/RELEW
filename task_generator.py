from recew.client import ClaudeClient, CLAUDE_3_OPUS

if __name__=="__main__":
    with open('resources/system_prompt') as f:
        system_prompt = f.read()

    client = ClaudeClient('resources/claude3.txt', 
                            CLAUDE_3_OPUS,
                            max_tokens=4096,
                            system_prompt=system_prompt)

    with open('graph.py') as f:
        tool_str = f.read()

    with open('resources/prompt') as f:
        prompt_template = f.read()

    problem = "Write a program that generates a acyclic graph of 5 nodes. Label each relation based on the level of depth. The depth of the graph should be 10."
    input = "No input"

    prompt = prompt_template.format(tool_str=tool_str, problem=problem, input=input)

    response = client.send_message(prompt)
    print(response)
    