from pydantic import BaseModel


class Speaker(BaseModel):
    '''
    @description: 讲话人文件类
    ''' 
    audioPath: str
    name: str