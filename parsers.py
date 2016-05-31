class Parsers(object):
    mBuf = None

    def __init__(self, buff):
        self.mDisplayData = buff

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
                more = False

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
        print 'Code: ' + str(Code)

        if Code == 1:
            bytes, strLen = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            # print 'Canary Size: ' + str(mValue)
            bytes, mValue = self.readString(sumbuf[mPos:], strLen)
            mPos += bytes
            print 'Canary is:' + mValue

            bytes, Timestamp = self.unpackInt64(sumbuf[mPos:])
            mPos += bytes
            print 'Timestamp is:' + str(Timestamp)

            bytes, Uptime = self.unpackInt64(sumbuf[mPos:])
            mPos += bytes
            print 'Uptime is:' + str(Uptime)

            bytes, Delta = self.unpackInt64(sumbuf[mPos:])
            mPos += bytes
            print 'Delta is:' + str(Delta)

            while True:
                bytes, mValue = self.unpackInt(sumbuf[mPos:])
                mPos += bytes
                strLen = mValue
                # print 'str1 Size: ' + str(mValue) + '\nRead ' + str(Bytes)
                #  +' Bytes, Current pos is ' + str(mPos)

                bytes, mValue = self.readString(sumbuf[mPos:], strLen)
                mPos += bytes
                # print 'str1 is:' + mValue + '\nRead '+str(Bytes)
                # + ' Bytes, Current pos is ' + str(mPos)
                print mValue

                if mValue == '':
                    break
        elif Code == 3:
            bytes, Core = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            print 'Core:' + str(Core)

            bytes, cpuid = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            print 'cpuid:' + str(cpuid)

            bytes, strLen = self.unpackInt(sumbuf[mPos:])
            mPos += bytes
            bytes, Name = self.readString(sumbuf[mPos:], strLen)
            mPos += bytes
            print 'Name:' + Name

    def handleBacktrace(self):
        pass

    def handleName(self):
        pass

    def handleCounter(self, inbuf, size):
        """
            Timestamp:
            Core:	packed32	Core to which this counter applies
            Key:	packed32	Key in Captured XML
            Value:	packed64	Value of the specified counter
        """
        # print repr(inbuf)
        mPos = 0
        while mPos < size:
            # mInfo = ''
            bytes, Timestamp = self.unpackInt64(inbuf[mPos:])
            mPos += bytes
            # mInfo += 'Timestamp:' + str(Timestamp)

            bytes, Core = self.unpackInt64(inbuf[mPos:])
            mPos += bytes
            # mInfo += '  Core: ' + str(Core)

            bytes, Key = self.unpackInt64(inbuf[mPos:])
            mPos += bytes
            # mInfo += '  Key: ' + str(Key)

            bytes, Value = self.unpackInt64(inbuf[mPos:])
            mPos += bytes
            # mInfo += '  Value: ' + str(Value)
            # print mInfo

            # if Key == self.mDisplayData.cpufreq_key:  # cpufreq
            if Key == self.mDisplayData.cpufreq_key:
                self.mDisplayData.cpufreq_lock.acquire()

                ins_index = len(self.mDisplayData.cpufreq[Core * 2 + 1]) - 1
                if ins_index < 0:
                    self.mDisplayData.cpufreq[Core * 2].append(Value / 1000000)
                    self.mDisplayData.cpufreq[Core * 2 + 1].append(Timestamp / 1000000)
                else:
                    while ins_index >= 0 and self.mDisplayData.cpufreq[Core * 2 + 1][ins_index] > Timestamp / 1000000:
                        ins_index -= 1

                    self.mDisplayData.cpufreq[Core * 2].insert(ins_index + 1, Value / 1000000)
                    self.mDisplayData.cpufreq[Core * 2 + 1].insert(ins_index + 1, Timestamp / 1000000)

                self.mDisplayData.cpufreq_lock.release()

            elif Key == self.mDisplayData.gpufreq_key:  # gpufreq
                self.mDisplayData.gpufreq_lock.acquire()

                ins_index = len(self.mDisplayData.gpufreq[1]) - 1
                if ins_index < 0:
                    self.mDisplayData.gpufreq[0].append(Value / 1000000)
                    self.mDisplayData.gpufreq[1].append(Timestamp / 1000000)
                else:
                    while ins_index >= 0 and self.mDisplayData.gpufreq[1][ins_index] > Timestamp / 1000000:
                        ins_index -= 1
                    self.mDisplayData.gpufreq[0].insert(ins_index + 1, Value / 1000000)
                    self.mDisplayData.gpufreq[1].insert(ins_index + 1, Timestamp / 1000000)

                self.mDisplayData.gpufreq_lock.release()

            elif Key == self.mDisplayData.fps_key:  # fps
                self.mDisplayData.fps_lock.acquire()
                ins_index = len(self.mDisplayData.fps[1]) - 1
                if ins_index < 0:
                    self.mDisplayData.fps[0].append(Value)
                    self.mDisplayData.fps[1].append(Timestamp / 1000000)
                else:
                    while ins_index >= 0 and self.mDisplayData.fps[1][ins_index] > Timestamp / 1000000:
                        ins_index -= 1
                    self.mDisplayData.fps[0].insert(ins_index + 1, Value)
                    self.mDisplayData.fps[1].insert(ins_index + 1, Timestamp / 1000000)
                self.mDisplayData.fps_lock.release()

            elif Key == self.mDisplayData.cpu_temp_key:  # cpu temp
                self.mDisplayData.cpu_temp_lock.acquire()
                ins_index = len(self.mDisplayData.cpu_temp[1]) - 1
                if ins_index < 0:
                    self.mDisplayData.cpu_temp[0].append(Value / 1000)
                    self.mDisplayData.cpu_temp[1].append(Timestamp / 1000000)
                else:
                    while ins_index >= 0 and self.mDisplayData.cpu_temp[1][ins_index] > Timestamp / 1000000:
                        ins_index -= 1
                    self.mDisplayData.cpu_temp[0].insert(ins_index + 1, Value / 1000)
                    self.mDisplayData.cpu_temp[1].insert(ins_index + 1, Timestamp / 1000000)
                self.mDisplayData.cpu_temp_lock.release()

            elif Key == self.mDisplayData.board_temp_key:  # board temp
                self.mDisplayData.board_temp_lock.acquire()
                ins_index = len(self.mDisplayData.board_temp[1]) - 1
                if ins_index < 0:
                    self.mDisplayData.board_temp[0].append(Value / 1000)
                    self.mDisplayData.board_temp[1].append(Timestamp / 1000000)
                else:
                    while ins_index >= 0 and self.mDisplayData.board_temp[1][ins_index] > Timestamp / 1000000:
                        ins_index -= 1
                    self.mDisplayData.board_temp[0].insert(ins_index + 1, Value / 1000)
                    self.mDisplayData.board_temp[1].insert(ins_index + 1, Timestamp / 1000000)
                self.mDisplayData.board_temp_lock.release()

            self.mDisplayData.lastts = Timestamp / 1000000

    def handleBlock(self):
        pass

    def handleAnnotate(self):
        pass

    def handleScheduler(self):
        pass

    def handleIdle(self):
        pass

    def handleExternal(self):
        pass

    def handleProc(self):
        pass

    def handleActivity(self):
        pass
