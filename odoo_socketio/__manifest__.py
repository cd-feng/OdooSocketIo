# -*- coding: utf-8 -*-
{
    'name': "Odoo SocketIo",
    'summary': """ Applicable to SocketIo communication service in Odoo """,
    'description': """ """,
    'author': "XueFeng.Su",
    'website': "https://github.com/cd-feng",
    'category': 'Tools/SocketIo',
    'version': '18.0.0.1',
    'depends': ['base'],
    "license": "AGPL-3",
    'installable': True,
    'application': False,
    'auto_install': False,
    'external_dependencies': {
        'python': ['python-socketio']
    },
    'data': [
        'security/ir.model.access.csv',
        'views/res_users.xml'
    ],
    'images': [
        'static/description/icon.png',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_socketio/static/libs/socket.io.min.js',
            'odoo_socketio/static/src/js/odoo_socketio.js',
            'odoo_socketio/static/src/js/odoo_socketio_msg.js',
        ],
    },
}
