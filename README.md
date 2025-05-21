# Odoo SocketIo Module

[简体中文](README.zh-CN.md)

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
- Custom event handling support
- Thread-safe message processing

## Installation
1. Install the module as usual in Odoo
2. Ensure the following dependencies are installed:
   ```bash
   pip install python-socketio==5.13.0 aiohttp
   ```
3. After installing the module, set the operating parameters under "Settings", "SocketIo", and restart Odoo

## Server Configuration
The module automatically starts a Socket.IO server when Odoo starts. Key server features:

- Runs on specified host:port (default: 0.0.0.0:3000)
- Supports WebSocket transport
- Maintains user connection mapping
- Processes incoming client events
- Thread-safe message queue processing

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
port = self.env['odoo.socketio'].get_socketio_conf().get('socketio_server_port')

# Handle custom events (override in your models)
def deal_custom_event(self, event, sid, data):
    # Your custom event handling logic
    super().deal_custom_event(event, sid, data)
```

## Client Usage
Include socket.io.min.js in your assets and use standard Socket.IO client API:

```javascript
// Connect to server
const socket = io('http://localhost:3000', {
    path: '/socket.io',
    query: {
        uid: user_id,  // Current user ID
        room: 'room_name'  // Optional room name
    }
});

// Subscribe to events
socket.on('event_name', (data) => {
    console.log('Received:', data);
});

// Send events
socket.emit('event_name', {key: 'value'});

// Connection status
socket.on('connect', () => {
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

# Handle custom event
def deal_custom_event(self, event, sid, data):
    if event == 'custom_action':
        # Process custom action
        self.do_something(data)
    super().deal_custom_event(event, sid, data)
```

### Client-side (JavaScript)
```javascript
// In your Odoo component
const socket = io('http://localhost:3000', {
    path: '/socket.io',
    query: {uid: current_user_id}
});

socket.on('user_notification', (data) => {
    this.env.services.notification.add(data.message);
});

socket.emit('custom_action', {action: 'refresh'});
```

## Testing
Administrators can test the functionality from:
`Settings → Users → Select User → Test Socketio Notify tab`

## Notes
- Requires Odoo 18.0 or later
- WebSocket support depends on browser compatibility
- For production use, consider adding authentication middleware
- The module runs in the main Odoo process - for heavy loads, consider a separate process
- Default ping interval: 20s, timeout: 60s

## Troubleshooting
- Connection issues: Check server host/port configuration
- Event not received: Verify event names match on both ends
- Permission errors: Ensure proper user authentication
- Performance issues: Consider increasing ping interval/timeout

## License
AGPL-3
