from dataclasses import dataclass
from typing import Optional
    
@dataclass
class LLMResponse:
    request_id: str
    output_text: Optional[str] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    
    @property
    def latency(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time 
        return None