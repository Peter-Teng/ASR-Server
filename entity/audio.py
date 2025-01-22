from typing import Optional
from pydantic import BaseModel


class Audio(BaseModel):
    '''
    @description: 音频文件类
    ''' 
    path: Optional[str] = None
    speaker_num: Optional[int] = None
    base64Str: Optional[str] = None