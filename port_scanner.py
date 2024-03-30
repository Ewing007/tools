import socket
import threading

def scan_port(host, port, result_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    if result == 0:
        with open(result_file, 'a') as file:
            file.write(f"Host: {host}\tPort: {port}\tState: filtered\n")
        print(f"Port {port} on host {host} is open")
    sock.close()

def scan_ports(hosts, start_port, end_port, num_threads, result_file):
    print(f"Scanning ports {start_port} to {end_port} on {len(hosts)} hosts...\n")
    # 计算每个线程需要扫描的主机数量
    hosts_per_thread = len(hosts) // num_threads
    remaining_hosts = len(hosts) % num_threads

    threads = []
    # 创建并启动线程
    for i in range(num_threads):
        # 计算当前线程的主机范围
        thread_start = i * hosts_per_thread
        thread_end = thread_start + hosts_per_thread
        # 最后一个线程处理剩余的主机
        if i == num_threads - 1:
            thread_end += remaining_hosts

        # 创建线程并启动
        thread = threading.Thread(target=scan_hosts, args=(hosts[thread_start:thread_end], start_port, end_port, result_file))
        thread.start()
        threads.append(thread)

    # 等待所有线程完成
    for thread in threads:
        thread.join()

def scan_hosts(hosts, start_port, end_port, result_file):
    for host in hosts:
        print(f"Scanning ports on host {host}...")
        for port in range(start_port, end_port + 1):
            scan_port(host, port, result_file)

# 示例用法
if __name__ == '__main__':
    num_hosts = int(input("请输入要扫描的主机数量："))
    hosts = []
    for i in range(num_hosts):
        host = input(f"请输入第{i+1}个主机的地址：")
        hosts.append(host)

    start_port = int(input("请输入开始端口号："))
    end_port = int(input("请输入结束端口号："))
    thread_num = int(input("请输入开启的线程数量："))
    result_file = "alive_ports.txt"

    # 清空结果文件
    open(result_file, 'w').close()

    scan_ports(hosts, start_port, end_port, thread_num, result_file)
    print("Port scanning completed for all hosts.")