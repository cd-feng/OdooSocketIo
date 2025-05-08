# -*- coding: utf-8 -*-
{
    'name': "Odoo SocketIo Notify",
    'summary': """ Use socketio communication capabilities to send notification messages to online users """,
    'description': """ """,
    'author': "XueFeng.Su",
    'website': "https://github.com/cd-feng",
    'category': 'Tools/SocketIo',
    'version': '0.1',
    'depends': ['odoo_socketio'],
    "license": "AGPL-3",
    'installable': True,
    'application': False,
    'auto_install': False,
    'data': [
        'views/res_users.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_socketio_notify/static/src/js/odoo_socketio_msg.js',
        ],
    },
}
