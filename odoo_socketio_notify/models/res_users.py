# -*- coding: utf-8 -*-
from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def notification_message(self, message, title=None, type_message=None, sticky=False):
        """
        Send a notification message to the user. Note: This message is real-time and based on socketio.
        If the user is not online, he will not receive the message.
        :param message: message
        :param title: title
        :param type_message: ["warning", "danger", "success", "info"]
        :param sticky:
        """
        data = {
            'message': message,
            'title': title,
            'type': type_message,
            'sticky': sticky,
        }
        for user in self:
            self.push_socketio_event_msg(
                event="odoo_user_notify_event", data=data,
                uid=user.id, room="odoo_browser_room"
            )

    def send_warning_socketio_message(self):
        self.notification_message("This is warning socketio message！", type_message="warning")

    def send_danger_socketio_message(self):
        self.notification_message("This is danger socketio message！", type_message="danger")

    def send_success_socketio_message(self):
        self.notification_message("This is success socketio message！", type_message="success")

    def send_info_socketio_message(self):
        self.notification_message("This is info socketio message！", type_message="info")
