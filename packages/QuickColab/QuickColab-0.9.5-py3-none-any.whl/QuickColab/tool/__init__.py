
import os
from openai import OpenAI
from .QuickDataset import Jsonl
from .SetTool import ToolCreate
from .whisper import Whisper
KEY = ""
URL = ""
class SetClient:
    client = OpenAI(api_key=KEY, base_url=URL)
    otherkey = ""
    otherbase = ""
    otherclient: OpenAI|None
    @staticmethod
    def set_other_client(key: str, base: str):
        SetClient.otherkey = key
        SetClient.otherbase = base
        SetClient.otherclient =OpenAI(api_key=key, base_url=base)
    def __init__(self):
        self.client = SetClient.client
        self._model = ""
        self.setting = {}
        self._messages = []
        self._sysPrompt = ""
    
    @property
    def set_model(self, model: str):
        self._model = model
        
    @set_model.setter
    def set_model(self, model: str):
        self._model = model
        
    def set_setting(self, **setting):
        self.setting.update(setting)
    
    @property
    def messages(self):
        return self._messages
    
    @messages.setter
    def messages(self, value):
        self._messages = value

    @property
    def append_message(self, message: str):
        self._messages.append({"role": "user", "content": message})
    @append_message.setter
    def append_message(self, message: str):
        self._messages.append({"role": "user", "content": message})
        
    @property
    def sysPrompt(self):
        return self._sysPrompt
    
    @sysPrompt.setter
    def sysPrompt(self, value: str):
        self._sysPrompt = value
    
    @property
    def completions(self):
        if not self._model:
            raise ValueError("Model is not set. Use set_model() to set a model.")
        
        new_messages = [{"role": "system", "content": self._sysPrompt}]
        new_messages.extend(self._messages)
        
        try:
            response = self.client.chat.completions.create(
                model=self._model,
                messages=new_messages,
                **self.setting
            )
            
            text = response.choices[0].message.content
            self._messages.append({"role": "assistant", "content": text})
            return text
        except Exception as e:
            print(f"Error occurred during API call: {e}")
            return None

__all__ = ["SetClient","Jsonl","ToolCreate","Whisper","KEY","URL"]
