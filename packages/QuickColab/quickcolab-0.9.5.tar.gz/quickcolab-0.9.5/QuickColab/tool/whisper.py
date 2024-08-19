import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset

class Whisper:
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model_id = "openai/whisper-large-v3"
        self.model: AutoModelForSpeechSeq2Seq
        self.pipeline: pipeline
        self.processor: AutoProcessor
        self._audio_path = ""

    def load_model(self):
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.model_id)
        self.pipeline = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )
        
    @property
    def audio_path(self):
        return self._audio_path
    
    @audio_path.setter
    def audio_path(self, path):
        self._audio_path = path
    
    def transcribe(self):
        if not self._audio_path:
            raise ValueError("Audio path is not set")
        return self.pipeline(self._audio_path)["text"]
    