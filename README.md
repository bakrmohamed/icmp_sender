# ICMP Sender

A small Scapy exercise for learning IPv4 echo requests and replies on a network you own or have permission to test. This is not a scanner or load-testing tool.

```bash
python -m pip install -r requirements.txt
python icmp_sender.py
python -m unittest -v
```

Enter the IPv4 address actually assigned to your local interface, an authorized destination IPv4 address and a count from 1 to 10. Each request waits at most two seconds and requests are spaced by a one-second pause. Matching echo replies are counted separately from other ICMP responses.

Raw packets usually require OS-specific privileges and packet-capture support. Do not use a forged source address. The program validates IPv4 syntax but does not prove that an address belongs to you or that a network permits the test. Avoid broadcast addresses. Firewalls and rate limits can suppress replies; no reply does not prove a host is down.

The offline tests mock packet transmission. No live packets were sent during verification, and Windows capture-driver setup has not been tested.
