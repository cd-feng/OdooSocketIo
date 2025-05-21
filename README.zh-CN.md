# Odoo SocketIo 模块

[English](README.md)

## 概述
本模块使用Socket.IO为Odoo提供实时通信能力，实现Odoo服务器与Web客户端之间的双向事件驱动通信。

## 功能特性
- 基于事件的实时通信
- 支持WebSocket传输
- 基于用户的连接管理
- 支持房间(room)消息机制
- 内置重连处理
- 与Odoo通知系统集成
- 管理员调试接口
- 支持自定义事件处理
- 线程安全的消息处理

## 安装
1. 像常规模块一样在Odoo中安装
2. 确保安装以下依赖：
   ```bash
   pip install python-socketio==5.13.0 aiohttp
   ```
3. 在安装完模块后，通过"设置"、“SocketIo”下设置运行参数，并重启Odoo


## 服务器配置
模块在Odoo启动时会自动启动Socket.IO服务器。主要特性：

- 运行在指定主机:端口(默认: 0.0.0.0:3000)
- 支持WebSocket传输
- 维护用户连接映射
- 处理客户端事件
- 线程安全的消息队列处理

### 服务器API
```python
# 推送消息到客户端
self.env['odoo.socketio'].push_socketio_event({
    'event': 'your_event_name',
    'data': {'key': 'value'},
    'uid': user_id,  # 目标用户ID
    # 可选: 'room': 'room_name'
})

# 获取配置的端口
port = self.env['odoo.socketio'].get_socketio_conf().get('socketio_server_port')

# 处理自定义事件(在您的模型中重写)
def deal_custom_event(self, event, sid, data):
    # 您的自定义事件处理逻辑
    super().deal_custom_event(event, sid, data)
```

## 客户端使用
在您的资源中包含socket.io.min.js并使用标准Socket.IO客户端API：

```javascript
// 连接到服务器
const socket = io('http://localhost:3000', {
    path: '/socket.io',
    query: {
        uid: user_id,  // 当前用户ID
        room: 'room_name'  // 可选房间名
    }
});

// 订阅事件
socket.on('event_name', (data) => {
    console.log('收到:', data);
});

// 发送事件
socket.emit('event_name', {key: 'value'});

// 连接状态
socket.on('connect', () => {
    console.log('已连接到Socket.IO');
});
```

## 示例
### 服务端(Python)
```python
# 发送通知给用户
self.env['odoo.socketio'].push_socketio_event({
    'event': 'user_notification',
    'data': {'message': '来自服务器的问候!'},
    'uid': user.id
})

# 处理自定义事件
def deal_custom_event(self, event, sid, data):
    if event == 'custom_action':
        # 处理自定义动作
        self.do_something(data)
    super().deal_custom_event(event, sid, data)
```

### 客户端(JavaScript)
```javascript
// 在您的Odoo组件中
const socket = io('http://localhost:3000', {
    path: '/socket.io',
    query: {uid: current_user_id}
});

socket.on('user_notification', (data) => {
    this.env.services.notification.add(data.message);
});

socket.emit('custom_action', {action: 'refresh'});
```

## 测试
管理员可以从以下位置测试功能：
`设置 → 用户 → 选择用户 → Test Socketio Notify标签页`

## 注意事项
- 需要Odoo 18.0或更高版本
- WebSocket支持取决于浏览器兼容性
- 生产环境使用建议添加认证中间件
- 模块运行在主Odoo进程中 - 对于高负载场景，建议使用独立进程
- 默认ping间隔: 20秒, 超时: 60秒

## 故障排除
- 连接问题: 检查服务器主机/端口配置
- 未收到事件: 确认两端事件名称匹配
- 权限错误: 确保正确的用户认证
- 性能问题: 考虑增加ping间隔/超时时间

## 许可证
AGPL-3
