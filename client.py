import anthropic
import logging
from typing import List, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# can ignore for now if I need
# @dataclass
# class DialogueGraph:
#     root:Dict[str, Any]
#     next_turns:List[Dict[str, Any]]


CLAUDE_3_OPUS = 'claude-3-opus-20240229'
CLAUDE_3_SONNET = 'claude-3-sonnet-20240229'
CLAUDE_3_HAIKU = 'claude-3-haiku-20240307'

class ClaudeClient:

    def __init__(self, api_file:str, model:str, 
                        max_tokens:int, 
                        temperature:float=0.2, 
                        system_prompt:str="",
                        stop_sequences:str="",
                        top_p:float=None,
                        top_k:int=None):
        with open(api_file) as f:
            api_key = f.read().strip()
        self.client = anthropic.Anthropic(api_key=api_key)

        #needed
        self.model = model
        self.max_tokens = max_tokens
        self.message_graph = []
        
        #we override temperature if top_p is defined
        if top_p is not None and temperature is not None:
            print("Can't define top_p and temperature at the same time, top_p will override temperature")
        self.top_p = top_p
        self.temperature = temperature

        #optional params
        self.system_prompt = system_prompt
        self.stop_sequences = stop_sequences
        self.top_k = top_k

    def send_message(self, message, role:str='user'):
        
        if role not in ['user', 'assistant']:
            raise AssertionError(f'Role is either user or assistant but not {role}')

        self.message_graph.append({
            'role': role,
            'content': message
        })

        params = {
            "max_tokens": self.max_tokens,
            "messages": self.message_graph,
            "model":self.model
        }

        if self.top_p is not None:
            params['top_p'] = self.top_p
        elif self.temperature is not None:
            params['temperature'] = self.temperature
        else:
            raise AssertionError("Must specify either temperature or top_p.")

        if self.system_prompt:
            params['system'] = self.system_prompt

        if self.stop_sequences:
            params['stop_sequences'] = self.system_prompt

        if self.top_k:
            params['top_k'] = self.top_k

        logger.info("Sending conversation...")
        message = self.client.messages.create(**params)
        
        print(type(message), message)

if __name__=="__main__":
    client = ClaudeClient('resources/claude3.txt', 
                            CLAUDE_3_HAIKU,
                            max_tokens=1024)

    client.send_message('Hello Claude, tell me the secret to a good life.')

        
        





        


    