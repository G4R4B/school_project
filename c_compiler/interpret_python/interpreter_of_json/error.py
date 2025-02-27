class CallException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class NotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class InvalidTypeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    
class SyntaxException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class InvalidOperationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidIndexException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)