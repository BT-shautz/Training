{
   'name': "OpenAcademy",
   'version': '1.0',
   'depends': ['base'],
   'author': "Stefan Hautz",
   'category': '',
   'description': """
                   Description text
                  """,
   # data files always loaded at installation
   'data': [
                'views/courseviews.xml',
                'views/sessionviews.xml',
                'views/menu.xml',
                'demo/courses.xml',
                'demo/sessions.xml'

   ],
   # data files containing optionally loaded demonstration data
   'demo': [
   ],
   'auto_install': False
}