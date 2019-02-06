from flask import Response

class Directory(object):
    def __init__(self, name=None):
        self.name = name
        self.contents = {}
    
    def set(self, alias, url):
        self.contents['alias-'+alias] = url
        return self
    
    def response(self):
        response = Response()
        response.status_code = 200
        response.headers = {'content-type': 'application/k2-directory'}
        if self.name:
            response.headers.update({'__name__': self.name})
        response.headers.update(self.contents)
        
        return response

 