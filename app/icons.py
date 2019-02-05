from flask import current_app

icons={
  'show': 'glyphicon glyphicon-chevron-right',
  'add': 'glyphicon glyphicon-plus',
  'UNKNOWN': 'glyphicon glyphicon-question-sign'
  }
  
def icon_html(name):
    cls=icons.get(name.lower(), icons.get('UNKNOWN'))
    return '<span aria-hidden="true" class="{cls}"></span>'.format(cls=cls)

def register(app):
    app.jinja_env.globals.update(icon_html=icon_html)

