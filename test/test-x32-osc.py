import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2)
for port in (10023, 10024):
    s.sendto(b'/info\x00\x00\x00', ('192.168.240.250', port))
    try:
        print(port, s.recvfrom(1024)[0])
    except (socket.timeout, ConnectionRefusedError) as e:
        print(port, 'no answer:', e)
