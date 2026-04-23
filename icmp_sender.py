from scapy.all import IP, ICMP, sr1


while True:
    try:
        print("icmp tool")

        src_ip = input("Input Source IP: ")
        dst_ip = input("Input Destination IP: ")
        count_icmp = int(input("Input number of packets: "))

        print(f"\n{src_ip} --------> {dst_ip}\n")

        success = 0

        for i in range(count_icmp):
            packet = IP(src=src_ip, dst=dst_ip) / ICMP(seq=i)

            
            response = sr1(packet,  verbose=0)
           

            if response:
                print(f"\n{src_ip} --------> {dst_ip}\n")
                print(f"Reply {i} response :\n {response.show}\n")
                print("-----------------------------------------------\n")
                success += 1

            else:
                print(f"\n{src_ip} --------> {dst_ip}\n")
                print(f"Reply {i}: Request faild")

        print("\n=== Statistics ===")
        print(f"Sent: {count_icmp}")
        print(f"Received: {success}")
        print(f"Lost: {count_icmp - success}")

        command = input("\nType 'exit' to quit or press Enter to continue: ")

        if command.lower() == "exit":
            break

    except Exception as e:
        print("Error:", e)
        continue