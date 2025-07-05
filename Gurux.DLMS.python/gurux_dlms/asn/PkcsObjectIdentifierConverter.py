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
from gurux_dlms.asn.enums.PkcsObjectIdentifier import PkcsObjectIdentifier


class PkcsObjectIdentifierConverter:
    @classmethod
    def getString(cls, value):
        if value == PkcsObjectIdentifier.RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.1"
        elif value == PkcsObjectIdentifier.MD2WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.2"
        elif value == PkcsObjectIdentifier.MD4WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.3"
        elif value == PkcsObjectIdentifier.MD5WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.4"
        elif value == PkcsObjectIdentifier.SHA1WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.5"
        elif value == PkcsObjectIdentifier.SRSA_OAEP_ENCRYPTION_SET:
            ret = "1.2.840.113549.1.1.6"
        elif value == PkcsObjectIdentifier.ID_RSAES_OAEP:
            ret = "1.2.840.113549.1.1.7"
        elif value == PkcsObjectIdentifier.ID_MGF1:
            ret = "1.2.840.113549.1.1.8"
        elif value == PkcsObjectIdentifier.ID_P_SPECIFIED:
            ret = "1.2.840.113549.1.1.9"
        elif value == PkcsObjectIdentifier.ID_RSASSA_PSS:
            ret = "1.2.840.113549.1.1.10"
        elif value == PkcsObjectIdentifier.SHA256WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.11"
        elif value == PkcsObjectIdentifier.SHA384WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.12"
        elif value == PkcsObjectIdentifier.SHA512WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.13"
        elif value == PkcsObjectIdentifier.SHA224WITH_RSA_ENCRYPTION:
            ret = "1.2.840.113549.1.1.14"
        elif value == PkcsObjectIdentifier.DH_KEY_AGREE1MENT:
            ret = "1.2.840.113549.1.3.1"
        elif value == PkcsObjectIdentifier.PBE_WITH_MD2AND_DES_CBC:
            ret = "1.2.840.113549.1.5.1"
        elif value == PkcsObjectIdentifier.PBE_WITH_MD2AND_RC2CBC:
            ret = "1.2.840.113549.1.5.4"
        elif value == PkcsObjectIdentifier.PBE_WITH_MD5AND_DES_CBC:
            ret = "1.2.840.113549.1.5.3"
        elif value == PkcsObjectIdentifier.PBE_WITH_MD5AND_RC2CBC:
            ret = "1.2.840.113549.1.5.6"
        elif value == PkcsObjectIdentifier.PBE_WITH_SHA1AND_DES_CBC:
            ret = "1.2.840.113549.1.5.10"
        elif value == PkcsObjectIdentifier.PBE_WITH_SHA1AND_RC2CBC:
            ret = "1.2.840.113549.1.5.11"
        elif value == PkcsObjectIdentifier.ID_PBE_S2:
            ret = "1.2.840.113549.1.5.13"
        elif value == PkcsObjectIdentifier.ID_PBKDF2:
            ret = "1.2.840.113549.1.5.12"
        elif value == PkcsObjectIdentifier.DES_EDE3CBC:
            ret = "1.2.840.113549.3.7"
        elif value == PkcsObjectIdentifier.RC2CBC:
            ret = "1.2.840.113549.3.2"
        elif value == PkcsObjectIdentifier.MD2:
            ret = "1.2.840.113549.2.2"
        elif value == PkcsObjectIdentifier.MD4:
            ret = "1.2.840.113549.2.4"
        elif value == PkcsObjectIdentifier.MD5:
            ret = "1.2.840.113549.2.5"
        elif value == PkcsObjectIdentifier.ID_HMAC_WITH_SHA1:
            ret = "1.2.840.113549.2.7"
        elif value == PkcsObjectIdentifier.ID_HMAC_WITH_SHA224:
            ret = "1.2.840.113549.2.8"
        elif value == PkcsObjectIdentifier.ID_HMAC_WITH_SHA256:
            ret = "1.2.840.113549.2.9"
        elif value == PkcsObjectIdentifier.ID_HMAC_WITH_SHA384:
            ret = "1.2.840.113549.2.10"
        elif value == PkcsObjectIdentifier.ID_HMAC_WITH_SHA512:
            ret = "1.2.840.113549.2.11"
        elif value == PkcsObjectIdentifier.DATA:
            ret = "1.2.840.113549.1.7.1"
        elif value == PkcsObjectIdentifier.SIGNED_DATA:
            ret = "1.2.840.113549.1.7.2"
        elif value == PkcsObjectIdentifier.ENVELOPED_DATA:
            ret = "1.2.840.113549.1.7.3"
        elif value == PkcsObjectIdentifier.SIGNED_AND_ENVELOPED_DATA:
            ret = "1.2.840.113549.1.7.4"
        elif value == PkcsObjectIdentifier.DIGESTED_DATA:
            ret = "1.2.840.113549.1.7.5"
        elif value == PkcsObjectIdentifier.ENCRYPTED_DATA:
            ret = "1.2.840.113549.1.7.6"
        elif value == PkcsObjectIdentifier.PKCS9AT_EMAIL_ADDRESS:
            ret = "1.2.840.113549.1.9.1"
        elif value == PkcsObjectIdentifier.PKCS9AT_UNSTRUCTURED_NAME:
            ret = "1.2.840.113549.1.9.2"
        elif value == PkcsObjectIdentifier.PKCS9AT_CONTENT_TYPE:
            ret = "1.2.840.113549.1.9.3"
        elif value == PkcsObjectIdentifier.PKCS9AT_MESSAGE_DIGEST:
            ret = "1.2.840.113549.1.9.4"
        elif value == PkcsObjectIdentifier.PKCS9AT_SIGNING_TIME:
            ret = "1.2.840.113549.1.9.5"
        elif value == PkcsObjectIdentifier.PKCS9AT_COUNTER_SIGNATURE:
            ret = "1.2.840.113549.1.9.6"
        elif value == PkcsObjectIdentifier.PKCS9AT_CHALLENGE_PASSWORD:
            ret = "1.2.840.113549.1.9.7"
        elif value == PkcsObjectIdentifier.PKCS9AT_UNSTRUCTURED_ADDRESS:
            ret = "1.2.840.113549.1.9.8"
        elif value == PkcsObjectIdentifier.PKCS9AT_EXTENDED_CERTIFICATE_ATTRIBUTES:
            ret = "1.2.840.113549.1.9.9"
        elif value == PkcsObjectIdentifier.PKCS9AT_SIGNING_DESCRIPTION:
            ret = "1.2.840.113549.1.9.13"
        elif value == PkcsObjectIdentifier.PKCS9AT_EXTENSION_REQUEST:
            ret = "1.2.840.113549.1.9.14"
        elif value == PkcsObjectIdentifier.PKCS9AT_SMIME_CAPABILITIES:
            ret = "1.2.840.113549.1.9.15"
        elif value == PkcsObjectIdentifier.ID_SMIME:
            ret = "1.2.840.113549.1.9.16"
        elif value == PkcsObjectIdentifier.PKCS9AT_FRIENDLY_NAME:
            ret = "1.2.840.113549.1.9.20"
        elif value == PkcsObjectIdentifier.PKCS9AT_LOCAL_KEY_ID:
            ret = "1.2.840.113549.1.9.21"
        elif value == PkcsObjectIdentifier.X509CERTIFICATE:
            ret = "1.2.840.113549.1.9.22.1"
        elif value == PkcsObjectIdentifier.SDSI_CERTIFICATE:
            ret = "1.2.840.113549.1.9.22.2"
        elif value == PkcsObjectIdentifier.X509CRL:
            ret = "1.2.840.113549.1.9.23.1"
        elif value == PkcsObjectIdentifier.ID_ALG:
            ret = "1.2.840.113549.1.9.16.3"
        elif value == PkcsObjectIdentifier.ID_ALG_ESDH:
            ret = "1.2.840.113549.1.9.16.3.5"
        elif value == PkcsObjectIdentifier.ID_ALG_CMS3DES_WRAP:
            ret = "1.2.840.113549.1.9.16.3.6"
        elif value == PkcsObjectIdentifier.ID_ALG_CMS_RC2WRAP:
            ret = "1.2.840.113549.1.9.16.3.7"
        elif value == PkcsObjectIdentifier.ID_ALG_PWRI_KEK:
            ret = "1.2.840.113549.1.9.16.3.9"
        elif value == PkcsObjectIdentifier.ID_ALG_SSDH:
            ret = "1.2.840.113549.1.9.16.3.10"
        elif value == PkcsObjectIdentifier.ID_RSA_KEM:
            ret = "1.2.840.113549.1.9.16.3.14"
        elif value == PkcsObjectIdentifier.PREFER_SIGNED_DATA:
            ret = "1.2.840.113549.1.9.15.1"
        elif value == PkcsObjectIdentifier.CANNOT_DECRYPT_ANY:
            ret = "1.2.840.113549.1.9.15.2"
        elif value == PkcsObjectIdentifier.SMIME_CAPABILITIES_VERSIONS:
            ret = "1.2.840.113549.1.9.15.3"
        elif value == PkcsObjectIdentifier.ID_AA_RECEIPT_REQUEST:
            ret = "1.2.840.113549.1.9.16.2.1"
        elif value == PkcsObjectIdentifier.ID_CT_AUTH_DATA:
            ret = "1.2.840.113549.1.9.16.1.2"
        elif value == PkcsObjectIdentifier.ID_CT_TST_INFO:
            ret = "1.2.840.113549.1.9.16.1.4"
        elif value == PkcsObjectIdentifier.ID_CT_COMPRESSED_DATA:
            ret = "1.2.840.113549.1.9.16.1.9"
        elif value == PkcsObjectIdentifier.ID_CT_AUTH_ENVELOPED_DATA:
            ret = "1.2.840.113549.1.9.16.1.23"
        elif value == PkcsObjectIdentifier.ID_CT_TIMESTAMPED_DATA:
            ret = "1.2.840.113549.1.9.16.1.31"
        elif value == PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_ORIGIN:
            ret = "1.2.840.113549.1.9.16.6.1"
        elif value == PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_RECEIPT:
            ret = "1.2.840.113549.1.9.16.6.2"
        elif value == PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_DELIVERY:
            ret = "1.2.840.113549.1.9.16.6.3"
        elif value == PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_SENDER:
            ret = "1.2.840.113549.1.9.16.6.4"
        elif value == PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_APPROVAL:
            ret = "1.2.840.113549.1.9.16.6.5"
        elif value == PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_CREATION:
            ret = "1.2.840.113549.1.9.16.6.6"
        elif value == PkcsObjectIdentifier.ID_AA_CONTENT_HINT:
            ret = "1.2.840.113549.1.9.16.2.4"
        elif value == PkcsObjectIdentifier.ID_AA_MSG_SIG_DIGEST:
            ret = "1.2.840.113549.1.9.16.2.5"
        elif value == PkcsObjectIdentifier.ID_AA_CONTENT_REFERENCE:
            ret = "1.2.840.113549.1.9.16.2.10"
        elif value == PkcsObjectIdentifier.ID_AA_ENCRYP_KEY_PREF:
            ret = "1.2.840.113549.1.9.16.2.11"
        elif value == PkcsObjectIdentifier.ID_AA_SIGNING_CERTIFICATE:
            ret = "1.2.840.113549.1.9.16.2.12"
        elif value == PkcsObjectIdentifier.ID_AA_SIGNING_CERTIFICATE_V2:
            ret = "1.2.840.113549.1.9.16.2.47"
        elif value == PkcsObjectIdentifier.ID_AA_CONTENT_IDENTIFIER:
            ret = "1.2.840.113549.1.9.16.2.7"
        elif value == PkcsObjectIdentifier.ID_AA_SIGNATURE_TIME_STAMP_TOKEN:
            ret = "1.2.840.113549.1.9.16.2.14"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_SIG_POLICY_ID:
            ret = "1.2.840.113549.1.9.16.2.15"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_COMMITMENT_TYPE:
            ret = "1.2.840.113549.1.9.16.2.16"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_SIGNER_LOCATION:
            ret = "1.2.840.113549.1.9.16.2.17"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_SIGNER_ATTR:
            ret = "1.2.840.113549.1.9.16.2.18"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_OTHER_SIG_CERT:
            ret = "1.2.840.113549.1.9.16.2.19"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_CONTENT_TIMESTAMP:
            ret = "1.2.840.113549.1.9.16.2.20"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_CERTIFICATE_REFS:
            ret = "1.2.840.113549.1.9.16.2.21"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_REVOCATION_REFS:
            ret = "1.2.840.113549.1.9.16.2.22"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_CERT_VALUES:
            ret = "1.2.840.113549.1.9.16.2.23"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_REVOCATION_VALUES:
            ret = "1.2.840.113549.1.9.16.2.24"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_ESC_TIME_STAMP:
            ret = "1.2.840.113549.1.9.16.2.25"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_CERT_CRL_TIMESTAMP:
            ret = "1.2.840.113549.1.9.16.2.26"
        elif value == PkcsObjectIdentifier.ID_AA_ETS_ARCHIVE_TIMESTAMP:
            ret = "1.2.840.113549.1.9.16.2.27"
        elif value == PkcsObjectIdentifier.ID_SPQ_ETS_URI:
            ret = "1.2.840.113549.1.9.16.5.1"
        elif value == PkcsObjectIdentifier.ID_SPQ_ETS_U_NOTICE:
            ret = "1.2.840.113549.1.9.16.5.2"
        elif value == PkcsObjectIdentifier.KEY_BAG:
            ret = "1.2.840.113549.1.12.10.1.1"
        elif value == PkcsObjectIdentifier.PKCS8SHROUDED_KEY_BAG:
            ret = "1.2.840.113549.1.12.10.1.2"
        elif value == PkcsObjectIdentifier.CERT_BAG:
            ret = "1.2.840.113549.1.12.10.1.3"
        elif value == PkcsObjectIdentifier.CRL_BAG:
            ret = "1.2.840.113549.1.12.10.1.4"
        elif value == PkcsObjectIdentifier.SECRET_BAG:
            ret = "1.2.840.113549.1.12.10.1.5"
        elif value == PkcsObjectIdentifier.SAFE_CONTENTS_BAG:
            ret = "1.2.840.113549.1.12.10.1.6"
        elif value == PkcsObjectIdentifier.PBE_WITH_SHA_AND128BIT_RC4:
            ret = "1.2.840.113549.1.12.1.1"
        elif value == PkcsObjectIdentifier.PBE_WITH_SHA_AND40BIT_RC4:
            ret = "1.2.840.113549.1.12.1.2"
        elif value == PkcsObjectIdentifier.PBE_WITH_SHA_AND3KEY_TRIPLE_DES_CBC:
            ret = "1.2.840.113549.1.12.1.3"
        elif value == PkcsObjectIdentifier.PBE_WITH_SHA_AND2KEY_TRIPLE_DES_CBC:
            ret = "1.2.840.113549.1.12.1.4"
        elif value == PkcsObjectIdentifier.PBE_WITH_SHA_AND128BIT_RC2CBC:
            ret = "1.2.840.113549.1.12.1.5"
        elif value == PkcsObjectIdentifier.PBEWITH_SHA_AND40BIT_RC2CBC:
            ret = "1.2.840.113549.1.12.1.6"
        else:
            ret = PkcsObjectIdentifier.NONE
        return ret

    @classmethod
    def fromString(cls, value):
        if value == "1.2.840.113549.1.1.1":
            ret = PkcsObjectIdentifier.RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.2":
            ret = PkcsObjectIdentifier.MD2WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.3":
            ret = PkcsObjectIdentifier.MD4WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.4":
            ret = PkcsObjectIdentifier.MD5WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.5":
            ret = PkcsObjectIdentifier.SHA1WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.6":
            ret = PkcsObjectIdentifier.SRSA_OAEP_ENCRYPTION_SET
        elif value == "1.2.840.113549.1.1.7":
            ret = PkcsObjectIdentifier.ID_RSAES_OAEP
        elif value == "1.2.840.113549.1.1.8":
            ret = PkcsObjectIdentifier.ID_MGF1
        elif value == "1.2.840.113549.1.1.9":
            ret = PkcsObjectIdentifier.ID_P_SPECIFIED
        elif value == "1.2.840.113549.1.1.10":
            ret = PkcsObjectIdentifier.ID_RSASSA_PSS
        elif value == "1.2.840.113549.1.1.11":
            ret = PkcsObjectIdentifier.SHA256WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.12":
            ret = PkcsObjectIdentifier.SHA384WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.13":
            ret = PkcsObjectIdentifier.SHA512WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.1.14":
            ret = PkcsObjectIdentifier.SHA224WITH_RSA_ENCRYPTION
        elif value == "1.2.840.113549.1.3.1":
            ret = PkcsObjectIdentifier.DH_KEY_AGREE1MENT
        elif value == "1.2.840.113549.1.5.1":
            ret = PkcsObjectIdentifier.PBE_WITH_MD2AND_DES_CBC
        elif value == "1.2.840.113549.1.5.4":
            ret = PkcsObjectIdentifier.PBE_WITH_MD2AND_RC2CBC
        elif value == "1.2.840.113549.1.5.3":
            ret = PkcsObjectIdentifier.PBE_WITH_MD5AND_DES_CBC
        elif value == "1.2.840.113549.1.5.6":
            ret = PkcsObjectIdentifier.PBE_WITH_MD5AND_RC2CBC
        elif value == "1.2.840.113549.1.5.10":
            ret = PkcsObjectIdentifier.PBE_WITH_SHA1AND_DES_CBC
        elif value == "1.2.840.113549.1.5.11":
            ret = PkcsObjectIdentifier.PBE_WITH_SHA1AND_RC2CBC
        elif value == "1.2.840.113549.1.5.13":
            ret = PkcsObjectIdentifier.ID_PBE_S2
        elif value == "1.2.840.113549.1.5.12":
            ret = PkcsObjectIdentifier.ID_PBKDF2
        elif value == "1.2.840.113549.3.7":
            ret = PkcsObjectIdentifier.DES_EDE3CBC
        elif value == "1.2.840.113549.3.2":
            ret = PkcsObjectIdentifier.RC2CBC
        elif value == "1.2.840.113549.2.2":
            ret = PkcsObjectIdentifier.MD2
        elif value == "1.2.840.113549.2.4":
            ret = PkcsObjectIdentifier.MD4
        elif value == "1.2.840.113549.2.5":
            ret = PkcsObjectIdentifier.MD5
        elif value == "1.2.840.113549.2.7":
            ret = PkcsObjectIdentifier.ID_HMAC_WITH_SHA1
        elif value == "1.2.840.113549.2.8":
            ret = PkcsObjectIdentifier.ID_HMAC_WITH_SHA224
        elif value == "1.2.840.113549.2.9":
            ret = PkcsObjectIdentifier.ID_HMAC_WITH_SHA256
        elif value == "1.2.840.113549.2.10":
            ret = PkcsObjectIdentifier.ID_HMAC_WITH_SHA384
        elif value == "1.2.840.113549.2.11":
            ret = PkcsObjectIdentifier.ID_HMAC_WITH_SHA512
        elif value == "1.2.840.113549.1.7.1":
            ret = PkcsObjectIdentifier.DATA
        elif value == "1.2.840.113549.1.7.2":
            ret = PkcsObjectIdentifier.SIGNED_DATA
        elif value == "1.2.840.113549.1.7.3":
            ret = PkcsObjectIdentifier.ENVELOPED_DATA
        elif value == "1.2.840.113549.1.7.4":
            ret = PkcsObjectIdentifier.SIGNED_AND_ENVELOPED_DATA
        elif value == "1.2.840.113549.1.7.5":
            ret = PkcsObjectIdentifier.DIGESTED_DATA
        elif value == "1.2.840.113549.1.7.6":
            ret = PkcsObjectIdentifier.ENCRYPTED_DATA
        elif value == "1.2.840.113549.1.9.1":
            ret = PkcsObjectIdentifier.PKCS9AT_EMAIL_ADDRESS
        elif value == "1.2.840.113549.1.9.2":
            ret = PkcsObjectIdentifier.PKCS9AT_UNSTRUCTURED_NAME
        elif value == "1.2.840.113549.1.9.3":
            ret = PkcsObjectIdentifier.PKCS9AT_CONTENT_TYPE
        elif value == "1.2.840.113549.1.9.4":
            ret = PkcsObjectIdentifier.PKCS9AT_MESSAGE_DIGEST
        elif value == "1.2.840.113549.1.9.5":
            ret = PkcsObjectIdentifier.PKCS9AT_SIGNING_TIME
        elif value == "1.2.840.113549.1.9.6":
            ret = PkcsObjectIdentifier.PKCS9AT_COUNTER_SIGNATURE
        elif value == "1.2.840.113549.1.9.7":
            ret = PkcsObjectIdentifier.PKCS9AT_CHALLENGE_PASSWORD
        elif value == "1.2.840.113549.1.9.8":
            ret = PkcsObjectIdentifier.PKCS9AT_UNSTRUCTURED_ADDRESS
        elif value == "1.2.840.113549.1.9.9":
            ret = PkcsObjectIdentifier.PKCS9AT_EXTENDED_CERTIFICATE_ATTRIBUTES
        elif value == "1.2.840.113549.1.9.13":
            ret = PkcsObjectIdentifier.PKCS9AT_SIGNING_DESCRIPTION
        elif value == "1.2.840.113549.1.9.14":
            ret = PkcsObjectIdentifier.PKCS9AT_EXTENSION_REQUEST
        elif value == "1.2.840.113549.1.9.15":
            ret = PkcsObjectIdentifier.PKCS9AT_SMIME_CAPABILITIES
        elif value == "1.2.840.113549.1.9.16":
            ret = PkcsObjectIdentifier.ID_SMIME
        elif value == "1.2.840.113549.1.9.20":
            ret = PkcsObjectIdentifier.PKCS9AT_FRIENDLY_NAME
        elif value == "1.2.840.113549.1.9.21":
            ret = PkcsObjectIdentifier.PKCS9AT_LOCAL_KEY_ID
        elif value == "1.2.840.113549.1.9.22.1":
            ret = PkcsObjectIdentifier.X509CERTIFICATE
        elif value == "1.2.840.113549.1.9.22.2":
            ret = PkcsObjectIdentifier.SDSI_CERTIFICATE
        elif value == "1.2.840.113549.1.9.23.1":
            ret = PkcsObjectIdentifier.X509CRL
        elif value == "1.2.840.113549.1.9.16.3":
            ret = PkcsObjectIdentifier.ID_ALG
        elif value == "1.2.840.113549.1.9.16.3.5":
            ret = PkcsObjectIdentifier.ID_ALG_ESDH
        elif value == "1.2.840.113549.1.9.16.3.6":
            ret = PkcsObjectIdentifier.ID_ALG_CMS3DES_WRAP
        elif value == "1.2.840.113549.1.9.16.3.7":
            ret = PkcsObjectIdentifier.ID_ALG_CMS_RC2WRAP
        elif value == "1.2.840.113549.1.9.16.3.9":
            ret = PkcsObjectIdentifier.ID_ALG_PWRI_KEK
        elif value == "1.2.840.113549.1.9.16.3.10":
            ret = PkcsObjectIdentifier.ID_ALG_SSDH
        elif value == "1.2.840.113549.1.9.16.3.14":
            ret = PkcsObjectIdentifier.ID_RSA_KEM
        elif value == "1.2.840.113549.1.9.15.1":
            ret = PkcsObjectIdentifier.PREFER_SIGNED_DATA
        elif value == "1.2.840.113549.1.9.15.2":
            ret = PkcsObjectIdentifier.CANNOT_DECRYPT_ANY
        elif value == "1.2.840.113549.1.9.15.3":
            ret = PkcsObjectIdentifier.SMIME_CAPABILITIES_VERSIONS
        elif value == "1.2.840.113549.1.9.16.2.1":
            ret = PkcsObjectIdentifier.ID_AA_RECEIPT_REQUEST
        elif value == "1.2.840.113549.1.9.16.1.2":
            ret = PkcsObjectIdentifier.ID_CT_AUTH_DATA
        elif value == "1.2.840.113549.1.9.16.1.4":
            ret = PkcsObjectIdentifier.ID_CT_TST_INFO
        elif value == "1.2.840.113549.1.9.16.1.9":
            ret = PkcsObjectIdentifier.ID_CT_COMPRESSED_DATA
        elif value == "1.2.840.113549.1.9.16.1.23":
            ret = PkcsObjectIdentifier.ID_CT_AUTH_ENVELOPED_DATA
        elif value == "1.2.840.113549.1.9.16.1.31":
            ret = PkcsObjectIdentifier.ID_CT_TIMESTAMPED_DATA
        elif value == "1.2.840.113549.1.9.16.6.1":
            ret = PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_ORIGIN
        elif value == "1.2.840.113549.1.9.16.6.2":
            ret = PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_RECEIPT
        elif value == "1.2.840.113549.1.9.16.6.3":
            ret = PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_DELIVERY
        elif value == "1.2.840.113549.1.9.16.6.4":
            ret = PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_SENDER
        elif value == "1.2.840.113549.1.9.16.6.5":
            ret = PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_APPROVAL
        elif value == "1.2.840.113549.1.9.16.6.6":
            ret = PkcsObjectIdentifier.ID_CTI_ETS_PROOF_OF_CREATION
        elif value == "1.2.840.113549.1.9.16.2.4":
            ret = PkcsObjectIdentifier.ID_AA_CONTENT_HINT
        elif value == "1.2.840.113549.1.9.16.2.5":
            ret = PkcsObjectIdentifier.ID_AA_MSG_SIG_DIGEST
        elif value == "1.2.840.113549.1.9.16.2.10":
            ret = PkcsObjectIdentifier.ID_AA_CONTENT_REFERENCE
        elif value == "1.2.840.113549.1.9.16.2.11":
            ret = PkcsObjectIdentifier.ID_AA_ENCRYP_KEY_PREF
        elif value == "1.2.840.113549.1.9.16.2.12":
            ret = PkcsObjectIdentifier.ID_AA_SIGNING_CERTIFICATE
        elif value == "1.2.840.113549.1.9.16.2.47":
            ret = PkcsObjectIdentifier.ID_AA_SIGNING_CERTIFICATE_V2
        elif value == "1.2.840.113549.1.9.16.2.7":
            ret = PkcsObjectIdentifier.ID_AA_CONTENT_IDENTIFIER
        elif value == "1.2.840.113549.1.9.16.2.14":
            ret = PkcsObjectIdentifier.ID_AA_SIGNATURE_TIME_STAMP_TOKEN
        elif value == "1.2.840.113549.1.9.16.2.15":
            ret = PkcsObjectIdentifier.ID_AA_ETS_SIG_POLICY_ID
        elif value == "1.2.840.113549.1.9.16.2.16":
            ret = PkcsObjectIdentifier.ID_AA_ETS_COMMITMENT_TYPE
        elif value == "1.2.840.113549.1.9.16.2.17":
            ret = PkcsObjectIdentifier.ID_AA_ETS_SIGNER_LOCATION
        elif value == "1.2.840.113549.1.9.16.2.18":
            ret = PkcsObjectIdentifier.ID_AA_ETS_SIGNER_ATTR
        elif value == "1.2.840.113549.1.9.16.2.19":
            ret = PkcsObjectIdentifier.ID_AA_ETS_OTHER_SIG_CERT
        elif value == "1.2.840.113549.1.9.16.2.20":
            ret = PkcsObjectIdentifier.ID_AA_ETS_CONTENT_TIMESTAMP
        elif value == "1.2.840.113549.1.9.16.2.21":
            ret = PkcsObjectIdentifier.ID_AA_ETS_CERTIFICATE_REFS
        elif value == "1.2.840.113549.1.9.16.2.22":
            ret = PkcsObjectIdentifier.ID_AA_ETS_REVOCATION_REFS
        elif value == "1.2.840.113549.1.9.16.2.23":
            ret = PkcsObjectIdentifier.ID_AA_ETS_CERT_VALUES
        elif value == "1.2.840.113549.1.9.16.2.24":
            ret = PkcsObjectIdentifier.ID_AA_ETS_REVOCATION_VALUES
        elif value == "1.2.840.113549.1.9.16.2.25":
            ret = PkcsObjectIdentifier.ID_AA_ETS_ESC_TIME_STAMP
        elif value == "1.2.840.113549.1.9.16.2.26":
            ret = PkcsObjectIdentifier.ID_AA_ETS_CERT_CRL_TIMESTAMP
        elif value == "1.2.840.113549.1.9.16.2.27":
            ret = PkcsObjectIdentifier.ID_AA_ETS_ARCHIVE_TIMESTAMP
        elif value == "1.2.840.113549.1.9.16.5.1":
            ret = PkcsObjectIdentifier.ID_SPQ_ETS_URI
        elif value == "1.2.840.113549.1.9.16.5.2":
            ret = PkcsObjectIdentifier.ID_SPQ_ETS_U_NOTICE
        elif value == "1.2.840.113549.1.12.10.1.1":
            ret = PkcsObjectIdentifier.KEY_BAG
        elif value == "1.2.840.113549.1.12.10.1.2":
            ret = PkcsObjectIdentifier.PKCS8SHROUDED_KEY_BAG
        elif value == "1.2.840.113549.1.12.10.1.3":
            ret = PkcsObjectIdentifier.CERT_BAG
        elif value == "1.2.840.113549.1.12.10.1.4":
            ret = PkcsObjectIdentifier.CRL_BAG
        elif value == "1.2.840.113549.1.12.10.1.5":
            ret = PkcsObjectIdentifier.SECRET_BAG
        elif value == "1.2.840.113549.1.12.10.1.6":
            ret = PkcsObjectIdentifier.SAFE_CONTENTS_BAG
        elif value == "1.2.840.113549.1.12.1.1":
            ret = PkcsObjectIdentifier.PBE_WITH_SHA_AND128BIT_RC4
        elif value == "1.2.840.113549.1.12.1.2":
            ret = PkcsObjectIdentifier.PBE_WITH_SHA_AND40BIT_RC4
        elif value == "1.2.840.113549.1.12.1.3":
            ret = PkcsObjectIdentifier.PBE_WITH_SHA_AND3KEY_TRIPLE_DES_CBC
        elif value == "1.2.840.113549.1.12.1.4":
            ret = PkcsObjectIdentifier.PBE_WITH_SHA_AND2KEY_TRIPLE_DES_CBC
        elif value == "1.2.840.113549.1.12.1.5":
            ret = PkcsObjectIdentifier.PBE_WITH_SHA_AND128BIT_RC2CBC
        elif value == "1.2.840.113549.1.12.1.6":
            ret = PkcsObjectIdentifier.PBEWITH_SHA_AND40BIT_RC2CBC
        else:
            ret = PkcsObjectIdentifier.NONE
        return ret
