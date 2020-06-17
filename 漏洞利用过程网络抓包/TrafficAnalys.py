from scapy.all import *
from scapy.layers.inet import TCP


def antSword():
    packets = rdpcap('antshell.pcap')
    print(packets)
    # packets.show()
    for data in packets:
        s = str(data.payload.payload.payload)
        if 'bl-content' in s and 'tmp' in s and 'shell' in s:
            print("use :", data[TCP].load)
        if 'upload-images' in s:
            print("upload webshell:", data[TCP].load)


def reverseShell():
    packets = rdpcap('reverseShell.pcap')
    print(packets)
    # packets.show()
    for data in packets:
        s = str(data.payload.payload.payload)
        if 'bl-content' in s and 'tmp' in s and 'rshell' in s:
            print("use:", data[TCP].load)
        if 'upload-images' in s:
            print("upload:", data[TCP].load)


if __name__ == '__main__':
    print("--------antsword---------")
    antSword()
    print("--------reverseshell------")
    reverseShell()
