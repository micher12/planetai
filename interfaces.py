import scapy.all as scapy

# Lista todas as interfaces disponíveis
print("Interfaces de rede disponíveis:")
for iface in scapy.get_if_list():
    print(f" - {iface}")