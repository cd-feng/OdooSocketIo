# -*- coding: utf-8 -*-
import logging
import threading
import asyncio
import socketio
import queue
import multiprocessing
from urllib.parse import parse_qs
from aiohttp import web
from odoo import models, api, tools
from odoo.service.server import server, ThreadedServer

SOCKETIO_CLIENT_EVENT_MESSAGE_QUEUE = queue.Queue()


class SocketIoServer(threading.Thread):

    def __init__(self, conf):
        super().__init__(daemon=True)
        self.event_loop = None
        self.host = conf['socketio_server_host']
        self.port = int(conf['socketio_server_port'])
        self.send_queue = None
        self.user_sids = dict()
        self.sio = socketio.AsyncServer(
            async_mode='aiohttp', cors_allowed_origins=[],
            allow_upgrades=True, transports=['websocket'],
            ping_interval=20, ping_timeout=60
        )
        self.app = web.Application()
        self.sio.attach(self.app, socketio_path=conf['socketio_handshake_path'])
        self._register_events()

    def run(self):
        """
        Run SocketIo Server
        """
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        self.send_queue = asyncio.Queue()
        self.event_loop.create_task(self._send_client_message_task())
        web.run_app(self.app, host=self.host, port=self.port, handle_signals=False, loop=self.event_loop)

    def _register_events(self):
        """
        Register server event messages
        """

        def remove_user_sid(sid):
            """delete sid to user_sids"""
            for key in self.user_sids:
                if sid in self.user_sids[key]:
                    self.user_sids[key].remove(sid)

        @self.sio.event
        async def connect(sid, environ):
            query_string = environ.get('QUERY_STRING', '')
            if query_string:
                params = parse_qs(query_string)
                try:
                    uid = int(params.get('uid', [None])[0])
                    user_sids = self.user_sids.get(uid, [])
                    if user_sids:
                        user_sids.append(sid)
                    else:
                        self.user_sids[uid] = [sid]
                except Exception:
                    pass
                try:
                    room = params.get('room', [None])[0]
                    if room:
                        await self.sio.enter_room(sid, room)
                except Exception:
                    pass
            logging.info(f'New SocketIo Client Connection. SID: {sid}')

        @self.sio.event
        async def disconnect(sid):
            try:
                remove_user_sid(sid)
            except Exception:
                pass
            logging.info('SocketIo Client Disconnect: {sid}'.format(sid=sid))

        @self.sio.on("*")
        async def handle_catch_all_event(event, sid, data):
            SOCKETIO_CLIENT_EVENT_MESSAGE_QUEUE.put_nowait((event, sid, data))

    async def _send_client_message_task(self):
        """
        Send Message To Client Task
        """
        while True:
            message = await self.send_queue.get()
            event, data, sid = message.get('event', None), message.get('data', {}), message.get('sid', None)
            if not event:
                continue
            callback, room = message.get('callback', None), message.get('room', None)
            await self.sio.emit(event, data=data, to=sid, room=room)
            await asyncio.sleep(0.001)

    async def _add_event_message(self, data):
        """
        Add a message to the send queue
        """
        await self.send_queue.put(data)

    def add_send_event_msg(self, msg):
        """
        Add a message to the queue of messages to be sent.
        This function is a synchronous function and is used to call an external synchronization environment.
        """
        uid, sid = msg.get('uid', None), msg.get('sid', None)
        if not sid and uid:
            msg['sid'] = self.user_sids.get(uid, None)
        del msg['uid']
        asyncio.run_coroutine_threadsafe(self._add_event_message(msg), self.event_loop)


class OdooSocketIo(models.Model):
    _name = 'odoo.socketio'
    _description = "Odoo SocketIo"

    socketio_server = None

    @api.model
    def get_socketio_conf(self):
        """
        Get the configured socketio running config from 'res.config.settings'
        """
        return self.env['res.config.settings'].get_odoo_socketio_values()

    def _register_hook(self):
        super()._register_hook()
        if isinstance(server, ThreadedServer) and getattr(server, 'main_thread_id') != threading.current_thread().ident:
            return
        if multiprocessing.current_process().name == 'MainProcess':
            OdooSocketIo.socketio_server = SocketIoServer(self.get_socketio_conf())
            OdooSocketIo.socketio_server.start()
            threading.Thread(target=self.handle_client_socketio_event_thread, daemon=True).start()

    @api.model
    def push_socketio_event(self, messages):
        """
        Push socketio event messages
        """
        try:
            OdooSocketIo.socketio_server.add_send_event_msg(messages)
        except Exception as e:
            logging.error(f"Push SocketIo Event Error: {e}")

    @api.model
    def handle_client_socketio_event_thread(self):
        """
        Process event messages sent by clients
        """
        # registry = odoo.modules.registry.Registry(odoo.tools.config['db_name'])
        # with registry.cursor() as new_cr:
        while True:
            event, sid, data = SOCKETIO_CLIENT_EVENT_MESSAGE_QUEUE.get()
            with self.pool.cursor() as new_cr:
                self = self.with_env(self.env(cr=new_cr))
                # Here you can add the logic code for handling default events
                if not event or not data:
                    continue
                # Call other custom event methods
                else:
                    self.deal_custom_event(event, sid, data)
            SOCKETIO_CLIENT_EVENT_MESSAGE_QUEUE.task_done()

    @api.model
    def deal_custom_event(self, event, sid, data):
        """
        Handle custom events, other modules call this function for extension
        When calling a subclass, be sure to call the parent class message processing function
        """
        logging.debug(f"deal custom msg {event} {sid} {data}")