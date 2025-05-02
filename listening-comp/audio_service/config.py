from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioConfig:
    engine: str = 'neural'
    language_code: str = 'ro-RO'
    voice_id: str = 'Carmen'  # Romanian voice
    output_format: str = 'mp3'
    sample_rate: int = 24000
    text_type: str = 'text'
    
    def to_dict(self):
        return {
            'Engine': self.engine,
            'LanguageCode': self.language_code,
            'VoiceId': self.voice_id,
            'OutputFormat': self.output_format,
            'SampleRate': self.sample_rate,
            'TextType': self.text_type
        } 