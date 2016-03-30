import struct

class Parser:
    mBuf = None
    def __init__(self, buff):
        self.mBuf = buff

    def readString(self, inbytes, size):
        result = ''.join(chr(cur) for cur in inbytes[:size])
        return size, result


    def readBytes(self, inbytes, size):
        result = 0
        for count in range(0, size):
            cur = inbytes[count]
            result |= (cur & 0xff) << (count * 8)

        return size, result


    def unpackInt(self, inbytes):
        result = 0
        count = 0
        more = True
        signBits = -1
        while more:
            cur = inbytes[count]
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
            cur = inbytes[count]
            result |= (cur & 0x7f) << (count * 7)
            signBits <<= 7
            count += 1
            if cur & 0x80 != 0x80:
                more = False;

        if (signBits >> 1) & result != 0:
            result |= signBits
        return count, result


    """
        Core:	packed32	ONLY Backtrace, Name, Block Counter, Scheduler Trace and Proc Frames;
    """
    def handleSummary(self, sumbuf):
        mPos = 0

        bytes, Code = self.unpackInt(sumbuf[mPos:])
        mPos += bytes
        print "Code: " + str(Code)

        if Code == 1:
            bytes, strLen = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            # print "Canary Size: " + str(mValue)
            bytes, mValue = self.readString(sumbuf[mPos:], strLen)
            mPos += bytes
            print "Canary is:" + mValue

            bytes, Timestamp = self.unpackInt64(sumbuf[mPos:])
            mPos += bytes
            print "Timestamp is:" + str(Timestamp)

            bytes, Uptime = self.unpackInt64(sumbuf[mPos:])
            mPos += bytes
            print "Uptime is:" + str(Uptime)

            bytes, Delta = self.unpackInt64(sumbuf[mPos:])
            mPos += bytes
            print "Delta is:" + str(Delta)

            while True:
                bytes, mValue = self.unpackInt(sumbuf[mPos:])
                mPos += bytes
                strLen = mValue
                # print "str1 Size: " + str(mValue) + "\nRead " + str(Bytes)
                #  +" Bytes, Current pos is " + str(mPos)

                bytes, mValue = self.readString(sumbuf[mPos:], strLen)
                mPos += bytes
                # print "str1 is:" + mValue + "\nRead "+str(Bytes)
                # + " Bytes, Current pos is " + str(mPos)
                print mValue

                if mValue == '':
                    break
        elif Code == 3:
            bytes, Core = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            print "Core:" + str(Core)

            bytes, cpuid = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            print "cpuid:" + str(cpuid)

            bytes, strLen = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            bytes, Name = self.readString(sumbuf[mPos:], strLen)
            mPos += bytes
            print "Name:" + Name


    def handleBacktrace(self):
        pass

    def handleName(self):
        pass

    def handleCounter(self):
        pass

    def handleBlock(self):
        pass

    def handleAnnotate(self):
        pass

    def handleScheduler(self):
        pass

    def  handleIdle(self):
        pass

    def handleExternal(self):
        pass

    def handleProc(self):
        pass

    def handleActivity(self):
        pass
