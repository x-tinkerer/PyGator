import struct

sammary = bytearray([
0x03,0xaf,0x00,0x00,0x00,0x01,0x01,0x0b,0x31,0x0a,0x32,0x0d,0x0a,0x33,0x0d,0x34,
0x0a,0x0d,0x35,0xd5,0xe1,0xd8,0xc1,0xf5,0xd1,0x9c,0x9f,0x14,0xff,0xf9,0x9e,0x9a,
0xb2,0xbe,0xd0,0x00,0x85,0xec,0xd1,0x89,0x97,0xbd,0xc3,0x00,0x05,0x75,0x6e,0x61,
0x6d,0x65,0xe3,0x00,0x4c,0x69,0x6e,0x75,0x78,0x20,0x6c,0x6f,0x63,0x61,0x6c,0x68,
0x6f,0x73,0x74,0x20,0x33,0x2e,0x31,0x38,0x2e,0x32,0x32,0x2d,0x75,0x73,0x65,0x72,
0x2d,0x30,0x31,0x32,0x30,0x31,0x2d,0x67,0x32,0x38,0x61,0x30,0x62,0x64,0x61,0x20,
0x23,0x34,0x20,0x53,0x4d,0x50,0x20,0x50,0x52,0x45,0x45,0x4d,0x50,0x54,0x20,0x53,
0x61,0x74,0x20,0x4d,0x61,0x72,0x20,0x31,0x39,0x20,0x31,0x30,0x3a,0x35,0x36,0x3a,
0x35,0x36,0x20,0x43,0x53,0x54,0x20,0x32,0x30,0x31,0x36,0x20,0x61,0x61,0x72,0x63,
0x68,0x36,0x34,0x20,0x47,0x4e,0x55,0x08,0x50,0x41,0x47,0x45,0x53,0x49,0x5a,0x45,
0x04,0x34,0x30,0x39,0x36,0x09,0x6d,0x61,0x6c,0x69,0x5f,0x74,0x79,0x70,0x65,0x03,
0x36,0x78,0x78,0x00,0x03,0x11,0x00,0x00,0x00,0x01,0x03,0x00,0x83,0xba,0x10,0x0a,
0x43,0x6f,0x72,0x74,0x65,0x78,0x2d,0x41,0x35,0x33,0x03,0x11,0x00,0x00,0x00,0x01,
0x03,0x01,0x83,0xba,0x10,0x0a,0x43,0x6f,0x72,0x74,0x65,0x78,0x2d,0x41,0x35,0x33,
0x03,0x11,0x00,0x00,0x00,0x01,0x03,0x02,0x83,0xba,0x10,0x0a,0x43,0x6f,0x72,0x74,
0x65,0x78,0x2d,0x41,0x35,0x33,0x03,0x11,0x00,0x00,0x00,0x01,0x03,0x03,0x83,0xba,
0x10,0x0a,0x43,0x6f,0x72,0x74,0x65,0x78,0x2d,0x41,0x35,0x33,0x03,0x11,0x00,0x00,
0x00,0x01,0x03,0x04,0x83,0xba,0x10,0x0a,0x43,0x6f,0x72,0x74,0x65,0x78,0x2d,0x41,
0x35,0x33,0x03,0x0c,0x00,0x00,0x00,0x01,0x03,0x05,0x7f,0x07,0x55,0x6e,0x6b,0x6e,
0x6f,0x77,0x6e,0x03,0x0c,0x00,0x00,0x00,0x01,0x03,0x06,0x7f,0x07,0x55,0x6e,0x6b,
0x6e,0x6f,0x77,0x6e,0x03,0x0c,0x00,0x00,0x00,0x01,0x03,0x07,0x7f,0x07,0x55,0x6e,
0x6b,0x6e,0x6f,0x77,0x6e,0x03,0x11,0x00,0x00,0x00,0x01,0x03,0x08,0x88,0xba,0x10,
0x0a,0x43,0x6f,0x72,0x74,0x65,0x78,0x2d,0x41,0x37,0x32,0x03,0x0c,0x00,0x00,0x00,
0x01,0x03,0x09,0x7f,0x07,0x55,0x6e,0x6b,0x6e,0x6f,0x77,0x6e,0x03,0x0d,0x00,0x00,
0x00,0x04,0x8c,0x39,0x00,0x7f,0x8e,0x82,0xee,0x88,0x97,0xbd,0xc3,0x00])


class UnPack:
    def __init__(self, data, pos):
        self.buf = data
        self.cur = pos

"""
    /**
     * Reads an signed integer from {@code in}.
     */
    public static int readSignedLeb128(ByteInput in) {
        int result = 0;
        int cur;
        int count = 0;
        int signBits = -1;
        do {
            cur = in.readByte() & 0xff;
            result |= (cur & 0x7f) << (count * 7);
            signBits <<= 7;
            count++;
        } while (((cur & 0x80) == 0x80) && count < 5);
        if ((cur & 0x80) == 0x80) {
            throw new DexException("invalid LEB128 sequence");
        }
        // Sign extend if appropriate
        if (((signBits >> 1) & result) != 0 ) {
            result |= signBits;
        }
        return result;
    }
"""

def recv_Respons(sock):
    head = sock.recv(5)
    print repr(head)
    listhead= list(bytearray(head))
    buftype =listhead[0]
    #buftype =head.encode("hex")
    if buftype == 1:
        envlen = readLEInt(head[1:], 4)
        data = sock.recv(envlen)
        print 'Received xml:'
        print data
    elif buftype == 3:
        envlen = readLEInt(head[1:], 4)
        data = sock.recv(envlen)
        if IsSammay(data):
            DecodeSam(data)
        else:
            #print repr(data)
            writeToFile(data)

def writeToFile(buf):
    target = open('00000000', 'a+')
    target.write(buf)
    target.close()

def readLEInt(inbytes,size):
    result = 0
    for count in range(0, size-1):
        cur = ord(inbytes[count])
        result |= (cur & 0xff) << (count * 8)

    return result


def readString(inbytes,size):
    result = ''.join(cur for cur in inbytes[:size])
    return size, result

def readBytes(inbytes,size):
    result = 0
    for count in range(0,size):
        cur = ord(inbytes[count])
        result |= (cur & 0xff) << (count * 8)

    return size, result

def unpackInt(inbytes):
    result = 0
    count = 0
    more = True
    signBits = -1
    while more:
        cur = ord(inbytes[count])
        result |= (cur & 0x7f) << (count * 7)
        signBits <<= 7
        count += 1
        if cur & 0x80 != 0x80:
            more = False

    if (signBits >> 1) & result != 0:
        result |= signBits
    return count, result

def unpackInt64(inbytes):
    result = 0
    count = 0
    more = True
    signBits = -1
    while more:
        cur = ord(inbytes[count])
        result |= (cur & 0x7f) << (count * 7)
        signBits <<= 7
        count += 1
        if cur & 0x80 != 0x80:
            more = False;

    if (signBits >> 1) & result != 0:
            result |= signBits
    return count, result

def IsSammay(sambuf):
    if sambuf[1] == 1 and sambuf[2] == 1:
        return True
    else:
        return False

def DecodeSam(sambuf):
    mPos=0

    Bytes, mValue = unpackInt(sambuf[mPos:])
    mPos += Bytes
    print "Frame Type: " + str(mValue)

    Bytes, mValue = unpackInt(sambuf[mPos:])
    mPos += Bytes
    print "Code: " + str(mValue)

    Bytes, mValue = unpackInt(sambuf[mPos:])
    mPos += Bytes
    strLen = mValue
    #print "Canary Size: " + str(mValue)

    Bytes, mValue = readString(sambuf[mPos:], strLen)
    mPos += Bytes
    print "Canary is:" + mValue

    Bytes, mValue = unpackInt64(sambuf[mPos:])
    mPos += Bytes
    print "Timestamp is:" + str(mValue)

    Bytes, mValue = unpackInt64(sambuf[mPos:])
    mPos += Bytes
    print "Uptime is:" + str(mValue)

    Bytes, mValue = unpackInt64(sambuf[mPos:])
    mPos += Bytes
    print "Delta is:" + str(mValue)

    while True:
        Bytes, mValue = unpackInt(sambuf[mPos:])
        mPos += Bytes
        strLen = mValue
        #print "str1 Size: " + str(mValue) + "\nRead " + str(Bytes) + " Bytes, Current pos is " + str(mPos)

        Bytes, mValue = readString(sambuf[mPos:], strLen)
        mPos += Bytes
        #print "str1 is:" + mValue + "\nRead "+str(Bytes) + " Bytes, Current pos is " + str(mPos)
        print mValue

        if mValue =='' :
            break

if __name__ == '__main__':
    DecodeSam(sammary)

