# -*- coding: utf-8 -*-
from odoo import models, api


class ResUsers(models.Model):
    _inherit = "res.users"

    def send_test_socketio_message(self):
        """
        send user test socketio message
        """
        self.ensure_one()
        data = {'text': "This Is A Test Message"}
        self.push_user_socketio_msg("odoo_user_test_event", data, self.env.user.id)

    @api.model
    def push_user_socketio_msg(self, event, data, uid):
        """
        Push room `odoo_browser_room` user message
        """
        self.push_socketio_event_msg(event, data=data, uid=uid, room="odoo_browser_room")
