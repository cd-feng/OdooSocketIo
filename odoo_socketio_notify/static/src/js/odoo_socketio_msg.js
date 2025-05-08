/** @odoo-module **/
import { registry } from "@web/core/registry";

export const odooSocketIoUserMessage = {
    dependencies: ["socketio_service"],

    start(env) {
        const self = this;
        const socketio_service = env.services.socketio_service;
        const notification = env.services.notification;

        function onUserNotifyEvent(data) {
            notification.add(data.message, {
                title: data.title,
                type: data.type || 'info',
                sticky: data.sticky,
            });
        }

        const eventHandlers = {
            "odoo_user_notify_event": onUserNotifyEvent,
        };

        for (const [eventName, handler] of Object.entries(eventHandlers)) {
            socketio_service.on(eventName, handler.bind(self));
        }

        return () => {
            for (const [eventName, handler] of Object.entries(eventHandlers)) {
                socketio_service.off(eventName, handler.bind(self));
            }
        };
    }
};

registry.category("services").add("odoo_socketio_user_notify_msg", odooSocketIoUserMessage);