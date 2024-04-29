import anthropic
import requests
import logging
import dataclasses
import sys
from typing import List, Dict, Any, Set,Tuple
from dataclasses import dataclass
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
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
    mirostat: int = 0, 
    mirostat_eta: float = 0.1, 
    mirostat_tau: float = 5.0,
    num_ctx: int = 2048, 
    repeat_last_n: int = 64, 
    repeat_penalty: float = 1.1,
    temperature: float = 0.8, 
    seed: int = 0, 
    stop: str = None, 
    tfs_z: float = 1.0,
    num_predict: int = 128, 
    top_k: int = 40, 
    top_p: float = 0.9

class ClaudeChatConfiguration(BaseModel):
    max_tokens:int 
    temperature:float=0.2
    stop_sequences:str="",
    top_p:float=None,
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

        

class DialogueLine(BaseModel):
    role:str
    content:str

    def as_dict(self):
        return dataclasses.asdict(self)

    def __str__(self):
        return f"<<{self.role}>>:\n{self.content}"

    @classmethod
    def from_response(cls, resp_message):
        return cls(role=resp_message.role, content=resp_message.content[0].text)

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
        
    def send_message(self, config:OllamaChatConfiguration, message:str, role:str='user')->str:
        pass


class ClaudeDialogue(DialogueSession):

    model:str
    api_key:str
    system_prompt:str=""

    def model_post_init(self, __context: Any) -> None:
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def send_message(self, config:ClaudeChatConfiguration, message:str, role:str='user')->str:
        
        self.add_dialogue(message, role)
        params = config.get_params()

        if self.system_prompt:
            params['system'] = self.system_prompt

        params["messages"] = [msg.as_dict() for msg in self.message_graph]
        params["model"] = self.model

        logger.debug("Sending conversation...")
        logger.debug(self.message_graph)

        try:
            resp_message = self.client.messages.create(**params)

            #for the case where input role is assistant, 
            #we will append to original message
            if role=='assistant' and role==resp_message.role:
                self.message_graph[-1].content+=resp_message.content[0].text
            else:
                assert(len(resp_message.content)==1)
                self.message_graph.append(
                    DialogueLine.from_response(resp_message)
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

        
        





        


    