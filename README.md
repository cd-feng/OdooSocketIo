# Odoo SocketIo Module

[中文版本](README.zh-CN.md)

## Overview
This module provides real-time communication capabilities for Odoo using Socket.IO. It enables bidirectional event-based communication between Odoo server and web clients.

## Features
- Real-time event-based communication
- Support for WebSocket transport
- User-based connection management
- Room-based messaging
- Built-in reconnection handling
- Integration with Odoo's notification system
- Admin test interface for debugging

## Installation
1. Install the module as usual in Odoo
2. Ensure the following dependencies are installed:
   ```bash
   pip install python-socketio==5.13.0
   ```
3. Configure the Socket.IO port in Odoo config file:
   ```ini
   [options]
   socketio_port = 3000
   ```

## Server Configuration
The module automatically starts a Socket.IO server when Odoo starts. Key server features:

- Runs on port specified in config (default: 3000)
- Supports WebSocket transport
- Maintains user connection mapping
- Processes incoming client events

### Server API
```python
# Push message to client
self.env['odoo.socketio'].push_socketio_event({
    'event': 'your_event_name',
    'data': {'key': 'value'},
    'uid': user_id,  # Target user ID
    # Optional: 'room': 'room_name'
})

# Get configured port
port = self.env['odoo.socketio'].get_socketio_port()
```

## Client Usage
The module provides a JavaScript service for easy client-side integration:

```javascript
// Get the socketio service
const socketioService = await this.env.services.socketio_service;

// Subscribe to events
socketioService.on('event_name', (data) => {
    console.log('Received:', data);
});

// Send events
socketioService.emit('event_name', {key: 'value'});

// Monitor connection status
socketioService.onServiceEvent('odoo_socketio_connect', () => {
    console.log('Connected to Socket.IO');
});
```

## Example
### Server-side (Python)
```python
# Send notification to user
self.env['odoo.socketio'].push_socketio_event({
    'event': 'user_notification',
    'data': {'message': 'Hello from server!'},
    'uid': user.id
})
```

### Client-side (JavaScript)
```javascript
// In your Odoo component
setup() {
    this.socketioService = useService('socketio_service');
    this.socketioService.on('user_notification', (data) => {
        this.env.services.notification.add(data.message);
    });
}
```

## Testing
Administrators can test the functionality from:
`Settings → Users → Select User → Test Socketio Notify tab`

## Notes
- Requires Odoo 18.0 or later
- WebSocket support depends on browser compatibility
- For production use, consider adding authentication middleware
- The module runs in the main Odoo process - for heavy loads, consider a separate process

## License
AGPL-3
