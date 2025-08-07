# Reverse-SOCKS5-proxy-through-SSH-tunnel
基于Python脚本开发的轻量级解决方案，能够快速搭建内网设备的网络代理服务。实现条件极为简单，只要目标设备具备SSH连接能力，即可创建稳定的网络访问链路。

### 适用场景
适用于所有服务器无法直接访问互联网，但开放了SSH端口供客户端连接的环境。在此配置下，客户端需具备互联网访问能力。下图展示了一个典型应用场景（实际网络环境可以比图示更加复杂，只要能够建立SSH连接即可实现功能）。
![示意图](./illustration.png)

### 使用要求
1. 服务器需开放SSH端口以支持远程连接
2. 客户端需具备访问公网的能力
3. 两端系统均需安装Python环境（仅依赖标准库）

### 使用教程
1. 使用SSH建立端口转发（隧道）
本地terminal执行：`ssh -L 127.0.0.1:8080:内部服务器:80 user@网关服务器`
效果：将本地8080端口的流量通过SSH隧道转发到内网服务器的80端口

2. 服务器运行[Tunnel_server.py](./Tunnel_server.py)

### Test example
`sudo proxychains apt download <package-name>`  
`pip install --proxy socks5h://127.0.0.1:9000 numpy`  
`curl -v --proxy socks5h://127.0.0.1:9000 https://www.baidu.com`
