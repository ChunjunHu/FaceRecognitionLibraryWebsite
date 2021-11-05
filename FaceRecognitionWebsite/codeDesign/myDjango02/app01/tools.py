class PermissionManager(object):
    def login(self,account,password):
        if account=='user' and password=='user':
            return True
        else:
            return False