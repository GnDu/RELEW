import anthropic
import requests
import logging
import dataclasses
import sys
from typing import List, Dict, Any, Set,Tuple
from dataclasses import dataclass
from pydantic import BaseModel, Field, ConfigDict
from anthropic import Anthropic

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)
# can ignore for now if I need
# @dataclass
# class DialogueGraph:
#     root:Dict[str, Any]
#     next_turns:List[Dict[str, Any]]


CLAUDE_3_OPUS = 'claude-3-opus-20240229'
CLAUDE_3_SONNET = 'claude-3-sonnet-20240229'
CLAUDE_3_HAIKU = 'claude-3-haiku-20240307'

class OllamaChatConfiguration(BaseModel):
    mirostat: int = None
    mirostat_eta: float = None
    mirostat_tau: float = None
    num_ctx: int = None
    repeat_last_n: int = None
    repeat_penalty: float = None
    temperature: float = None
    seed: int = None
    stop: str = None
    tfs_z: float = None
    num_predict: int = None
    top_k: int = None
    top_p: float = None

class ClaudeChatConfiguration(BaseModel):
    max_tokens:int 
    temperature:float=0.2
    stop_sequences:str=None
    top_p:float=None
    top_k:int=None

    def model_post_init(self, __context: Any) -> None:
        #we override temperature if top_p is defined
        if self.top_p is not None and self.temperature is not None:
            print("Can't define top_p and temperature at the same time, top_p will override temperature")

        if self.top_p is None and self.temperature is None:
            raise AssertionError("Must specify either temperature or top_p.")
    
    def get_params(self):
        params = {
            "max_tokens": self.max_tokens,
        }
        if self.top_p is not None:
            params['top_p'] = self.top_p
        elif self.temperature is not None:
            params['temperature'] = self.temperature
        else:
            raise AssertionError("Must specify either temperature or top_p.")
        
        if self.stop_sequences:
            params['stop_sequences'] = self.stop_sequences

        if self.top_k:
            params['top_k'] = self.top_k

        return params


class DialogueLine(BaseModel):
    role:str
    content:str

    def __str__(self):
        return f"<<{self.role}>>:\n{self.content}"

class DialogueSession(BaseModel):
    message_graph:List[DialogueLine]=Field(default_factory=list)

    def add_dialogue(self, message:str, role:str='user'):
        if role not in ['user', 'assistant']:
            raise AssertionError(f'Role is either user or assistant but not {role}')
        input_message = DialogueLine(role=role, content=message)
        self.message_graph.append(input_message)

class OllamaDialogue(DialogueSession):

    ollama_url:str
    modelfile:str
    
    def model_post_init(self, __context: Any) -> None:
        if self.ollama_url.endswith('/'):
            self.ollama_url = self.ollama_url[:-1]
        
        #get params from model file
        model_file_api_call = f"{self.ollama_url}/api/show"
        r = requests.post(model_file_api_call,
                      json={
                          'name': self.modelfile
                      })

        r.raise_for_status()
        json_file = r.json()
        raw_parameters = json_file['parameters'].split('\n')
        self.params:dict = {}
        for raw_params in raw_parameters:
            tokens = raw_params.strip().split(2)
            key = tokens[0]
            values = tokens[1]
            self.params[key] = values
            logger.debug(f"{key}: {values}")

    def send_message(self, config:OllamaChatConfiguration, message:str, role:str='user')->str:
        
        generate_api_call = f"{self.ollama_url}/api/chat"

        #to override any model parameters
        options = config.dict(exclude_defaults=True)
        self.add_dialogue(message, role)

        payload = {"model": self.modelfile, 
                    "messages": [msg.model_dump() for msg in self.message_graph], 
                    "stream": False}
        if options:
            payload['options'] = options

        r = requests.post(generate_api_call, json=payload)
        r.raise_for_status()

        response = r.json()
        message = response['message']
        logger.debug(message)


class ClaudeDialogue(DialogueSession):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    model:str
    api_key:str
    system_prompt:str=""
    client:Anthropic=None

    def model_post_init(self, __context: Any) -> None:
        self.client = Anthropic(api_key=self.api_key)

    def convert_resp_to_dialogue_line(self, resp_message):
        return DialogueLine(role=resp_message.role, content=resp_message.content[0].text)

    def send_message(self, config:ClaudeChatConfiguration, message:str, role:str='user')->str:
        
        self.add_dialogue(message, role)
        params = config.get_params()

        if self.system_prompt:
            params['system'] = self.system_prompt

        params["messages"] = [msg.model_dump() for msg in self.message_graph]
        params["model"] = self.model

        logger.debug("Sending conversation...")
        logger.debug(self.message_graph)
        logger.debug(params)

        try:
            resp_message = self.client.messages.create(**params)

            #for the case where input role is assistant, 
            #we will append to original message
            if role=='assistant' and role==resp_message.role:
                self.message_graph[-1].content+=resp_message.content[0].text
            else:
                assert(len(resp_message.content)==1)
                self.message_graph.append(
                    self.convert_resp_to_dialogue_line(resp_message)
                )
            logger.debug(f'Got reply: {self.message_graph[-1]}')
            last_reply = self.message_graph[-1]
            return last_reply
        #exceptions below copy from the git repo
        except anthropic.APIConnectionError as e:
            logger.error("The server could not be reached")
            logger.error(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except anthropic.RateLimitError as e:
            logger.error("A 429 status code was received; we should back off a bit.")
        except anthropic.APIStatusError as e:
            logger.error("Another non-200-range status code was received")
            logger.error(e.status_code)
            logger.error(e.response)
        
        return None

        
        





        


    