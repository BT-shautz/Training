# -*- coding: utf-8 -*-
{
    'name': "Open Academy",
    'summary': "Module for managing courses.",
    'description': """ longer description """,
    'author': "brain-tec AG",
    'category': "Education",
    'version': "1.0",
    'depends': ['base','board'],
    'demo': ['demo/demo.xml'],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'wizard/wizard_view.xml',
             'views/course_view.xml',
             'views/session_view.xml',
             'views/res_partner_view_ext.xml',
             'views/menus.xml',
             'views/session_board.xml',
             'reports/openacademy_reports.xml',
    ]
}
