import struct

class Parser:
    mBuf = None
    def __init__(self, buff):
        self.mBuf = buff

    def readString(self, inbytes, size):
        result = ''.join(cur for cur in inbytes[:size])
        return size, result


    def readBytes(self, inbytes, size):
        result = 0
        for count in range(0, size):
            cur = ord(inbytes[count])
            result |= (cur & 0xff) << (count * 8)

        return size, result


    def unpackInt(self, inbytes):
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


    def unpackInt64(self, inbytes):
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

    def isSummary(self, sumbuf):
        sumType, = struct.unpack('B', sumbuf[0])
        sumCode, = struct.unpack('B', sumbuf[1])
        if sumType == 1 and sumCode == 1:
            return True
        else:
            return False


    def decodeSummary(self, sumbuf):
        mPos = 0

        Bytes, mValue = self.unpackInt(sumbuf[mPos:])
        mPos += Bytes
        print "Frame Type: " + str(mValue)

        Bytes, mValue = self.unpackInt(sumbuf[mPos:])
        mPos += Bytes
        print "Code: " + str(mValue)

        Bytes, mValue = self.unpackInt(sumbuf[mPos:])
        mPos += Bytes
        strLen = mValue
        # print "Canary Size: " + str(mValue)

        Bytes, mValue = self.readString(sumbuf[mPos:], strLen)
        mPos += Bytes
        print "Canary is:" + mValue

        Bytes, mValue = self.unpackInt64(sumbuf[mPos:])
        mPos += Bytes
        print "Timestamp is:" + str(mValue)

        Bytes, mValue = self.unpackInt64(sumbuf[mPos:])
        mPos += Bytes
        print "Uptime is:" + str(mValue)

        Bytes, mValue = self.unpackInt64(sumbuf[mPos:])
        mPos += Bytes
        print "Delta is:" + str(mValue)

        while True:
            Bytes, mValue = self.unpackInt(sumbuf[mPos:])
            mPos += Bytes
            strLen = mValue
            # print "str1 Size: " + str(mValue) + "\nRead " + str(Bytes)
            #  +" Bytes, Current pos is " + str(mPos)

            Bytes, mValue = self.readString(sumbuf[mPos:], strLen)
            mPos += Bytes
            # print "str1 is:" + mValue + "\nRead "+str(Bytes)
            # + " Bytes, Current pos is " + str(mPos)
            print mValue

            if mValue == '':
                break
