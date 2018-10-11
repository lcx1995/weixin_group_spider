class RefreshPageException(Exception):
    '''
    重新刷新页面
    '''
    def __init__(self,*args):
        self.args = args