from flask import Response

class Directory(object):
    def __init__(self):
        self.contents = {}
    
    def set(self, alias, url):
        self.contents[alias] = url
        return self
    
    def response(self):
        response = Response()
        response.status_code = 200
        response.content_type = 'application/k2-directory'
        
        data = ''
        for alias, url in self.contents.items():
            data = data +'{alias}={url}\n'.format(alias=alias, url=url)
        
        response.set_data(data)
        return response

 