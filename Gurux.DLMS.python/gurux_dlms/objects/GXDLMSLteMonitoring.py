#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http:#www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http:#www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from .GXDLMSObject import GXDLMSObject
from .IGXDLMSBase import IGXDLMSBase
from ..enums import ErrorCode
from ..internal._GXCommon import _GXCommon
from ..GXByteBuffer import GXByteBuffer
from ..enums import ObjectType, DataType
from ..internal._GXLocalizer import _GXLocalizer
from .GXLteNetworkParameters import GXLteNetworkParameters
from .GXLteQualityOfService import GXLteQualityOfService
from .enums.LteCoverageEnhancement import LteCoverageEnhancement


class GXDLMSLteMonitoring(GXDLMSObject, IGXDLMSBase):
    """
    Online help:
     https://www.gurux.fi/Gurux.DLMS.Objects.GXDLMSLteMonitoring
    """

    __networkParameters = None
    "Network parameters for the LTE network."

    __qualityOfService = None
    "Quality of service of the LTE network."

    def __invoke(self, settings, e):
        """
        Invokes method.

            Parameters:
                settings: DLMS settings.
                e: Invoke parameters.
        """
        e.error = ErrorCode.READ_WRITE_DENIED
        return None

    def getAttributeIndexToRead(self, all_):
        """
        Returns collection of attributes to read.

            Parameters:
                all: All items are returned even if they are read already.

            Returns:
                Collection of attributes to read.
        """
        attributes = []
        # LN is static and read only once.
        if all_ or not self.logicalName:
            attributes.append(1)
        # NetworkParameters
        if all_ or self.canRead(2):
            attributes.append(2)
        if self.__version > 0:
            # QualityOfService
            if all_ or self.canRead(3):
                attributes.append(3)
        return attributes

    def getNames(self):
        """
        Returns names of attribute indexes.

            Returns:
        """
        return (
            _GXLocalizer.gettext("Logical name"),
            _GXLocalizer.gettext("Network parameters"),
            _GXLocalizer.gettext("Quality of service"),
        )

    def getMethodNames(self):
        """
        Returns names of method indexes.
        """
        return [0]

    def getAttributeCount(self):
        """
        Returns amount of attributes.

            Returns:
                Count of attributes.
        """
        if self.__version == 0:
            return 2
        return 3

    def getMethodCount(self):
        """
        Returns amount of methods.

            Returns:
        """
        return 0

    def getValue(self, settings, e):
        """
        Returns value of given attribute.

            Parameters:
                settings: DLMS settings.
                e: Get parameters.

            Returns:
                Value of the attribute index.
        """
        buff = GXByteBuffer()
        if e.index == 1:
            ret = _GXCommon.logicalNameToBytes(self.logicalName)
        elif e.index == 2:
            buff.setUInt8(DataType.STRUCTURE)
            if self.__version == 0:
                _GXCommon.setObjectCount(5, buff)
                _GXCommon.setData(
                    settings, buff, DataType.UINT16, self.__networkParameters.t3402
                )
                _GXCommon.setData(
                    settings, buff, DataType.UINT16, self.__networkParameters.t3412
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.UINT8,
                    self.__qualityOfService.signalQuality,
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.UINT8,
                    self.__qualityOfService.signalLevel,
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.INT8,
                    self.__networkParameters.qRxlevMinCE,
                )
            else:
                _GXCommon.setObjectCount(9, buff)
                _GXCommon.setData(
                    settings, buff, DataType.UINT16, self.__networkParameters.t3402
                )
                _GXCommon.setData(
                    settings, buff, DataType.UINT16, self.__networkParameters.t3412
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.UINT32,
                    self.__networkParameters.t3412ext2,
                )
                _GXCommon.setData(
                    settings, buff, DataType.UINT16, self.__networkParameters.t3324
                )
                _GXCommon.setData(
                    settings, buff, DataType.UINT32, self.__networkParameters.teDRX
                )
                _GXCommon.setData(
                    settings, buff, DataType.UINT16, self.__networkParameters.tPTW
                )
                _GXCommon.setData(
                    settings, buff, DataType.INT8, self.__networkParameters.qRxlevMin
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.INT8,
                    self.__networkParameters.qRxlevMinCE,
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.INT8,
                    self.__networkParameters.qRxLevMinCE1,
                )
            ret = buff.array()

        elif e.index == 3:
            if self.__version == 0:
                e.error = ErrorCode.READ_WRITE_DENIED
            else:
                buff.setUInt8(DataType.STRUCTURE)
                _GXCommon.setObjectCount(4, buff)
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.INT8,
                    self.__qualityOfService.signalQuality,
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.INT8,
                    self.__qualityOfService.signalLevel,
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.INT8,
                    self.__qualityOfService.signalToNoiseRatio,
                )
                _GXCommon.setData(
                    settings,
                    buff,
                    DataType.ENUM,
                    self.__qualityOfService.coverageEnhancement,
                )
                ret = buff.array()
        else:
            e.error = ErrorCode.READ_WRITE_DENIED
        return ret

    def setValue(self, settings, e):
        """
        Set value of given attribute.

            Parameters:
                settings: DLMS settings.
                e: Set parameters.
        """
        if e.index == 1:
            self.logicalName = _GXCommon.toLogicalName(e.value)
        elif e.index == 2:
            s = e.value
            if self.__version == 0:
                self.__networkParameters.T3402 = s[0]
                self.__networkParameters.T3412 = s[1]
                self.__qualityOfService.signalQuality = s[2]
                self.__qualityOfService.signalLevel = s[3]
                self.__qualityOfService.signalToNoiseRatio = s[4]
            else:
                self.__networkParameters.t3402 = s[0]
                self.__networkParameters.t3412 = s[1]
                self.__networkParameters.t3412ext2 = s[2]
                self.__networkParameters.t3324 = s[3]
                self.__networkParameters.teDRX = s[4]
                self.__networkParameters.tPTW = s[5]
                self.__networkParameters.qRxlevMin = s[6]
                self.__networkParameters.qRxlevMinCE = s[7]
                self.__networkParameters.qRxLevMinCE1 = s[8]
        elif e.index == 3:
            if self.__version == 0:
                e.error = ErrorCode.READ_WRITE_DENIED
            else:
                s = e.value
                self.__qualityOfService.signalQuality = s[0]
                self.__qualityOfService.signalLevel = s[1]
                self.__qualityOfService.signalToNoiseRatio = s[2]
                self.__qualityOfService.coverageEnhancement = LteCoverageEnhancement(
                    s[3]
                )
        else:
            e.error = ErrorCode.READ_WRITE_DENIED

    @property
    def networkParameters(self):
        """
        Network parameters for the LTE network.
        """
        return self.__networkParameters

    @networkParameters.setter
    def networkParameters(self, value):
        self.__networkParameters = value

    @property
    def qualityOfService(self):
        """
        Quality of service of the LTE network.
        """
        return self.__qualityOfService

    def getValues(self):
        """
        Returns attributes as an array.

            Returns:
                Collection of COSEM object values.
        """
        return (self.logicalName, self.__networkParameters, self.__qualityOfService)

    def getDataType(self, index):
        """
        Returns device data type of selected attribute index.

            Parameters:
                index: Attribute index of the object.

            Returns:
                Device data type of the object.
        """
        if index == 1:
            return DataType.OCTET_STRING
        elif index in (2, 3):
            return DataType.STRUCTURE
        else:
            raise ValueError("GetDataType failed. Invalid attribute index.")

    def __init__(self, ln="0.0.25.11.0.255", sn=0):
        """
        Constructor.

            Parameters:
                ln: Logical Name of the object.
                sn: Short Name of the object.
        """
        GXDLMSObject.__init__(self, ObjectType.LTE_MONITORING, ln, sn)
        self.__version = 1
        self.__networkParameters = GXLteNetworkParameters()
        self.__qualityOfService = GXLteQualityOfService()

    def load(self, reader):
        self.__networkParameters.t3402 = reader.readElementContentAsInt("T3402")
        self.__networkParameters.t3412 = reader.readElementContentAsInt("T3412")
        self.__networkParameters.t3412ext2 = reader.readElementContentAsInt("T3412ext2")
        self.__networkParameters.t3324 = reader.readElementContentAsInt("T3324")
        self.__networkParameters.teDRX = reader.readElementContentAsInt("TeDRX")
        self.__networkParameters.tPTW = reader.readElementContentAsInt("TPTW")
        self.__networkParameters.qRxlevMin = reader.readElementContentAsInt("QRxlevMin")
        self.__networkParameters.qRxlevMinCE = reader.readElementContentAsInt(
            "QRxlevMinCE"
        )
        self.__networkParameters.qRxLevMinCE1 = reader.readElementContentAsInt(
            "QRxLevMinCE1"
        )
        self.__qualityOfService.signalQuality = reader.readElementContentAsInt(
            "SignalQuality"
        )
        self.__qualityOfService.signalLevel = reader.readElementContentAsInt(
            "SignalLevel"
        )
        self.__qualityOfService.signalToNoiseRatio = reader.readElementContentAsInt(
            "SignalToNoiseRatio"
        )
        self.__qualityOfService.coverageEnhancement = LteCoverageEnhancement(
            reader.readElementContentAsInt("CoverageEnhancement")
        )

    def save(self, writer):
        writer.writeElementString("T3402", self.__networkParameters.t3402)
        writer.writeElementString("T3412", self.__networkParameters.t3412)
        writer.writeElementString("T3412ext2", self.__networkParameters.t3412ext2)
        writer.writeElementString("T3324", self.__networkParameters.t3324)
        writer.writeElementString("TeDRX", self.__networkParameters.teDRX)
        writer.writeElementString("TPTW", self.__networkParameters.tPTW)
        writer.writeElementString("QRxlevMin", self.__networkParameters.qRxlevMin)
        writer.writeElementString("QRxlevMinCE", self.__networkParameters.qRxlevMinCE)
        writer.writeElementString("QRxLevMinCE1", self.__networkParameters.qRxLevMinCE1)
        writer.writeElementString(
            "SignalQuality", self.__qualityOfService.signalQuality
        )
        writer.writeElementString("SignalLevel", self.__qualityOfService.signalLevel)
        writer.writeElementString(
            "SignalToNoiseRatio", self.__qualityOfService.signalToNoiseRatio
        )
        writer.writeElementString(
            "CoverageEnhancement", int(self.__qualityOfService.coverageEnhancement)
        )
