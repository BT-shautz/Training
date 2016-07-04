{

    'name': "Open Academy",
    'description': "Module for managing courses",
    'author' : "brain-tec AG",
    'category': "Education",
    'version': "1.0",
    'depends': ['base'],
    'data': ['views/openacademy.xml',
             'workflows/session_workflow.xml',
             'reports/openacademy_session_report.xml',
             'security/openacademy_security.xml',
             'security/ir.model.access.csv',]

}
