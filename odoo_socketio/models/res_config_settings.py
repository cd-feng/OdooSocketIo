# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    socketio_server_host = fields.Char(string="Server Host")
    socketio_server_port = fields.Char(string="Server Port")
    socketio_handshake_path = fields.Char(string="Handshake Path")

    socketio_odoo_connection_type = fields.Selection(string="Odoo Connection Type", selection=[
        ("port", "HostName + Server Port"), ("path", "HostName + Handshake Path")
    ])

    def set_values(self):
        res = super().set_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        config_parameter.set_param("odoo_socketio.socketio_server_host", self.socketio_server_host)
        config_parameter.set_param("odoo_socketio.socketio_server_port", self.socketio_server_port)
        config_parameter.set_param("odoo_socketio.socketio_handshake_path", self.socketio_handshake_path)
        config_parameter.set_param("odoo_socketio.socketio_odoo_connection_type", self.socketio_odoo_connection_type)
        return res

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        socketio_conf = self.get_odoo_socketio_values()
        res.update(socketio_conf)
        return res

    def get_odoo_socketio_values(self):
        """
        Returns SocketIo Setting
        """
        config = self.env['ir.config_parameter'].sudo()
        return {
            'socketio_server_host': config.get_param(key='odoo_socketio.socketio_server_host') or '0.0.0.0',
            'socketio_server_port': config.get_param(key='odoo_socketio.socketio_server_port') or '3000',
            'socketio_handshake_path': config.get_param(key='odoo_socketio.socketio_handshake_path') or '/socket.io',
            'socketio_odoo_connection_type': config.get_param(key='odoo_socketio.socketio_odoo_connection_type') or 'path',
        }

