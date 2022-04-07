import sys
import socket
import time

class SDG1032XNetworkException(Exception):
    pass

class SDG1032XParameterException(Exception):
    pass

class SDG1032X:
    POLARITY_NORMAL = 1
    POLARITY_INVERTED = 2

    # Trigger sources can be
    #   Internal
    #   External
    #   Manual

    TRIGGERSOURCE_INTERNAL = 'INT'
    TRIGGERSOURCE_EXTERNAL = 'EXT'
    TRIGGERSOURCE_MANUAL = 'MAN'

    # Burst mode can be either gated or specifying
    # the number of cycles

    BURSTMODE_GATE = 'GATE'
    BURSTMODE_NCYC = 'NCYC'

    def __init__(self, remoteIp):
        self.remoteIp = remoteIp
        self.hSocket = None
        try:
            self.hSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            raise SDG1032XNetworkException("Failed to create socket")
        try:
            self.hSocket.connect((remoteIp, 5024))
        except socket.error:
            raise SDG1032XNetworkException("Failed to connect to {}".format(remoteIp))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.hSocket != None:
            self.hSocket.close()
            self.hSocket = None

    def close(self):
        if self.hSocket != None:
            self.hSocket.close()
            self.hSocket = None

    def internal_socketSend(self, command):
        if self.hSocket == None:
            raise SDG1032XNetworkException("Closed device cannot send data")
        try:
            self.hSocket.sendall(command)
            self.hSocket.sendall(b'\n')
            time.sleep(1)
        except socket.error:
            self.hSocket.close()
            time.sleep(1)
            raise SDG1032XNetworkException("Failed to transmit command {}".format(command))
        reply = self.hSocket.recv(4096)
        return reply

    def factoryDefaults(self):
        ret = self.internal_socketSend(b'*RST')
        return ret

    def identify(self):
        ret = self.internal_socketSend(b'*IDN')
        return ret

    def outputEnable(self, channel=1, polarity=POLARITY_NORMAL, load="HZ"):
        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'

        command += b':OUTP ON,LOAD,'
        if load == "HZ":
            command += b'HZ,'
        else:
            command += bytes(str(load), encoding="ASCII")
            command += b','

        if polarity == self.POLARITY_NORMAL:
            command += b'PLTR,NOR'
        else:
            command += b'PLTR,INVT'

        ret = self.internal_socketSend(command)

    def outputDisable(self, channel=1):
        if channel == 1:
            self.internal_socketSend(b'C1:OUTP OFF')
        elif channel == 2:
            self.internal_socketSend(b'C2:OUTP OFF')
        else:
            pass

    def setDutyCycle(self, dutycycle, channel=1):
        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BSWV DUTY,'
        command += bytes(str(dutycycle), encoding="ASCII")

        ret = self.internal_socketSend(command)

    def setBurstModeEnable(self, channel=1):
        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BTWV STATE,ON'

        ret = self.internal_socketSend(command)
    def setBurstModeDisable(self, channel=1):
        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BTWV STATE,OFF'

        ret = self.internal_socketSend(command)

    def setBurstPeriod(self, period, channel=1):
        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BTWV PRD,'
        command += bytes(str(period), encoding="ASCII")

        ret = self.internal_socketSend(command)


    def setBurstDelay(self, delay, channel=1):
        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BTWV DLAY,'
        command += bytes(str(delay), encoding="ASCII")

        ret = self.internal_socketSend(command)

    def setBurstTriggerSource(self, triggerSource, channel=1):
        if (triggerSoruce != self.TRIGGERSOURCE_INTERNAL) and (triggerSource != self.TRIGGERSOURCE_EXTERNAL) and (triggerSource != self.TRIGGERSOURCE_MANUAL):
            raise SDG1032XParameterException("Invalid trigger source")
        if (channel != 1) and (channel != 2):
            raise SDG1032XParameterException("Invalid channel")

        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BTWV TRSR,'
        command += bytes(triggerSource, encoding="ASCII")

        ret = self.internal_socketSend(command)

    def setBurstMode(self, burstMode, channel=1):
        if (channel != 1) and (channel != 2):
            raise SDG1032XParameterException("Invalid channel")

        if (burstMode != self.BURSTMODE_GATE) and (burstMode != self.BURSTMODE_NCYC):
            raise SDG1032XParameterException("Invalid burst mode")

        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BTWV GATE_NCYC,'
        command += bytes(burstMode, encoding="ASCII")

        ret = self.internal_socketSend(command)

    def triggerBurst(self, channel=1):
        if (channel != 1) and (channel != 2):
            raise SDG1032XParameterException("Invalid channel")

        command = b''
        if channel == 1:
            command += b'C1'
        elif channel == 2:
            command += b'C2'
        command += b':BTWV MTRIG'

        ret = self.internal_socketSend(command)


if __name__ == "__main__":
    import time

    with SDG1032X("10.0.0.14") as sdg:
        print("Testing library functions ...")

        print("Identifying device")
        print(sdg.identify())

        sdg.setBurstModeEnable()

        for i in range(0,10):
            sdg.setBurstMode(sdg.BURSTMODE_GATE);
            time.sleep(1)
            sdg.setBurstMode(sdg.BURSTMODE_NCYC);
            time.sleep(1)
