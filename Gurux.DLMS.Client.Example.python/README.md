Simple example
=========================== 
First you need to install the client, in the Gurux.DLMS.Client.Example.python folder:

```Python
pip3 install .
```

This example works in optical output from ACE6000, execute: 

```
GuruxDlmsSample -S <serial-port> -i HdlcWithModeE -c 16 -s 17 -l 1

```

The output should be as follow:

```
gurux_dlms version: 1.0.121
gurux_net version: 1.0.17
gurux_serial version: 1.0.18
Authentication: Authentication.NONE
ClientAddress: 0x10
ServerAddress: 0x91
Standard: Standard.DLMS
Bitrate is : 9600
-------- Reading 1 0.0.42.0.0.255 Ch. 0 COSEM Logical device name
Index: 1 Value: 0.0.42.0.0.255
Index: 2 Value: ACE661MA63123090
-------- Reading 15 0.0.40.0.16.255 Ch. 0 Association  #16
Index: 1 Value: 0.0.40.0.16.255
Index: 2 Value: 0.0.42.0.0.255 Ch. 0 COSEM Logical device name, 0.0.40.0.16.255 Ch. 0 Association  #16
Index: 3 Value: 16, 1
Index: 4 Value: 2 16 756 5 8 1 1
Index: 5 Value: Conformance.ACTION|SELECTIVE_ACCESS|SET|GET|BLOCK_TRANSFER_WITH_GET_OR_READ|ATTRIBUTE_0_SUPPORTED_WITH_GET 65535 8500 6 0 00 00 00 00 00 00 00 00
Attribute6 is not readable.
Attribute7 is not readable.
Index: 8 Value: 2
DisconnectRequest
Ended. Press any key to continue.
```

If you need more information run the command with a higher privilege level:

```
GuruxDlmsSample -S <serial-port> -i HdlcWithModeE -c 3 -s 17 -l 1 -a Low -P "ABCDEFGH"
```

You can change the "-c" parameter with another client type for more verbose information. 
See the manual or contact with the instrument vendor for more information about that.
In this case, see the section "7.7 communication management" in the ACE6000 User Guide. 
