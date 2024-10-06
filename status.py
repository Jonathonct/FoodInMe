# Simple class to hold whether an action succeeded, or an optional error_msg
# if an action failed.
class Status():
    def __init__(self, success, error_msg=''):
        self.success = success
        self.error_msg = error_msg
        
    def okay(self):
        return self.success
        
    def error(self):
        return self.error_msg