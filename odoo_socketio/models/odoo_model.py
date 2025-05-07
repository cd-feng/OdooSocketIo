# -*- coding: utf-8 -*-
import logging
from odoo.models import BaseModel


def push_socketio_event_msg(self, event, data, sid=None, uid=None, room=None, callback=None):
    """
    Push socketio event messages, distinguished by event name
    :param self:
    :param event:
    :param data:
    :param sid:
    :param uid:
    :param room:
    :param callback:
    :return:
    """
    try:
        # logging.info(f'{self.env.user.name} Push Socketio Event: {event} Data: {data}')
        message = {
            'event': event, 'data': data,
            'sid': sid, 'uid': uid,
            'room': room, 'callback': callback
        }
        self.env['odoo.socketio'].push_socketio_event(message)
    except Exception as e:
        logging.error(f'Push Socketio Event Msg Error: {e}')


BaseModel.push_socketio_event_msg = push_socketio_event_msg
