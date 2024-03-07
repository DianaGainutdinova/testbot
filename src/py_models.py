from typing import List, Optional
from pydantic import BaseModel


class ResponseInfo(BaseModel):
    # pydantic модель для хранения всех сообщений от df и кнопок
    messages: Optional[List[str]]
    buttons: Optional[List[str]]
    # events: Optional[str]

    class Config:
        arbitrary_types_allowed = True
