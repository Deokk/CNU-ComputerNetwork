import struct
from pylibpcap.pcap import sniff
from pylibpcap import get_iface_list

using_iface = get_iface_list()[0]

def split_header(data):
	ethernet_header = data[:14]
	eth_header_parser(ethernet_header)

	ip_header = data[14:34]
	ip_header_parser(ip_header)

	ip_header = struct.unpack('!20B', ip_header)
	ip_protocol = (format(ip_header[9], '02x'))
	ip_protocol = int(ip_protocol, 16)

	ip_variable = (format(ip_header[0], '02x'))
	ip_length = (int(ip_variable[1]))
	tmp = 14 + (4 * ip_length)

	if ip_protocol == 6:
		tcp_header = data[tmp:tmp+20]
		tcp_header_parser(tcp_header)

	if ip_protocol == 17:
		udp_header = data[tmp:tmp+8]
		udp_header_parser(udp_header)

def eth_header_parser(data):
	ethernet_header = struct.unpack('!6B6BH', data)

	src_ethernet_addr = list()
	dst_ethernet_addr = list()

	for dst_et in ethernet_header[:6]:
		dst_ethernet_addr.append(format(dst_et, '02x'))
	for src_et in ethernet_header[6:12]:
		src_ethernet_addr.append(format(src_et, '02x'))

	typ_ethernet = list()

	for typ_et in ethernet_header[12:]:
		typ_ethernet.append(format(typ_et, '02x'))

	dst_ethernet_addr = ":".join(dst_ethernet_addr)
	src_ethernet_addr = ":".join(src_ethernet_addr)
	typ_ethernet = "".join(typ_ethernet)

	print("###### [ Ethernet_header ] ######")
	print("dst_mac_address:", dst_ethernet_addr)
	print("src_mac_address:", src_ethernet_addr)
	print("ip_version: 0x" + typ_ethernet)

def ip_header_parser(data):
	ip_header = struct.unpack('!20B', data)
	
	ip_total = list()
	for ip_i in ip_header[:20]:
		ip_total.append(format(ip_i, '02x'))
	ip_total = "".join(ip_total)

	ip_length = list()
	ip_total_length = list()
	ip_header_checksum = list()
	ip_src_ad = list()
	ip_dst_ad = list()

	ip_variable = (format(ip_header[0], '02x'))
	ip_version = (ip_variable[0])
	ip_length = (ip_variable[1])

	for tol_ip in ip_header[2:4]:
		ip_total_length.append(format(tol_ip, '02x'))
	ip_total_length = "".join(ip_total_length)
	ip_total_length = int(ip_total_length, 16)

	ip_TTL = (format(ip_header[8], '02x'))
	ip_TTL = int(ip_TTL, 16)

	ip_protocol = (format(ip_header[9], '02x'))
	ip_protocol = int(ip_protocol, 16)

	for ip_chc in ip_header[10:12]:
		ip_header_checksum.append(format(ip_chc, '02x'))
	ip_header_checksum = "".join(ip_header_checksum)

	for ip_src in ip_header[12:16]:
		ip_src_ad.append(str(ip_src))
	ip_src_ad = ".".join(ip_src_ad)

	for ip_dst in ip_header[16:20]:
		ip_dst_ad.append(str(ip_dst))
	ip_dst_ad = ".".join(ip_dst_ad)

	print("###### [ IP_header ] ######")
	print("ip_header:", ip_total)
	print("ip_version:", ip_version)
	print("ip_Length:", ip_length)
	print("total_length:", ip_total_length)
	print("Time to live:", ip_TTL)
	print("protocol:", ip_protocol)
	print("header checksum: 0x" + ip_header_checksum)
	print("source_ip_address:", ip_src_ad)
	print("dest_ip_address:", ip_dst_ad)

def udp_header_parser(data):
	udp_header = struct.unpack('!8B', data)
	
	udp_total = list()
	for udp_i in udp_header[:8]:
		udp_total.append(format(udp_i, '02x'))
	udp_total = "".join(udp_total)

	udp_src = list()
	udp_dst = list()
	udp_length = list()
	udp_checksum = list()

	for src_u in udp_header[0:2]:
		udp_src.append(format(src_u, '02x'))
	udp_src = "".join(udp_src)
	udp_src = int(udp_src, 16)

	for dst_u in udp_header[2:4]:
		udp_dst.append(format(dst_u, '02x'))
	udp_dst = "".join(udp_dst)
	udp_dst = int(udp_dst, 16)

	for len_u in udp_header[4:6]:
		udp_length.append(format(len_u, '02x'))
	udp_length = "".join(udp_length)
	udp_length = int(udp_length, 16)

	for chc_u in udp_header[6:8]:
		udp_checksum.append(format(chc_u, '02x'))
	udp_checksum = "".join(udp_checksum)

	print("###### [ UDP_header ] ######")
	print("udp_header:", udp_total)
	print("src_port:", udp_src)
	print("dst_port:", udp_dst)
	print("length:", udp_length)
	print("header checksum: 0x" + udp_checksum)

def tcp_header_parser(data):
	tcp_header = struct.unpack('!20B', data)
	
	tcp_total = list()
	for tcp_i in tcp_header[:20]:
		tcp_total.append(format(tcp_i, '02x'))
	tcp_total = "".join(tcp_total)

	tcp_src = list()
	tcp_dst = list()
	tcp_seq = list()
	tcp_ack = list()
	tcp_checksum = list()

	for src_t in tcp_header[0:2]:
		tcp_src.append(format(src_t, '02x'))
	tcp_src = "".join(tcp_src)
	tcp_src = int(tcp_src, 16)

	for dst_t in tcp_header[2:4]:
		tcp_dst.append(format(dst_t, '02x'))
	tcp_dst = "".join(tcp_dst)
	tcp_dst = int(tcp_dst, 16)

	for seq_t in tcp_header[4:8]:
		tcp_seq.append(format(seq_t, '02x'))
	tcp_seq = "".join(tcp_seq)
	tcp_seq = int(tcp_seq, 16)

	for ack_t in tcp_header[8:12]:
		tcp_ack.append(format(ack_t, '02x'))
	tcp_ack = "".join(tcp_ack)
	tcp_ack = int(tcp_ack, 16)

	tcp_HLEN = (format(tcp_header[12], '02x'))
	tcp_HLEN = tcp_HLEN[0]

	for chc_t in tcp_header[16:18]:
		tcp_checksum.append(format(chc_t, '02x'))
	tcp_checksum = "".join(tcp_checksum)
	tcp_checksum = int(tcp_checksum, 16)

	print("###### [ TCP_header ] ######")
	print("tcp_header:", tcp_total)
	print("src_port:", tcp_src)
	print("dst_port:", tcp_dst)
	print("seq_num:", tcp_seq)
	print("ack_num:", tcp_ack)
	print("HLEN:", tcp_HLEN)
	print("checksum:", tcp_checksum)

if __name__ == '__main__':
	for plen, t, buf in sniff(using_iface, count=3):
		split_header(buf)
		print("===========================================================")

