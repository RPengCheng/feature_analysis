import pyshark

# 指定服务器的IP和端口
server_ip = "127.0.0.1"
server_port = 8000

# 设置过滤规则，只捕获服务器到客户端或客户端到服务器的TCP流量
filter_rule = f"ip.addr == {server_ip} and tcp.port == {server_port}"

# 创建一个抓包会话
capture = pyshark.FileCapture(
    'temp.pcap', display_filter=filter_rule, only_summaries=True
)

# 开始捕获数据包并调用回调函数处理每个捕获的数据包
for packet in capture.sniff_continuously(packet_count=10):
    print(packet)

capture.close()