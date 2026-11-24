"""Small, bounded ICMP exercise for networks you own or may test."""
import ipaddress
import time

def validate_inputs(source, destination, count):
    for address in (source, destination):
        parsed = ipaddress.ip_address(address)
        if parsed.version != 4 or parsed.is_unspecified or parsed.is_multicast:
            raise ValueError("Use specific unicast IPv4 addresses")
    count = int(count)
    if not 1 <= count <= 10:
        raise ValueError("Choose 1 to 10 packets")
    return source, destination, count

def send_probes(source, destination, count, sr1, IP, ICMP, pause=time.sleep):
    source, destination, count = validate_inputs(source, destination, count)
    received = 0
    for index in range(count):
        packet = IP(src=source, dst=destination) / ICMP(seq=index)
        response = sr1(packet, timeout=2, verbose=0)
        if response is not None:
            if response.haslayer(ICMP) and response[ICMP].type == 0 and response[ICMP].seq == index and response.src == destination:
                received += 1
                print(response.summary())
            else:
                print("Received a response, but not a matching echo reply")
        else:
            print("No reply within 2 seconds")
        if index + 1 < count:
            pause(1)
    print(f"Sent: {count}; matching replies: {received}; unanswered: {count - received}")
    return received

def main():
    try:
        from scapy.all import IP, ICMP, sr1
    except ImportError:
        print("Install the optional runtime dependency: python -m pip install -r requirements.txt")
        return 1
    try:
        source = input("Local interface IPv4 address: ").strip()
        destination = input("Authorized destination IPv4 address: ").strip()
        count = input("Packets (1-10): ").strip()
        send_probes(source, destination, count, sr1, IP, ICMP)
        return 0
    except (ValueError, OSError, PermissionError) as error:
        print(f"Error: {error}")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nStopped")
        return 130

if __name__ == "__main__":
    raise SystemExit(main())
