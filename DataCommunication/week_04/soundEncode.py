import numpy as np
import pyaudio
from reedsolo import RSCodec

HANDSHAKE_START_HZ = 8192       # select start hz
HANDSHAKE_END_HZ = 8192 + 512   # select start hz (higher than start hz)

START_HZ = 1024
STEP_HZ = 256
BITS = 4

FEC_BYTES = 4

start_flag = False
end_flag = False

def sound_generate(stream, freq):
    ######insert your code in function######
    for i in range(len(freq)):
        samples = divide_by_tone(freq[i])
        stream.write(samples)

def divide_by_tone(each_data):
    ######insert your code in function######
    return (np.sin(2 * np.pi * np.arange(44100 * 0.5) * each_data / 44100)).astype(np.float32)

def to_freq(step):
    ######insert your code in function######
    if not start_flag:
        return HANDSHAKE_START_HZ
    if end_flag:
        return HANDSHAKE_END_HZ
    return START_HZ + step * STEP_HZ

def encode_byte_data(byte_data):
    data = list()
    for i in range(len(byte_data)):
        data.append(byte_data[i] >> 4)
        data.append(byte_data[i] & 15)
 #   print('bc:', data)
    return data

def data_to_feq_data(fec_payload):
    global start_flag
    global end_flag
    data = list()
    for i in range(len(fec_payload)):
        freq = to_freq(fec_payload[i])
        data.append(freq)
        if freq == HANDSHAKE_START_HZ:
            start_flag = True
            data.append(to_freq(fec_payload[i]))
        if i == len(fec_payload) - 1:
            end_flag = True
            data.append(to_freq(fec_payload[i]))

    print('list:', data)
    return data

def sound_code(fec_payload):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output = True)

    ######insert your code below######
    feq_data = data_to_feq_data(fec_payload)
    sound_generate(stream, feq_data)

def play_sound(msg):
    byte_array = msg
    rs = RSCodec(FEC_BYTES)
    fec_payload = rs.encode(byte_array.encode())
#    print('bs:', fec_payload)
    fec_payload = encode_byte_data(fec_payload)
    sound_code(fec_payload)

if __name__ == '__main__':
    input_msg = input("Input : ")
    play_sound(input_msg)
