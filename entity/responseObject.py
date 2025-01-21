from utils.constants import SUCCESS_CODE, SUCCESS_MSG, SUCCESS_DATA
class response:  
    '''
    @description: 为标准化输出对象编写的类
    '''  
    code: str
    msg: str
    data: None
    
    @staticmethod
    def success(data = SUCCESS_DATA):
        '''
        @description: 标准化输出成功对象
        @return {response} 输出对象
        '''        
        obj = response()
        obj.code = SUCCESS_CODE
        obj.msg = SUCCESS_MSG
        obj.data = data
        return obj
    
    
    @staticmethod
    def failure(code, msg):
        '''
        @description: 标准化输出失败对象（data为空）
        @return {response} 输出对象
        '''    
        obj = response()
        obj.code = code
        obj.msg = msg
        obj.data = None
        return obj