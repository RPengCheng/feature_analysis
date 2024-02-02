from scapy.all import sniff, wrpcap

def packet_callback(packet):
    print(packet.summary())
    wrpcap('captured_traffic.pcap', packet, append=True)
# 指定服务器的IP和端口
server_ip = "127.0.0.0"
server_port = 8000

# 设置过滤规则，只捕获服务器到客户端或客户端到服务器的TCP流量
filter_rule = f"host {server_ip} and port {server_port}"

# 开始嗅探网络流量并调用packet_callback处理每个捕获的数据包
sniff(filter=filter_rule, prn=packet_callback, store=0)