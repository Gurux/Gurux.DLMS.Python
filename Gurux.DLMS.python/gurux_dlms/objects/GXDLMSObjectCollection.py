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
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import xml.etree.cElementTree as ET
from xml.dom import minidom
from .GXDLMSObject import GXDLMSObject
from ..enums import ObjectType
from .GXXmlWriter import GXXmlWriter
from .GXXmlReader import GXXmlReader
from ..GXDLMSConverter import GXDLMSConverter
from ..enums import AccessMode
from ..enums import AccessMode3
from ..enums import MethodAccessMode
from ..enums import MethodAccessMode3


class GXDLMSObjectCollection(list):
    """
    Collection of DLMS objects.
    """

    #
    # Constructor.
    #
    # forParent: Parent object.
    #
    def __init__(self, forParent=None):
        # pylint: disable=super-with-arguments
        super(GXDLMSObjectCollection, self).__init__()
        self.parent = forParent

    def append(self, item):
        if not isinstance(item, GXDLMSObject):
            raise TypeError("item is not of type GXDLMSObject")
        # pylint: disable=super-with-arguments
        super(GXDLMSObjectCollection, self).append(item)
        item.parent = self

    def extend(self, items):
        # pylint: disable=super-with-arguments
        if not isinstance(items, GXDLMSObjectCollection):
            raise TypeError("items is not of type GXDLMSObjectCollection")
        for it in items:
            super(GXDLMSObjectCollection, self).append(it)
            it.parent = self

    def getObjects(self, type_):
        if isinstance(type_, (int, ObjectType)):
            type_ = [type_]
        items = GXDLMSObjectCollection()
        for it in self:
            if it.objectType in type_:
                items.append(it)
        return items

    def findByLN(self, type_, ln):
        for it in self:
            if (
                type_ in (ObjectType.NONE, it.objectType)
                and it.logicalName.strip() == ln
            ):
                return it
        return None

    def findBySN(self, sn):
        for it in self:
            if it.shortName == sn:
                return it
        return None

    def __str__(self):
        str_ = "["
        for it in self:
            if str_:
                str_ += ", "
            str_ += it
        str_ += "]"
        return str_

    @classmethod
    def load(cls, file_):
        # pylint: disable=import-outside-toplevel
        from .._GXObjectFactory import _GXObjectFactory

        obj = None
        target = None
        type_ = None
        reader = GXXmlReader(file_, GXDLMSObjectCollection())
        reader.getNext()
        while not reader.isEOF():
            if reader.isStartElement():
                target = reader.name()
                if "Objects".lower() == target.lower():
                    reader.getNext()
                elif target.find("GXDLMS") == 0:
                    try:
                        type_ = GXDLMSConverter.valueOfObjectType(target[6:])
                    except Exception:
                        # pylint:disable=raise-missing-from
                        raise ValueError("Invalid object type: " + target + ".")
                    obj = _GXObjectFactory.createObject(type_)
                    obj.version = 0
                    reader.objects.append(obj)
                    reader.getNext()
                elif "SN".lower() == target.lower():
                    obj.shortName = reader.readElementContentAsInt("SN")
                elif "LN".lower() == target.lower():
                    obj.logicalName = reader.readElementContentAsString("LN")
                elif "Description".lower() == target.lower():
                    obj.description = reader.readElementContentAsString("Description")
                elif "Version".lower() == target.lower():
                    obj.version = reader.readElementContentAsInt("Version")
                elif "Access".lower() == target.lower():
                    pos = 0
                    tmp = reader.readElementContentAsString("Access")
                    if tmp:
                        for it in tmp:
                            pos += 1
                            obj.setAccess(pos, (AccessMode)(int(it)))
                elif "Access3".lower() == target.lower():
                    tmp = reader.readElementContentAsString("Access3")
                    if tmp:
                        pos = 0
                        while pos < len(tmp) / 4:
                            obj.setAccess3(
                                1 + pos,
                                (AccessMode3)(
                                    int(tmp[4 * pos : 4 * pos + 4], 16) & ~0x8000
                                ),
                            )
                            pos += 1
                elif "MethodAccess".lower() == target.lower():
                    pos = 0
                    tmp = reader.readElementContentAsString("MethodAccess")
                    if tmp:
                        for it in tmp:
                            pos += 1
                            obj.setMethodAccess(pos, (MethodAccessMode)(int(it)))
                elif "MethodAccess3".lower() == target.lower():
                    tmp = reader.readElementContentAsString("MethodAccess3")
                    if tmp:
                        pos = 0
                        while pos < len(tmp) / 4:
                            obj.setMethodAccess3(
                                1 + pos,
                                (MethodAccessMode3)(
                                    int(tmp[4 * pos : 4 * pos + 4], 16) & ~0x8000
                                ),
                            )
                            pos += 1
                else:
                    # pylint:disable=broad-except
                    try:
                        obj.load(reader)
                    except Exception as ex:
                        print("Failed to load object " + str(obj) + " " + str(ex))
                    obj = None
            else:
                reader.read()
        for obj in reader.objects:
            obj.postLoad(reader)
        return reader.objects

    def save(self, name, settings=None):
        from .GXDLMSAssociationLogicalName import GXDLMSAssociationLogicalName

        writer = GXXmlWriter()
        objects = ET.Element("Objects")
        lnVersion = 2
        for it in self:
            if isinstance(it, GXDLMSAssociationLogicalName):
                lnVersion = it.version
                break

        for it in self:
            node = ET.SubElement(
                objects, "GXDLMS" + GXDLMSConverter.objectTypeToString(it.objectType)
            )
            if it.shortName != 0:
                ET.SubElement(node, "SN").text = str(it.shortName)
            ET.SubElement(node, "LN").text = it.logicalName
            if it.version != 0:
                ET.SubElement(node, "Version").text = str(it.version)
            if it.description:
                ET.SubElement(node, "Description").text = it.description

            # Add access rights.
            if lnVersion < 3:
                sb = ""
                pos = 1
                while pos <= it.getAttributeCount():
                    sb += str(int(it.getAccess(pos)))
                    pos += 1
                ET.SubElement(node, "Access").text = sb
                sb = ""
                pos = 1
                while pos <= it.getMethodCount():
                    sb += str(int(it.getMethodAccess(pos)))
                    pos += 1
                ET.SubElement(node, "MethodAccess").text = sb
            else:
                sb = ""
                pos = 1
                while pos <= it.getAttributeCount():
                    # Set highest bit to save integer with two chars.
                    value = int(it.getAccess3(pos))
                    value |= 0x8000
                    sb += "%0.2X" % value
                    pos += 1
                ET.SubElement(node, "Access3").text = sb
                sb = ""
                pos = 1
                while pos <= it.getMethodCount():
                    # Set highest bit to save integer with two chars.
                    value = 0x8000 | it.getMethodAccess3(pos)
                    sb += "%0.2X" % value
                    pos += 1
                ET.SubElement(node, "MethodAccess3").text = sb

            if not settings or settings.values:
                writer.objects = []
                writer.objects.append(node)
                it.save(writer)
        str_ = minidom.parseString(
            ET.tostring(objects, encoding="utf-8", method="xml")
        ).toprettyxml(indent="  ")
        with open(name, "w") as f:
            f.write(str_)
