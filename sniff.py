from scapy.all import sniff, wrpcap
import os

def packet_callback(packet):
    print(packet.summary())
    file_name = os.path.join('./sniff','captured_traffic.pcap')
    wrpcap(file_name, packet, append=True)
# 指定服务器的IP和端口
server_ip = "127.0.0.1"
server_port = 8000

# 设置过滤规则，只捕获客户端到服务器的TCP流量
filter_rule = f"src host {server_ip} and dst port {server_port}"

# 开始嗅探网络流量并调用packet_callback处理每个捕获的数据包
print('begin')
# sniff(filter=filter_rule, prn=packet_callback, store=0,count=1)
sniff(filter=filter_rule, prn=packet_callback, store=0, count=0,  promisc=True, timeout=10)
print('end')