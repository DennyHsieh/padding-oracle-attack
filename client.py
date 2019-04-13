import telnetlib
import binascii


def query(msg_test):
    '''ask the server if the ciphertext is valid'''
    tn.write(msg_test.encode("utf-8") + b'\r\n')

    ret = tn.read_until(b".\n", timeout=3)

    if ret.find(b"invalid") != -1:
        # print(b"invalid")
        return False
    elif ret.find(b"valid") != -1:
        # print(b"valid")
        return True
    else:
        print(ret)


def to_hex(s):
    '''string to hex'''
    return ''.join("{:02x}".format(ord(c)) for c in s)


def to_str(s):
    '''hex to string'''
    return s and chr(int(s[:2], base=16)) + to_str(s[2:]) or ''


def int2hex(i):
    return hex(i)[2:] if len(hex(i)[2:]) == 2 else '0' + hex(i)[2:]


def exor_pad(i):
    '''try integer 1 to 16
    :return 16 byte str with padding 0 in the front'''
    assert (i > 0)
    assert (i <= 16)
    return '00' * (16 - i) + int2hex(i) * i


def exor_guess(guess, pos):
    '''
    :param guess: guess integer
    :param pos: position of XOR (0-15)
    :return: 16 byte str with padding 0 in the front and end
    '''
    assert (pos >= 0)
    assert (pos < 16)
    return '00' * (15 - pos) + int2hex(guess) + '00' * pos


def refill_zero(s):
    '''
    append 0 to front string until len(str) = 32
    :return: str
    '''
    return '0' * (32 - len(s)) + s


def strxor(a, b):
    '''
    xor two strings with different lengths
    Note: a XOR b in python: chr(ord(a) ^ ord(b))
    :return: XOR string result
    '''
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


def hex_xor(s1, s2):
    '''
    xor two hex by decode string to hex
    :return: XOR string result
    '''
    return to_hex(strxor(to_str(s1), to_str(s2)))


def test_a_byte(found_msg, pos, dictionary_, iv, ct, is_padding=False):
    '''
    Try a byte to get the plaintext
    :param found_msg: the hex_str has already been found
    :param pos: byte position of hex backward from 1-16 which will be tried by int between 0-255
    :param dictionary_: int range between 0-255
    :param iv: hex_str to be XORed
    :param ct: ciphertext to be decrypted
    :param is_padding: check the padding validity of ciphertext, default=False
    :return: hex(plaintext)
    '''
    pad = exor_pad(pos)
    lastmsg = refill_zero(to_hex(found_msg))
    getletter = False
    possible_padding = []
    for guess in dictionary_:
        guess_pad = exor_guess(guess, pos - 1)
        # Try all possible situation
        send_ek = hex_xor(lastmsg, hex_xor(iv, hex_xor(guess_pad, pad))) + ct
        # while len(send_ek) < 256:
        #     send_ek = '00' + send_ek
        # print(send_ek.encode("utf-8"))
        if query(send_ek):
            getletter = True
            new_msg = to_str(int2hex(guess)) + found_msg
            if is_padding:
                possible_padding.append(guess)
            else:
                return new_msg
    if is_padding:
        return possible_padding
    if getletter is False:
        return None


if __name__ == "__main__":
    HOST = "140.122.185.174"

    tn = telnetlib.Telnet(HOST, 8081)
    tn.read_until(b"---\n")
    ciphertext = tn.read_until(b"---\n")[:-5]
    ciphertext_decrypt = binascii.unhexlify(ciphertext)

    print("The whole ciphertext is:")
    print(ciphertext)
    print("\nDirectly decrypt the ciphertext, and we can see the plaintext of IV of first 16 bytes")
    print(ciphertext_decrypt)

    tn.read_until(b"What is your ciphertext?\n")

    N = 16
    printable_chars = range(32, 128)
    padding_chars = range(1, 17)
    inter_text = ''

    #  Change to Dec
    ek_liststr = list(ciphertext)
    # print(ek_liststr)
    # print(type(ek_liststr[-1]))

    iv_lt = ek_liststr[:32]
    iv_origin = bytes(iv_lt)

    # Divide ciphertext into block
    blocks = []
    ciphertext_decode = ciphertext.decode("utf-8")
    while ciphertext_decode:
        blocks.append(ciphertext_decode[:32])
        ciphertext_decode = ciphertext_decode[32:]
    # print(blocks)

    for index in range(1, 8):
        b_index = 8 - index
        print("\n======")
        print('Start to try block', b_index + 1)
        iv = blocks[b_index - 1]
        block = blocks[b_index]
        print("The IV(temp) encrypted text we need to change elements is:" + iv)
        print("The block we want to try is:" + block)

        # Try the validity of the padding for the last block
        is_last_block = False
        if b_index == len(blocks)-1:
            is_last_block = True
        if is_last_block:
            possible_paddings = test_a_byte('', 1, padding_chars, iv, block, True)
            # Test the validity of the padding after chosen
            for i in possible_paddings:
                print("possible padding size is:", i)
                msg = chr(i) * i
                start_byte = i + 1
                if test_a_byte(msg, start_byte, printable_chars, iv, block) is not None:
                    print("good padding size is:", i)
                    break
        else:
            msg = ''
            start_byte = 1

        # Decrypted the byte one by one to the chosen block of 16byte
        for pos in range(start_byte, 17):
            is_found = test_a_byte(msg, pos, printable_chars, iv, block)
            if is_found:
                msg = is_found
                print("%r" % msg)
            else:
                print("can't found the last #%d byte" % pos)
                exit(0)
            if pos == 16:
                inter_text = msg + inter_text
        if is_last_block and msg:
            print("If remove padding off, the last block is:\n%r" % msg[:-(start_byte - 1)])
            inter_text = msg[:-(start_byte - 1)]

    print("The plaintext_hex is:", inter_text)
    print("The IV is:", to_str(iv_origin))
    print("The plaintext is:", to_str(inter_text))
