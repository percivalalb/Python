from datacomplier import dataoutput, datainput

packet_dict = {} #Maps channel name to packet class

class packet():

    def __init__(self, channel):
        self.data = None
        self.channel = channel

    def read(self, do):
        print('read')

    def write(self, di):
        pass

    def execute(self, screen):
        pass

#Handles data and converts it to a packet and excutes the data
def recive_packet(data, screen):
    di = datainput(data)
    while not di.has_read_everything():
        channel = di.readString()
        if channel not in packet_dict.keys():
            print('Recived data with unknown packet mapping')
            return

        packet = packet_dict[channel]()
        packet.read(di)
        packet.execute(screen);

def write_packet(packets):
    do = dataoutput()
    for packet in packets:
        do.writeString(packet.channel)
        packet.write(do)
    if len(do.data) > 1024:
        print('TOO BIG PACKET')
    return do.data

#Registers a channel to a packet
def register_channel(channel, packet):
    if channel in packet_dict.keys():
        print('The channel name %s is already in use' % channel)
        return False

    packet_dict[channel] = packet
