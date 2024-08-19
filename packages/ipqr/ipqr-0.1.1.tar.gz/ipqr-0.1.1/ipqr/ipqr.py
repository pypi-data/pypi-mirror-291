import qrcode
import socket
import netifaces
import argparse
from io import StringIO


def get_local_ip():

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        pass

    try:
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            addr = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
            if addr:
                for item in addr:
                    ip = item['addr']
                    if ip != '127.0.0.1' and not ip.startswith('169.254'):
                        return ip
    except:
        pass

    return "127.0.0.1"


def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(data)
    qr.make(fit=True)

    f = StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    return f.read()


def run():
    parser = argparse.ArgumentParser(
        description="Generate QR code for local server URL")
    parser.add_argument("-p", "--port", type=int, default=8000,
                        help="Port number (default: 8000)")
    args = parser.parse_args()

    ip = get_local_ip()
    url = f"http://{ip}:{args.port}"
    qr_code = generate_qr_code(url)
    print(f"Local server URL: {url}")
    print("Scan this QR code to access the local server:")
    print(qr_code)


if __name__ == "__main__":
    run()
