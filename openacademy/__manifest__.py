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
                'demo/sessions.xml',
                'views/childrenpartnerviews.xml',
                'demo/category.xml',
                'wizards/wizard_view.xml',
                'data/session_end_crn.xml',
                'security/security.xml',
                'security/ir.model.access.csv',
                'reports/report.xml'

   ],
   # data files containing optionally loaded demonstration data
   'demo': [
   ],
   'auto_install': False
}