See [Gurux](https://www.gurux.fi/ "Gurux") for an overview.

Join the Gurux Community or follow [@Gurux](https://twitter.com/guruxorg "@Gurux") on
Twitter for project updates.

*gurux_dlms* is a high-performance Python library that helps you read DLMS/COSEM
compatible electricity, gas, or water meters. We try to make it easy to use without the
need to understand the protocol at all.

For more info check out
[Gurux.DLMS](https://www.gurux.fi/Gurux.DLMS "Gurux.DLMS").

We are updating documentation on Gurux web page. 

Read [DLMS/COSEM FAQ](https://www.gurux.fi/DLMSCOSEMFAQ) first to get started.
Read the instructions for making your own
[meter reading application](https://www.gurux.fi/DLMSIntro) or build your own DLMS/COSEM
[meter/simulator/proxy](https://www.gurux.fi/OwnDLMSMeter).

If you have problems you can ask your questions in Gurux
[Forum](https://www.gurux.fi/forum).

Before starting with the client example, go to the *Gurux.DLMS.Client.Example.python*
directory and run

```shell
pip install -r requirements.txt
```

You can use any connection (TCP, serial, PLC) library you want.
Gurux.DLMS classes only parse the data.

Before start
=========================== 

If you find an issue, please report it here:
https://www.gurux.fi/project/issues/gurux.dlms.python


Simple example
=========================== 
First you need to install the library:

```shell
pip install gurux-common
pip install gurux-serial
pip install gurux-net
pip install gurux-dlms
```

Before use, you must set following device parameters. 
Parameters are manufacturer specific.

```Python
# First import gurux_dlms. 
from gurux_dlms import *

# All default parameters are given in constructor.
# Is Logical Name or Short Name referencing used.
client = GXDLMSClient(True)

```

HDLC addressing
=========================== 

Each meter has own server address. Server address is divided to Logical address and
Physical address. Usually you can use value 1 for meter address. You can count server
address from serial number of the meter. You can use GetServerAddress method for that.

```Python
# Count server address from serial number.
serverAddress = CGXDLMSClient.getServerAddress(serial_number)
# Count server address from logical and physical address.
serverAddress = CGXDLMSClient.getServerAddress2(logical_ddress, physical_address, address_size_in_bytes)
```

If you are using IEC handshake you must first send identify command and move to mode E.

```Python
# Support for serial port is added later.
```

After you have set the parameters, you can try to connect to the meter.
First you should send an *SNRM* request and handle the *UA* response.
After that you will send an *AARQ* request and handle the *AARE* response.


```Python
reply = GXReplyData()
data = self.client.snrmRequest()
if data:
    self.readDLMSPacket(data, reply)
    self.client.parseUAResponse(reply.data)
    size = self.client.limits.maxInfoTX + 40
    self.replyBuff = bytearray(size)
reply.clear()
self.readDataBlock(self.client.aarqRequest(), reply)
self.client.parseAareResponse(reply.data)
reply.clear()
if self.client.authentication.value > Authentication.LOW.value:
    for it in self.client.getApplicationAssociationRequest():
        self.readDLMSPacket(it, reply)
    self.client.parseApplicationAssociationResponse(reply.data)
```

If the parameters are correct, a connection is established.
Next you can read Association view and show all objects that meter can offer.

```Python
# Read Association View from the meter.
reply = GXReplyData()
self.readDataBlock(self.client.getObjectsRequest(), reply)
objects = self.client.parseObjects(reply.data, True)
converter = GXDLMSConverter.GXDLMSConverter()
converter.updateOBISCodeInformation(objects)
```

Now you can read the desired objects. After reading is done, you must close the
connection by sending a disconnect request.

```Python
self.readDLMSPacket(self.client.disconnectRequest(), reply)
# Close media.
```

```Python
def readDLMSPacket2(self, data, reply):
    if not data:
        return
    notify = GXReplyData()
    reply.error = 0
    succeeded = False
    rd = GXByteBuffer()
    if not reply.isStreaming():
        self.writeTrace("TX: " + self.now() + "\t" + GXByteBuffer.hex(data), TraceLevel.VERBOSE)
        self.media.sendall(data)
    msgPos = 0
    count = 100
    pos = 0
    try:
        while not self.client.getData(rd, reply, notify):
            if notify.data.size != 0:
                if not notify.isMoreData():
                    t = GXDLMSTranslator(TranslatorOutputType.SIMPLE_XML)
                    xml = t.dataToXml(notify.data)
                    print(xml)
                    notify.clear()
                    msgPos = rd.position
                continue
            rd.position = msgPos
            rd.set(self.media.recv(100))
        if pos == 3:
            raise ValueError("Failed to receive reply from the device in given time.")
        if pos != 0:
            print("Data send failed.  Try to resend " + str(pos) + "/3")
        pos += 1
    except Exception as e:
        self.writeTrace("RX: " + self.now() + "\t" + rd.__str__(), TraceLevel.ERROR)
        raise e
    self.writeTrace("RX: " + self.now() + "\t" + rd.__str__(), TraceLevel.VERBOSE)
    if reply.error != 0:
        raise GXDLMSException(reply.error)
```
