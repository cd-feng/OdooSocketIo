/** @odoo-module **/
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { EventBus } from "@odoo/owl";
import { user } from "@web/core/user";


class SocketIoClient {
    constructor(env) {
        this.env = env;
        this.socketio = null;
        this.hostUrl = null;
        this.uid = null;
        this.bus = new EventBus();
        this.isConnected = false;
        this.wait_ons = [];
        this.room = "odoo_browser_room";
    }

    async _start() {
        try {
            const port = await rpc("/web/dataset/call_kw", {
                model: "odoo.socketio", method: "get_socketio_port",
                args: [], kwargs: {}
            });
            if (!port || typeof io === 'undefined') return;
            this.hostUrl = window.location.hostname + ':' + port;
            this.uid = user.userId;
            this.socketio = io(this.hostUrl, {
                rememberUpgrade: true,
                transports: ['websocket', 'long-polling'],
                upgrade: true,
                query: { uid: this.uid, room: this.room }
            });
            this._registerSocketIOEvents();
            this._processWaitOns();
        } catch (error) {
            console.error("Failed to initialize Socket.IO service:", error);
        }
    }

    _registerSocketIOEvents() {
        if (!this.socketio) return;

        this.socketio.on('connect', () => {
            this.isConnected = true;
            console.log(`Successfully Connected To The SocketIo Service：${this.hostUrl}`);
            this.bus.trigger('odoo_socketio_connect');
            this._processWaitOns();
        });

        this.socketio.on('disconnect', () => {
            this.isConnected = false;
            console.log(`Communication With SocketIo Has Been Disconnect: ${this.hostUrl}`);
            this.bus.trigger('odoo_socketio_disconnect');
        });

        this.socketio.on('connect_error', (error) => {
            this.bus.trigger('odoo_socketio_connect_error', error);
        });

        this.socketio.on('odoo_server_event', (msg) => {
            this.bus.trigger('odoo_server_event', msg);
        });
    }

    /**
     * Handle events registered before the connection is established
     */
    _processWaitOns() {
        if (this.socketio && this.isConnected) {
            while (this.wait_ons.length > 0) {
                const [eventName, callback, once] = this.wait_ons.shift();
                if (once) {
                    this.socketio.once(eventName, callback);
                } else {
                    this.socketio.on(eventName, callback);
                }
            }
        }
    }

    /**
     * Method for components to call: subscribe to Socket.IO events (corresponding to the old on_bus)
     * If Socket.IO is not connected, it will be queued and registered after waiting for connection
     * @param {string} eventName
     * @param {function} callback
     * @param {boolean} [once=false]
     */
    on(eventName, callback, once = false) {
        if (this.socketio && this.isConnected) {
            if (once) {
                this.socketio.once(eventName, callback);
            } else {
                this.socketio.on(eventName, callback);
            }
        } else {
            this.wait_ons.push([eventName, callback, once]);
        }
    }

    /**
     * Method for component to call: unsubscribe Socket.IO event (corresponding to the old remove_on_bus)
     * @param {string} eventName event name
     * @param {function} callback callback function (must be the same function instance used when subscribing)
     */
    off(eventName, callback) {
        if (this.socketio) {
            this.socketio.off(eventName, callback);
        } else {
            this.wait_ons = this.wait_ons.filter(([name, cb, once]) => !(name === eventName && cb === callback));
        }
    }

    /**
     * Method for component to call: send message to Socket.IO server
     * @param {string} eventName event name
     * @param {*} data data to be sent
     */
    emit(eventName, data) {
        if (this.socketio && this.isConnected) {
            this.socketio.emit(eventName, data);
        } else {
            console.warn("Socket.IO is not connected. Cannot emit event:", eventName);
        }
    }

    _stop() {
        if (this.socketio) {
            this.socketio.disconnect();
            this.socketio = null;
        }
        this.wait_ons = [];
        this.bus.destroy();
    }

    // Subscribe and unsubscribe methods of the Service internal event bus for components to monitor service status or general messages
    onServiceEvent(eventName, callback) {
        this.bus.on(eventName, this, callback);
    }

    offServiceEvent(eventName, callback) {
        this.bus.off(eventName, this, callback);
    }
}


export const socketIOService = {

    start(env) {
        const socketioClient = new SocketIoClient(env);
        socketioClient._start().then();

        return {
            on: socketioClient.on.bind(socketioClient),
            off: socketioClient.off.bind(socketioClient),
            emit: socketioClient.emit.bind(socketioClient),
            // Expose the subscription method of the service's internal event bus to monitor service status or general messages
            onServiceEvent: socketioClient.onServiceEvent.bind(socketioClient),
            offServiceEvent: socketioClient.offServiceEvent.bind(socketioClient),
            getIsConnected: () => socketioClient.isConnected,
        };
    },

    stop(env, dependencies, socketioClient) {
        if (socketioClient && socketioClient._stop) {
            socketioClient._stop();
        }
    }

};


registry.category("services").add("socketio_service", socketIOService);
