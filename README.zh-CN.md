# Odoo SocketIo 模块

[English Version](README.md)

## 概述
本模块为Odoo提供基于Socket.IO的实时通信能力，实现服务端与网页客户端的双向事件通信。

## 功能特性
- 基于事件的实时通信
- 支持WebSocket传输
- 基于用户的连接管理
- 支持房间(room)消息机制
- 内置重连处理
- 与Odoo通知系统集成
- 管理员测试界面

## 安装配置
1. 像普通模块一样安装
2. 确保安装以下依赖：
   ```bash
   pip install python-socketio==5.13.0
   ```
3. 在Odoo配置文件中设置Socket.IO端口：
   ```ini
   [options]
   socketio_port = 3000
   ```

## 服务端配置
模块会在Odoo启动时自动启动Socket.IO服务，主要特性：

- 运行在配置指定的端口（默认：3000）
- 支持WebSocket传输
- 维护用户连接映射
- 处理客户端事件

### 服务端API
```python
# 推送消息到客户端
self.env['odoo.socketio'].push_socketio_event({
    'event': '事件名称',
    'data': {'key': 'value'},
    'uid': user_id,  # 目标用户ID
    # 可选: 'room': '房间名称'
})

# 获取配置端口
port = self.env['odoo.socketio'].get_socketio_port()
```

## 客户端使用
模块提供了易用的JavaScript服务：

```javascript
// 获取socketio服务
const socketioService = await this.env.services.socketio_service;

// 订阅事件
socketioService.on('事件名称', (data) => {
    console.log('收到:', data);
});

// 发送事件
socketioService.emit('事件名称', {key: 'value'});

// 监听连接状态
socketioService.onServiceEvent('odoo_socketio_connect', () => {
    console.log('已连接Socket.IO');
});
```

## 示例
### 服务端(Python)
```python
# 发送通知给用户
self.env['odoo.socketio'].push_socketio_event({
    'event': 'user_notification',
    'data': {'message': '来自服务端的问候!'},
    'uid': user.id
})
```

### 客户端(JavaScript)
```javascript
// 在Odoo组件中
setup() {
    this.socketioService = useService('socketio_service');
    this.socketioService.on('user_notification', (data) => {
        this.env.services.notification.add(data.message);
    });
}
```

## 测试
管理员可以通过以下路径测试功能：
`设置 → 用户 → 选择用户 → Test Socketio Notify 标签页`

## 注意事项
- 需要Odoo 18.0或更高版本
- WebSocket支持取决于浏览器兼容性
- 生产环境建议添加认证中间件
- 模块运行在主Odoo进程中 - 高负载场景建议使用独立进程

## 许可证
AGPL-3
