from pydantic import BaseModel


class Audio(BaseModel):
    '''
    @description: 音频文件类
    ''' 
    path: str