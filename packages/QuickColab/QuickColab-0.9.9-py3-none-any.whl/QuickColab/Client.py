
import os
from openai import OpenAI
import config
class SetClient:
    def __init__(self):
        self.client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
        self._model = ""
        self.setting = {}
        self._messages = []
        self._sysPrompt = ""
    
    @property
    def model(self):
       return self._model
        
    @model.setter
    def model(self, value: str):
        self._model = value
        
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

