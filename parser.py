import os
import struct


class Parser:

    def __init__(self, data, pos):
        """

        :type pos: object
        """
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

def isReady(sock, filename):
    head = sock.recv(5)
    print repr(head)
    buftype, = struct.unpack('B', head[0])
    bufsize, = struct.unpack('I', head[1:])

    if buftype == 3:
        data = sock.recv(bufsize)
        if isSummary(data):
            decodeSummary(data)
        writeToFile(filename, head)
        writeToFile(filename, data)
    return True


def recv_Data(sock, buff):
    buff = sock.recv(4096)

def readString(inbytes, size):
    result = ''.join(cur for cur in inbytes[:size])
    return size, result


def readBytes(inbytes, size):
    result = 0
    for count in range(0, size):
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


def isSummary(sumbuf):
    sumType, = struct.unpack('B', sumbuf[0])
    sumCode, = struct.unpack('B', sumbuf[1])
    if sumType == 1 and sumCode == 1:
        return True
    else:
        return False


def decodeSummary(sumbuf):
    mPos = 0

    Bytes, mValue = unpackInt(sumbuf[mPos:])
    mPos += Bytes
    print "Frame Type: " + str(mValue)

    Bytes, mValue = unpackInt(sumbuf[mPos:])
    mPos += Bytes
    print "Code: " + str(mValue)

    Bytes, mValue = unpackInt(sumbuf[mPos:])
    mPos += Bytes
    strLen = mValue
    # print "Canary Size: " + str(mValue)

    Bytes, mValue = readString(sumbuf[mPos:], strLen)
    mPos += Bytes
    print "Canary is:" + mValue

    Bytes, mValue = unpackInt64(sumbuf[mPos:])
    mPos += Bytes
    print "Timestamp is:" + str(mValue)

    Bytes, mValue = unpackInt64(sumbuf[mPos:])
    mPos += Bytes
    print "Uptime is:" + str(mValue)

    Bytes, mValue = unpackInt64(sumbuf[mPos:])
    mPos += Bytes
    print "Delta is:" + str(mValue)

    while True:
        Bytes, mValue = unpackInt(sumbuf[mPos:])
        mPos += Bytes
        strLen = mValue
        # print "str1 Size: " + str(mValue) + "\nRead " + str(Bytes)
        #  +" Bytes, Current pos is " + str(mPos)

        Bytes, mValue = readString(sumbuf[mPos:], strLen)
        mPos += Bytes
        # print "str1 is:" + mValue + "\nRead "+str(Bytes)
        # + " Bytes, Current pos is " + str(mPos)
        print mValue

        if mValue == '':
            break
