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
from __future__ import print_function
from .GXByteBuffer import GXByteBuffer
from .enums.Security import Security

# pylint: disable=too-many-public-methods,too-many-instance-attributes,too-many-arguments
class GXDLMSChipperingStream:
    """
    Implements GMAC.  This class is based to this doc:
    http://csrc.nist.gov/publications/nistpubs/800-38D/SP-800-38D.pdf
    """

    #  Consts.
    BLOCK_SIZE = 16
    TAG_SIZE = 0x10
    IV = [0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6]

     #schedule Vector (powers of x).
    R_CON = (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80,\
        0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,\
        0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,\
        0xc5, 0x91)

    #S box
    S_BOX = (0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,\
        0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, 0xCA, 0x82,\
        0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF,\
        0x9C, 0xA4, 0x72, 0xC0, 0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F,\
        0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,\
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12,\
        0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, 0x09, 0x83, 0x2C, 0x1A,\
        0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3,\
        0x2F, 0x84, 0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,\
        0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, 0xD0, 0xEF,\
        0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F,\
        0x50, 0x3C, 0x9F, 0xA8, 0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D,\
        0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,\
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7,\
        0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, 0x60, 0x81, 0x4F, 0xDC,\
        0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E,\
        0x0B, 0xDB, 0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,\
        0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, 0xE7, 0xC8,\
        0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA,\
        0x65, 0x7A, 0xAE, 0x08, 0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6,\
        0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,\
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35,\
        0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, 0xE1, 0xF8, 0x98, 0x11,\
        0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55,\
        0x28, 0xDF, 0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,\
        0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16)

     #Inverse sbox
    S_BOX_REVERSED = (0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5,\
        0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c,\
        0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43,\
        0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32, 0xa6,\
        0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3,\
        0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76,\
        0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6,\
        0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,\
        0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9,\
        0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90,\
        0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58,\
        0x05, 0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca,\
        0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a,\
        0x6b, 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97,\
        0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, 0x96, 0xac, 0x74,\
        0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c,\
        0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5,\
        0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc,\
        0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,\
        0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88,\
        0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec,\
        0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d,\
        0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b,\
        0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83,\
        0x53, 0x99, 0x61, 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6,\
        0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d)

     #Rijndael (AES) Encryption fast table.
    AES = (0xa56363c6, 0x847c7cf8, 0x997777ee,\
        0x8d7b7bf6, 0x0df2f2ff, 0xbd6b6bd6, 0xb16f6fde, 0x54c5c591,\
        0x50303060, 0x03010102, 0xa96767ce, 0x7d2b2b56, 0x19fefee7,\
        0x62d7d7b5, 0xe6abab4d, 0x9a7676ec, 0x45caca8f, 0x9d82821f,\
        0x40c9c989, 0x877d7dfa, 0x15fafaef, 0xeb5959b2, 0xc947478e,\
        0x0bf0f0fb, 0xecadad41, 0x67d4d4b3, 0xfda2a25f, 0xeaafaf45,\
        0xbf9c9c23, 0xf7a4a453, 0x967272e4, 0x5bc0c09b, 0xc2b7b775,\
        0x1cfdfde1, 0xae93933d, 0x6a26264c, 0x5a36366c, 0x413f3f7e,\
        0x02f7f7f5, 0x4fcccc83, 0x5c343468, 0xf4a5a551, 0x34e5e5d1,\
        0x08f1f1f9, 0x937171e2, 0x73d8d8ab, 0x53313162, 0x3f15152a,\
        0x0c040408, 0x52c7c795, 0x65232346, 0x5ec3c39d, 0x28181830,\
        0xa1969637, 0x0f05050a, 0xb59a9a2f, 0x0907070e, 0x36121224,\
        0x9b80801b, 0x3de2e2df, 0x26ebebcd, 0x6927274e, 0xcdb2b27f,\
        0x9f7575ea, 0x1b090912, 0x9e83831d, 0x742c2c58, 0x2e1a1a34,\
        0x2d1b1b36, 0xb26e6edc, 0xee5a5ab4, 0xfba0a05b, 0xf65252a4,\
        0x4d3b3b76, 0x61d6d6b7, 0xceb3b37d, 0x7b292952, 0x3ee3e3dd,\
        0x712f2f5e, 0x97848413, 0xf55353a6, 0x68d1d1b9, 0x00000000,\
        0x2cededc1, 0x60202040, 0x1ffcfce3, 0xc8b1b179, 0xed5b5bb6,\
        0xbe6a6ad4, 0x46cbcb8d, 0xd9bebe67, 0x4b393972, 0xde4a4a94,\
        0xd44c4c98, 0xe85858b0, 0x4acfcf85, 0x6bd0d0bb, 0x2aefefc5,\
        0xe5aaaa4f, 0x16fbfbed, 0xc5434386, 0xd74d4d9a, 0x55333366,\
        0x94858511, 0xcf45458a, 0x10f9f9e9, 0x06020204, 0x817f7ffe,\
        0xf05050a0, 0x443c3c78, 0xba9f9f25, 0xe3a8a84b, 0xf35151a2,\
        0xfea3a35d, 0xc0404080, 0x8a8f8f05, 0xad92923f, 0xbc9d9d21,\
        0x48383870, 0x04f5f5f1, 0xdfbcbc63, 0xc1b6b677, 0x75dadaaf,\
        0x63212142, 0x30101020, 0x1affffe5, 0x0ef3f3fd, 0x6dd2d2bf,\
        0x4ccdcd81, 0x140c0c18, 0x35131326, 0x2fececc3, 0xe15f5fbe,\
        0xa2979735, 0xcc444488, 0x3917172e, 0x57c4c493, 0xf2a7a755,\
        0x827e7efc, 0x473d3d7a, 0xac6464c8, 0xe75d5dba, 0x2b191932,\
        0x957373e6, 0xa06060c0, 0x98818119, 0xd14f4f9e, 0x7fdcdca3,\
        0x66222244, 0x7e2a2a54, 0xab90903b, 0x8388880b, 0xca46468c,\
        0x29eeeec7, 0xd3b8b86b, 0x3c141428, 0x79dedea7, 0xe25e5ebc,\
        0x1d0b0b16, 0x76dbdbad, 0x3be0e0db, 0x56323264, 0x4e3a3a74,\
        0x1e0a0a14, 0xdb494992, 0x0a06060c, 0x6c242448, 0xe45c5cb8,\
        0x5dc2c29f, 0x6ed3d3bd, 0xefacac43, 0xa66262c4, 0xa8919139,\
        0xa4959531, 0x37e4e4d3, 0x8b7979f2, 0x32e7e7d5, 0x43c8c88b,\
        0x5937376e, 0xb76d6dda, 0x8c8d8d01, 0x64d5d5b1, 0xd24e4e9c,\
        0xe0a9a949, 0xb46c6cd8, 0xfa5656ac, 0x07f4f4f3, 0x25eaeacf,\
        0xaf6565ca, 0x8e7a7af4, 0xe9aeae47, 0x18080810, 0xd5baba6f,\
        0x887878f0, 0x6f25254a, 0x722e2e5c, 0x241c1c38, 0xf1a6a657,\
        0xc7b4b473, 0x51c6c697, 0x23e8e8cb, 0x7cdddda1, 0x9c7474e8,\
        0x211f1f3e, 0xdd4b4b96, 0xdcbdbd61, 0x868b8b0d, 0x858a8a0f,\
        0x907070e0, 0x423e3e7c, 0xc4b5b571, 0xaa6666cc, 0xd8484890,\
        0x05030306, 0x01f6f6f7, 0x120e0e1c, 0xa36161c2, 0x5f35356a,\
        0xf95757ae, 0xd0b9b969, 0x91868617, 0x58c1c199, 0x271d1d3a,\
        0xb99e9e27, 0x38e1e1d9, 0x13f8f8eb, 0xb398982b, 0x33111122,\
        0xbb6969d2, 0x70d9d9a9, 0x898e8e07, 0xa7949433, 0xb69b9b2d,\
        0x221e1e3c, 0x92878715, 0x20e9e9c9, 0x49cece87, 0xff5555aa,\
        0x78282850, 0x7adfdfa5, 0x8f8c8c03, 0xf8a1a159, 0x80898909,\
        0x170d0d1a, 0xdabfbf65, 0x31e6e6d7, 0xc6424284, 0xb86868d0,\
        0xc3414182, 0xb0999929, 0x772d2d5a, 0x110f0f1e, 0xcbb0b07b,\
        0xfc5454a8, 0xd6bbbb6d, 0x3a16162c)

    AES1_REVERSED = (0x50a7f451, 0x5365417e,\
    0xc3a4171a, 0x965e273a, 0xcb6bab3b, 0xf1459d1f, 0xab58faac,\
    0x9303e34b, 0x55fa3020, 0xf66d76ad, 0x9176cc88, 0x254c02f5,\
    0xfcd7e54f, 0xd7cb2ac5, 0x80443526, 0x8fa362b5, 0x495ab1de,\
    0x671bba25, 0x980eea45, 0xe1c0fe5d, 0x02752fc3, 0x12f04c81,\
    0xa397468d, 0xc6f9d36b, 0xe75f8f03, 0x959c9215, 0xeb7a6dbf,\
    0xda595295, 0x2d83bed4, 0xd3217458, 0x2969e049, 0x44c8c98e,\
    0x6a89c275, 0x78798ef4, 0x6b3e5899, 0xdd71b927, 0xb64fe1be,\
    0x17ad88f0, 0x66ac20c9, 0xb43ace7d, 0x184adf63, 0x82311ae5,\
    0x60335197, 0x457f5362, 0xe07764b1, 0x84ae6bbb, 0x1ca081fe,\
    0x942b08f9, 0x58684870, 0x19fd458f, 0x876cde94, 0xb7f87b52,\
    0x23d373ab, 0xe2024b72, 0x578f1fe3, 0x2aab5566, 0x0728ebb2,\
    0x03c2b52f, 0x9a7bc586, 0xa50837d3, 0xf2872830, 0xb2a5bf23,\
    0xba6a0302, 0x5c8216ed, 0x2b1ccf8a, 0x92b479a7, 0xf0f207f3,\
    0xa1e2694e, 0xcdf4da65, 0xd5be0506, 0x1f6234d1, 0x8afea6c4,\
    0x9d532e34, 0xa055f3a2, 0x32e18a05, 0x75ebf6a4, 0x39ec830b,\
    0xaaef6040, 0x069f715e, 0x51106ebd, 0xf98a213e, 0x3d06dd96,\
    0xae053edd, 0x46bde64d, 0xb58d5491, 0x055dc471, 0x6fd40604,\
    0xff155060, 0x24fb9819, 0x97e9bdd6, 0xcc434089, 0x779ed967,\
    0xbd42e8b0, 0x888b8907, 0x385b19e7, 0xdbeec879, 0x470a7ca1,\
    0xe90f427c, 0xc91e84f8, 0x00000000, 0x83868009, 0x48ed2b32,\
    0xac70111e, 0x4e725a6c, 0xfbff0efd, 0x5638850f, 0x1ed5ae3d,\
    0x27392d36, 0x64d90f0a, 0x21a65c68, 0xd1545b9b, 0x3a2e3624,\
    0xb1670a0c, 0x0fe75793, 0xd296eeb4, 0x9e919b1b, 0x4fc5c080,\
    0xa220dc61, 0x694b775a, 0x161a121c, 0x0aba93e2, 0xe52aa0c0,\
    0x43e0223c, 0x1d171b12, 0x0b0d090e, 0xadc78bf2, 0xb9a8b62d,\
    0xc8a91e14, 0x8519f157, 0x4c0775af, 0xbbdd99ee, 0xfd607fa3,\
    0x9f2601f7, 0xbcf5725c, 0xc53b6644, 0x347efb5b, 0x7629438b,\
    0xdcc623cb, 0x68fcedb6, 0x63f1e4b8, 0xcadc31d7, 0x10856342,\
    0x40229713, 0x2011c684, 0x7d244a85, 0xf83dbbd2, 0x1132f9ae,\
    0x6da129c7, 0x4b2f9e1d, 0xf330b2dc, 0xec52860d, 0xd0e3c177,\
    0x6c16b32b, 0x99b970a9, 0xfa489411, 0x2264e947, 0xc48cfca8,\
    0x1a3ff0a0, 0xd82c7d56, 0xef903322, 0xc74e4987, 0xc1d138d9,\
    0xfea2ca8c, 0x360bd498, 0xcf81f5a6, 0x28de7aa5, 0x268eb7da,\
    0xa4bfad3f, 0xe49d3a2c, 0x0d927850, 0x9bcc5f6a, 0x62467e54,\
    0xc2138df6, 0xe8b8d890, 0x5ef7392e, 0xf5afc382, 0xbe805d9f,\
    0x7c93d069, 0xa92dd56f, 0xb31225cf, 0x3b99acc8, 0xa77d1810,\
    0x6e639ce8, 0x7bbb3bdb, 0x097826cd, 0xf418596e, 0x01b79aec,\
    0xa89a4f83, 0x656e95e6, 0x7ee6ffaa, 0x08cfbc21, 0xe6e815ef,\
    0xd99be7ba, 0xce366f4a, 0xd4099fea, 0xd67cb029, 0xafb2a431,\
    0x31233f2a, 0x3094a5c6, 0xc066a235, 0x37bc4e74, 0xa6ca82fc,\
    0xb0d090e0, 0x15d8a733, 0x4a9804f1, 0xf7daec41, 0x0e50cd7f,\
    0x2ff69117, 0x8dd64d76, 0x4db0ef43, 0x544daacc, 0xdf0496e4,\
    0xe3b5d19e, 0x1b886a4c, 0xb81f2cc1, 0x7f516546, 0x04ea5e9d,\
    0x5d358c01, 0x737487fa, 0x2e410bfb, 0x5a1d67b3, 0x52d2db92,\
    0x335610e9, 0x1347d66d, 0x8c61d79a, 0x7a0ca137, 0x8e14f859,\
    0x893c13eb, 0xee27a9ce, 0x35c961b7, 0xede51ce1, 0x3cb1477a,\
    0x59dfd29c, 0x3f73f255, 0x79ce1418, 0xbf37c773, 0xeacdf753,\
    0x5baafd5f, 0x146f3ddf, 0x86db4478, 0x81f3afca, 0x3ec468b9,\
    0x2c342438, 0x5f40a3c2, 0x72c31d16, 0x0c25e2bc, 0x8b493c28,\
    0x41950dff, 0x7101a839, 0xdeb30c08, 0x9ce4b4d8, 0x90c15664,\
    0x6184cb7b, 0x70b632d5, 0x745c6c48, 0x4257b8d0)

    blockSize = 16

    #
    #      * Constructor.
    #      *
    #      * @param forSecurity
    #      * Used security level.
    #      * @param forEncrypt
    #      * @param blockCipherKey
    #      * @param forAad
    #      * @param iv
    #      * @param forTag
    #
    def __init__(self, forSecurity, forEncrypt, blockCipherKey, forAad, iv, forTag):
        self.security = forSecurity
        self.tag = forTag
        if not self.tag:
            #  Tag size is 12 bytes.
            self.tag = bytearray(12)
        elif len(self.tag) != 12:
            raise ValueError("Invalid tag.")
        self.encrypt = forEncrypt
        self.workingKey = self.generateKey(forEncrypt, blockCipherKey)
        if self.encrypt:
            bufLength = GXDLMSChipperingStream.BLOCK_SIZE
        else:
            bufLength = (GXDLMSChipperingStream.BLOCK_SIZE + GXDLMSChipperingStream.TAG_SIZE)
        self.bufBlock = bytearray(bufLength)
        self.aad = forAad
        self.h = bytearray(GXDLMSChipperingStream.BLOCK_SIZE)
        if iv:
            self.processBlock(self.h, 0, self.h, 0)
            self.mArray = [[None] * 32] * 32
            self.init(self.h)
            self.j0 = bytearray(16)
            self.j0[0:len(iv)] = iv[0:]
            self.j0[15] = 0x01
        if self.aad:
            self.s = self.getGHash(self.aad)
        if iv:
            self.counter = self.clone(self.j0)
        self.bytesRemaining = 0
        self.totalLength = 0
        self.output = GXByteBuffer()
        self.c0 = self.c1 = self.c2 = self.c3 = 0
        self.blockSize = 16

    @classmethod
    def clone(cls, value):
        """
        Clone byte array.
        """
        tmp = value[0:]
        return tmp

    #
    #      * Convert byte array to Little Endian.
    #      *
    #      * @param data
    #      * @param offset
    #      * @return
    #
    @classmethod
    def toUInt32(cls, value, offset):
        tmp = value[offset] & 0xFF
        tmp |= (value[offset + 1] << 8) & 0xFF00
        tmp |= (value[offset + 2] << 16) & 0xFF0000
        tmp |= (value[offset + 3] << 24) & 0xFF000000
        return tmp

    @classmethod
    def subWord(cls, value):
        tmp = cls.S_BOX[value & 0xFF] & 0xFF
        tmp |= (((cls.S_BOX[(value >> 8) & 0xFF]) & 0xFF) << 8) & 0xFF00
        tmp |= (((cls.S_BOX[(value >> 16) & 0xFF]) & 0xFF) << 16) & 0xFF0000
        tmp |= (((cls.S_BOX[(value >> 24) & 0xFF]) & 0xFF) << 24) & 0xFF000000
        return tmp

    @classmethod
    def shift(cls, value, shift):
        """
        Shift value.
        """
        return (value >> shift) | (value << (32 - shift)) & 0xFFFFFFFF

    #
    #      * Initialise the key schedule from the user supplied key.
    #      *
    #      * @return
    #
    @classmethod
    def starX(cls, value):
        m1 = 0x80808080
        m2 = 0x7f7f7f7f
        m3 = 0x0000001b
        return ((value & m2) << 1) ^ (((value & m1) >> 7) * m3)

    def imixCol(self, x):
        f2 = self.starX(x)
        f4 = self.starX(f2)
        f8 = self.starX(f4)
        f9 = x ^ f8
        return f2 ^ f4 ^ f8 ^ self.shift(f2 ^ f9, 8) ^ self.shift(f4 ^ f9, 16) ^ self.shift(f9, 24)

    #
    #      * Get bytes from UIn32.
    #      *
    #      * @param value
    #      * @param data
    #      * @param offset
    #
    @classmethod
    def getUInt32(cls, value, data, offset):
        data[offset] = value & 0xFF
        data[offset + 1] = (value >> 8) & 0xFF
        data[offset + 2] = (value >> 16) & 0xFF
        data[offset + 3] = (value >> 24) & 0xFF

    def unPackBlock(self, bytes_, offset):
        self.c0 = self.toUInt32(bytes_, offset)
        self.c1 = self.toUInt32(bytes_, offset + 4)
        self.c2 = self.toUInt32(bytes_, offset + 8)
        self.c3 = self.toUInt32(bytes_, offset + 12)

    def packBlock(self, bytes_, offset):
        self.getUInt32(self.c0, bytes_, offset)
        self.getUInt32(self.c1, bytes_, offset + 4)
        self.getUInt32(self.c2, bytes_, offset + 8)
        self.getUInt32(self.c3, bytes_, offset + 12)

    #
    #      * Encrypt data block.
    #      *
    #      * @param key
    #
    def encryptBlock(self, key):
        r = 1
        self.c0 ^= key[0][0]
        self.c1 ^= key[0][1]
        self.c2 ^= key[0][2]
        self.c3 ^= key[0][3]
        while r < self.rounds - 1:
            r0 = (self.AES[self.c0 & 0xFF] & 0xFFFFFFFF)
            r0 ^= (self.shift(self.AES[(self.c1 >> 8) & 0xFF], 24) & 0xFFFFFFFF)
            r0 ^= (self.shift(self.AES[(self.c2 >> 16) & 0xFF], 16) & 0xFFFFFFFF)
            r0 ^= (self.shift(self.AES[(self.c3 >> 24) & 0xFF], 8) & 0xFFFFFFFF)
            r0 ^= (key[r][0] & 0xFFFFFFFF)
            r1 = (self.AES[self.c1 & 0xFF] & 0xFFFFFFFF)
            r1 ^= self.shift(self.AES[(self.c2 >> 8) & 0xFF], 24) & 0xFFFFFFFF
            r1 ^= self.shift(self.AES[(self.c3 >> 16) & 0xFF], 16) & 0xFFFFFFFF
            r1 ^= self.shift(self.AES[(self.c0 >> 24) & 0xFF], 8) & 0xFFFFFFFF
            r1 ^= key[r][1] & 0xFFFFFFFF
            r2 = self.AES[self.c2 & 0xFF] & 0xFFFFFFFF
            r2 ^= self.shift(self.AES[(self.c3 >> 8) & 0xFF], 24) & 0xFFFFFFFF
            r2 ^= self.shift(self.AES[(self.c0 >> 16) & 0xFF], 16) & 0xFFFFFFFF
            r2 ^= self.shift(self.AES[(self.c1 >> 24) & 0xFF], 8) & 0xFFFFFFFF
            r2 ^= key[r][2] & 0xFFFFFFFF
            r3 = self.AES[self.c3 & 0xFF] & 0xFFFFFFFF
            r3 ^= self.shift(self.AES[(self.c0 >> 8) & 0xFF], 24) & 0xFFFFFFFF
            r3 ^= self.shift(self.AES[(self.c1 >> 16) & 0xFF], 16) & 0xFFFFFFFF
            r3 ^= self.shift(self.AES[(self.c2 >> 24) & 0xFF], 8) & 0xFFFFFFFF
            r3 ^= key[r][3] & 0xFFFFFFFF
            r = r + 1
            self.c0 = self.AES[r0 & 0xFF] & 0xFFFFFFFF
            self.c0 ^= self.shift(self.AES[(r1 >> 8) & 0xFF], 24) & 0xFFFFFFFF
            self.c0 ^= self.shift(self.AES[(r2 >> 16) & 0xFF], 16) & 0xFFFFFFFF
            self.c0 ^= self.shift(self.AES[(r3 >> 24) & 0xFF], 8) & 0xFFFFFFFF
            self.c0 ^= key[r][0] & 0xFFFFFFFF
            self.c1 = self.AES[r1 & 0xFF] & 0xFFFFFFFF
            self.c1 ^= self.shift(self.AES[(r2 >> 8) & 0xFF], 24) & 0xFFFFFFFF
            self.c1 ^= self.shift(self.AES[(r3 >> 16) & 0xFF], 16) & 0xFFFFFFFF
            self.c1 ^= self.shift(self.AES[(r0 >> 24) & 0xFF], 8) & 0xFFFFFFFF
            self.c1 ^= key[r][1] & 0xFFFFFFFF
            self.c2 = self.AES[r2 & 0xFF] & 0xFFFFFFFF
            self.c2 ^= self.shift(self.AES[(r3 >> 8) & 0xFF], 24) & 0xFFFFFFFF
            self.c2 ^= self.shift(self.AES[(r0 >> 16) & 0xFF], 16) & 0xFFFFFFFF
            self.c2 ^= self.shift(self.AES[(r1 >> 24) & 0xFF], 8) & 0xFFFFFFFF
            self.c2 ^= key[r][2] & 0xFFFFFFFF
            self.c3 = self.AES[r3 & 0xFF] & 0xFFFFFFFF
            self.c3 ^= self.shift(self.AES[(r0 >> 8) & 0xFF], 24) & 0xFFFFFFFF
            self.c3 ^= self.shift(self.AES[(r1 >> 16) & 0xFF], 16) & 0xFFFFFFFF
            self.c3 ^= self.shift(self.AES[(r2 >> 24) & 0xFF], 8) & 0xFFFFFFFF
            self.c3 ^= key[r][3] & 0xFFFFFFFF
            r = r + 1

        r0 = self.AES[self.c0 & 0xFF] & 0xFFFFFFFF
        r0 ^= self.shift(self.AES[(self.c1 >> 8) & 0xFF], 24) & 0xFFFFFFFF
        r0 ^= self.shift(self.AES[(self.c2 >> 16) & 0xFF], 16) & 0xFFFFFFFF
        r0 ^= self.shift(self.AES[self.c3 >> 24], 8) & 0xFFFFFFFF
        r0 ^= key[r][0] & 0xFFFFFFFF
        r1 = self.AES[self.c1 & 0xFF] & 0xFFFFFFFF
        r1 ^= self.shift(self.AES[(self.c2 >> 8) & 0xFF], 24) & 0xFFFFFFFF
        r1 ^= self.shift(self.AES[(self.c3 >> 16) & 0xFF], 16) & 0xFFFFFFFF
        r1 ^= self.shift(self.AES[self.c0 >> 24], 8) & 0xFFFFFFFF
        r1 ^= key[r][1] & 0xFFFFFFFF
        r2 = self.AES[self.c2 & 0xFF] & 0xFFFFFFFF
        r2 ^= self.shift(self.AES[(self.c3 >> 8) & 0xFF], 24) & 0xFFFFFFFF
        r2 ^= self.shift(self.AES[(self.c0 >> 16) & 0xFF], 16) & 0xFFFFFFFF
        r2 ^= self.shift(self.AES[self.c1 >> 24], 8) & 0xFFFFFFFF
        r2 ^= key[r][2] & 0xFFFFFFFF
        r3 = self.AES[self.c3 & 0xFF] & 0xFFFFFFFF
        r3 ^= self.shift(self.AES[(self.c0 >> 8) & 0xFF], 24) & 0xFFFFFFFF
        r3 ^= self.shift(self.AES[(self.c1 >> 16) & 0xFF], 16) & 0xFFFFFFFF
        r3 ^= self.shift(self.AES[self.c2 >> 24], 8) & 0xFFFFFFFF
        r3 ^= key[r][3] & 0xFFFFFFFF
        r += 1
        self.c0 = (self.S_BOX[r0 & 0xFF] & 0xFF) & 0xFFFFFFFF
        self.c0 ^= ((self.S_BOX[(r1 >> 8) & 0xFF] & 0xFF) << 8) & 0xFFFFFFFF
        self.c0 ^= ((self.S_BOX[(r2 >> 16) & 0xFF] & 0xFF) << 16) & 0xFFFFFFFF
        self.c0 ^= ((self.S_BOX[r3 >> 24] & 0xFF) << 24) & 0xFFFFFFFF
        self.c0 ^= key[r][0] & 0xFFFFFFFF
        self.c1 = (self.S_BOX[r1 & 0xFF] & 0xFF) & 0xFFFFFFFF
        self.c1 ^= ((self.S_BOX[(r2 >> 8) & 0xFF] & 0xFF) << 8) & 0xFFFFFFFF
        self.c1 ^= ((self.S_BOX[(r3 >> 16) & 0xFF] & 0xFF) << 16) & 0xFFFFFFFF
        self.c1 ^= ((self.S_BOX[r0 >> 24] & 0xFF) << 24) & 0xFFFFFFFF
        self.c1 ^= key[r][1] & 0xFFFFFFFF
        self.c2 = (self.S_BOX[r2 & 0xFF] & 0xFF) & 0xFFFFFFFF
        self.c2 ^= ((self.S_BOX[(r3 >> 8) & 0xFF] & 0xFF) << 8) & 0xFFFFFFFF
        self.c2 ^= ((self.S_BOX[(r0 >> 16) & 0xFF] & 0xFF) << 16) & 0xFFFFFFFF
        self.c2 ^= ((self.S_BOX[r1 >> 24] & 0xFF) << 24) & 0xFFFFFFFF
        self.c2 ^= key[r][2] & 0xFFFFFFFF
        self.c3 = (self.S_BOX[r3 & 0xFF] & 0xFF) & 0xFFFFFFFF
        self.c3 ^= ((self.S_BOX[(r0 >> 8) & 0xFF] & 0xFF) << 8) & 0xFFFFFFFF
        self.c3 ^= ((self.S_BOX[(r1 >> 16) & 0xFF] & 0xFF) << 16) & 0xFFFFFFFF
        self.c3 ^= ((self.S_BOX[r2 >> 24] & 0xFF) << 24) & 0xFFFFFFFF
        self.c3 ^= key[r][3] & 0xFFFFFFFF

    def decryptBlock(self, key):
        t0 = self.c0 ^ key[self.rounds][0]
        t1 = self.c1 ^ key[self.rounds][1]
        t2 = self.c2 ^ key[self.rounds][2]
        r0 = r1 = r2 = 0
        r3 = self.c3 ^ key[self.rounds][3]
        r = self.rounds - 1
        while r > 1:
            r0 = (self.AES1_REVERSED[t0 & 255] & 0xFFFFFFFF) ^ self.shift(self.AES1_REVERSED[(r3 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(t2 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(t1 >> 24) & 255], 8) ^ key[r][0]
            r1 = self.AES1_REVERSED[t1 & 255] ^ self.shift(self.AES1_REVERSED[(t0 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(r3 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(t2 >> 24) & 255], 8) ^ key[r][1]
            r2 = self.AES1_REVERSED[t2 & 255] ^ self.shift(self.AES1_REVERSED[(t1 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(t0 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(r3 >> 24) & 255], 8) ^ key[r][2]
            r3 = self.AES1_REVERSED[r3 & 255] ^ self.shift(self.AES1_REVERSED[(t2 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(t1 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(t0 >> 24) & 255], 8) ^ key[r][3]
            r -= 1
            t0 = self.AES1_REVERSED[r0 & 255] ^ self.shift(self.AES1_REVERSED[(r3 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(r2 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(r1 >> 24) & 255], 8) ^ key[r][0]
            t1 = self.AES1_REVERSED[r1 & 255] ^ self.shift(self.AES1_REVERSED[(r0 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(r3 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(r2 >> 24) & 255], 8) ^ key[r][1]
            t2 = self.AES1_REVERSED[r2 & 255] ^ self.shift(self.AES1_REVERSED[(r1 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(r0 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(r3 >> 24) & 255], 8) ^ key[r][2]
            r3 = self.AES1_REVERSED[r3 & 255] ^ self.shift(self.AES1_REVERSED[(r2 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(r1 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(r0 >> 24) & 255], 8) ^ key[r][3]
            r -= 1
        r = 1
        r0 = self.AES1_REVERSED[t0 & 255] ^ self.shift(self.AES1_REVERSED[(r3 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(t2 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(t1 >> 24) & 255], 8) ^ key[r][0]
        r1 = self.AES1_REVERSED[t1 & 255] ^ self.shift(self.AES1_REVERSED[(t0 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(r3 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(t2 >> 24) & 255], 8) ^ key[r][1]
        r2 = self.AES1_REVERSED[t2 & 255] ^ self.shift(self.AES1_REVERSED[(t1 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(t0 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(r3 >> 24) & 255], 8) ^ key[r][2]
        r3 = self.AES1_REVERSED[r3 & 255] ^ self.shift(self.AES1_REVERSED[(t2 >> 8) & 255], 24) ^ self.shift(self.AES1_REVERSED[(t1 >> 16) & 255], 16) ^ self.shift(self.AES1_REVERSED[(t0 >> 24) & 255], 8) ^ key[r][3]
        r = 0
        self.c0 = (self.S_BOX_REVERSED[r0 & 255] & 0xFF) ^ ((((self.S_BOX_REVERSED[(r3 >> 8) & 255]) & 0xFF) << 8)) ^ ((((self.S_BOX_REVERSED[(r2 >> 16) & 255]) & 0xFF) << 16)) ^ ((((self.S_BOX_REVERSED[(r1 >> 24) & 255]) & 0xFF) << 24)) ^ key[r][0]
        self.c1 = (self.S_BOX_REVERSED[r1 & 255] & 0xFF) ^ (((self.S_BOX_REVERSED[(r0 >> 8) & 255]) & 0xFF) << 8) ^ (((self.S_BOX_REVERSED[(r3 >> 16) & 255]) & 0xFF) << 16) ^ (((self.S_BOX_REVERSED[(r2 >> 24) & 255]) & 0xFF) << 24) ^ key[r][1]
        self.c2 = (self.S_BOX_REVERSED[r2 & 255] & 0xFF) ^ (((self.S_BOX_REVERSED[(r1 >> 8) & 255]) & 0xFF) << 8) ^ (((self.S_BOX_REVERSED[(r0 >> 16) & 255]) & 0xFF) << 16) ^ (((self.S_BOX_REVERSED[(r3 >> 24) & 255]) & 0xFF) << 24) ^ key[r][2]
        self.c3 = (self.S_BOX_REVERSED[r3 & 255] & 0xFF) ^ (((self.S_BOX_REVERSED[(r2 >> 8) & 255]) & 0xFF) << 8) ^ (((self.S_BOX_REVERSED[(r1 >> 16) & 255]) & 0xFF) << 16) ^ (((self.S_BOX_REVERSED[(r0 >> 24) & 255]) & 0xFF) << 24) ^ key[r][3]

    def processBlock(self, input_, inOffset, forOutput, outOffset):
        if inOffset + (32 / 2) > len(input_):
            raise ValueError("input buffer too short")
        if outOffset + (32 / 2) > len(forOutput):
            raise ValueError("output buffer too short")
        self.unPackBlock(input_, inOffset)
        if self.encrypt:
            self.encryptBlock(self.workingKey)
        else:
            self.decryptBlock(self.workingKey)
        self.packBlock(forOutput, outOffset)
        return self.BLOCK_SIZE

    @classmethod
    def bEToUInt32(cls, buff, offset):
        value = (buff[offset] << 24)
        value |= (buff[offset + 1] << 16) & 0xFF0000
        value |= (buff[offset + 2] << 8) & 0xFF00
        value |= buff[offset + 3] & 0xFF
        return value

    @classmethod
    def shiftRight(cls, block, count):
        bit = 0
        i = 0
        while i < 4:
            b = block[i]
            block[i] = (b >> count) | bit
            bit = (b << (32 - count)) & 0xFFFFFFFF
            i += 1

    @classmethod
    def multiplyP(cls, x):
        lsb = (x[3] & 1) != 0
        cls.shiftRight(x, 1)
        if lsb:
            x[0] ^= 0xe1000000

    @classmethod
    def getUint128(cls, buff):
        us = [None] * 4
        us[0] = cls.bEToUInt32(buff, 0)
        us[1] = cls.bEToUInt32(buff, 4)
        us[2] = cls.bEToUInt32(buff, 8)
        us[3] = cls.bEToUInt32(buff, 12)
        return us

    @classmethod
    def xor(cls, block, value):
        pos = 0
        while pos != 16:
            block[pos] ^= value[pos]
            pos += 1

    @classmethod
    def xor128(cls, block, value):
        pos = 0
        while pos != 4:
            block[pos] ^= value[pos]
            pos += 1

    @classmethod
    def multiplyP8(cls, x):
        lsw = x[3]
        cls.shiftRight(x, 8)
        pos = 0
        while pos != 8:
            if (lsw & (1 << pos)) != 0:
                x[0] ^= ((0xe1000000 >> (7 - pos)) & 0xFFFFFFFF)
            pos += 1

    def getGHash(self, b):
        y = bytearray(16)
        pos = 0
        while pos < len(b):
            x = bytearray(16)
            cnt = min(len(b) - pos, 16)
            x[0:cnt] = b[pos:pos + cnt]
            self.xor(y, x)
            self.multiplyH(y)
            pos += 16
        return y

    @classmethod
    def uInt32ToBE(cls, value, buff, offset):
        buff[offset] = (value >> 24) & 0xFF
        buff[offset + 1] = (value >> 16) & 0xFF
        buff[offset + 2] = (value >> 8) & 0xFF
        buff[offset + 3] = value & 0xFF

    def multiplyH(self, value):
        tmp = [0] * 4
        pos = 0
        while pos != 16:
            m = self.mArray[pos + pos][value[pos] & 0x0f]
            tmp[0] ^= m[0]
            tmp[1] ^= m[1]
            tmp[2] ^= m[2]
            tmp[3] ^= m[3]
            m = self.mArray[pos + pos + 1][(value[pos] & 0xf0) >> 4]
            tmp[0] ^= m[0]
            tmp[1] ^= m[1]
            tmp[2] ^= m[2]
            tmp[3] ^= m[3]
            pos += 1
        self.uInt32ToBE(tmp[0], value, 0)
        self.uInt32ToBE(tmp[1], value, 4)
        self.uInt32ToBE(tmp[2], value, 8)
        self.uInt32ToBE(tmp[3], value, 12)

    def init(self, value):
        self.mArray[0] = [0] * 16
        self.mArray[1] = [0] * 16
        self.mArray[0][0] = [0] * 4
        self.mArray[1][0] = [0] * 4
        self.mArray[1][8] = self.getUint128(value)
        tmp = []
        pos = 4
        while pos >= 1:
            tmp = self.clone(self.mArray[1][pos + pos])
            self.multiplyP(tmp)
            self.mArray[1][pos] = tmp
            pos >>= 1
        tmp = self.clone(self.mArray[1][1])
        self.multiplyP(tmp)
        self.mArray[0][8] = tmp
        pos = 4
        while pos >= 1:
            tmp = self.clone(self.mArray[0][pos + pos])
            self.multiplyP(tmp)
            self.mArray[0][pos] = tmp
            pos >>= 1
        pos1 = 0
        while True:
            pos2 = 2
            while pos2 < 16:
                k = 1
                while k < pos2:
                    tmp = self.clone(self.mArray[pos1][pos2])
                    self.xor128(tmp, self.mArray[pos1][k])
                    self.mArray[pos1][pos2 + k] = tmp
                    k += 1
                pos2 += pos2
            pos1 += 1
            if pos1 == 32:
                return
            if pos1 > 1:
                self.mArray[pos1] = [0] * 16
                self.mArray[pos1][0] = [0] * 4
                pos = 8
                while pos > 0:
                    tmp = self.clone(self.mArray[pos1 - 2][pos])
                    self.multiplyP8(tmp)
                    self.mArray[pos1][pos] = tmp
                    pos >>= 1


    def gCTRBlock(self, buf, bufCount):
        i = 15
        while i >= 12:
            self.counter[i] += 1
            if self.counter[i] != 0:
                break
            i -= 1
        tmp = bytearray(self.BLOCK_SIZE)
        self.processBlock(self.counter, 0, tmp, 0)
        if self.encrypt:
            zeroes = bytearray(self.BLOCK_SIZE)
            tmp[bufCount:self.BLOCK_SIZE] = zeroes[bufCount:self.BLOCK_SIZE]
            hashBytes = tmp
        else:
            hashBytes = buf
        pos = 0
        while pos != bufCount:
            tmp[pos] ^= buf[pos]
            self.output.setUInt8(tmp[pos])
            pos += 1
        self.xor(self.s, hashBytes)
        self.multiplyH(self.s)
        self.totalLength += bufCount

    @classmethod
    def setPackLength(cls, length, buff, offset):
        cls.uInt32ToBE(int((length >> 32)), buff, offset)
        cls.uInt32ToBE(int(length), buff, offset + 4)

    def reset(self):
        self.s = self.getGHash(self.aad)
        self.counter = self.clone(self.j0)
        self.bytesRemaining = 0
        self.totalLength = 0

    @classmethod
    def tagsEquals(cls, tag1, tag2):
        pos = 0
        while pos != 12:
            if tag1[pos] != tag2[pos]:
                return False
            pos += 1
        return True

    def write(self, input_):
        for it in input_:
            self.bufBlock[self.bytesRemaining] = it
            self.bytesRemaining += 1
            if self.bytesRemaining == self.BLOCK_SIZE:
                self.gCTRBlock(self.bufBlock, self.BLOCK_SIZE)
                if not self.encrypt:
                    #System.arraycopy(self.bufBlock, self.BLOCK_SIZE,
                    #self.bufBlock, 0,)
                    self.bufBlock[0:len(self.tag)] = self.bufBlock[self.blockSize:self.blockSize + len(self.tag)]
                self.bytesRemaining = 0

    def flushFinalBlock(self):
        if self.bytesRemaining > 0:
            tmp = self.bufBlock[0:self.bytesRemaining]
            self.gCTRBlock(tmp, self.bytesRemaining)
        if self.security == Security.ENCRYPTION:
            self.reset()
            return self.output.array()
        x = bytearray(16)
        self.setPackLength(8 * len(self.aad), x, 0)
        self.setPackLength(self.totalLength * 8, x, 8)
        self.xor(self.s, x)
        self.multiplyH(self.s)
        generatedTag = bytearray(self.BLOCK_SIZE)
        self.processBlock(self.j0, 0, generatedTag, 0)
        self.xor(generatedTag, self.s)
        if not self.encrypt:
            if not self.tagsEquals(self.tag, generatedTag):
                print(GXByteBuffer.hex(self.tag, False) + "-" + GXByteBuffer.hex(generatedTag, False))
                raise ValueError("Decrypt failed. Invalid tag.")
        else:
            #Tag size is 12 bytes.
            self.tag = generatedTag[0:12]
        self.reset()
        return self.output.array()

    def generateKey(self, isEncrypt, key):
        #Key length in words.
        keyLen = int(len(key) / 4)
        self.rounds = keyLen + 6
        w = [[0 for x in range(4)] for y in range(self.rounds + 1)]
        t = 0
        i = 0
        while i < len(key):
            w[t >> 2][t & 3] = self.toUInt32(key, i)
            i += 4
            t += 1
        k = (self.rounds + 1) << 2
        i = keyLen
        while i < k:
            temp = w[(i - 1) >> 2][(i - 1) & 3]
            if (i % keyLen) == 0:
                temp = self.subWord(self.shift(temp, 8)) ^ (self.R_CON[int(i / keyLen) - 1] & 0xFF)
            elif (keyLen > 6) and ((i % keyLen) == 4):
                temp = self.subWord(temp)
            w[i >> 2][i & 3] = w[(i - keyLen) >> 2][(i - keyLen) & 3] ^ temp
            i += 1
        if not isEncrypt:
            j = 1
            while j < self.rounds:
                i = 0
                while i < 4:
                    w[j][i] = self.imixCol(w[j][i])
                    i += 1
                j += 1
        return w

    @classmethod
    def galoisMultiply(cls, value):
        if value >> 7 != 0:
            value = value << 1
            return (value ^ 0x1b) & 0xFF

        return (value << 1) & 0xFF
#        temp = (value >> 7) & 0xFF
#        temp = temp & 0x1b
#        return ((value << 1) ^ temp) & 0xFF

    @classmethod
    def aes1Encrypt(cls, data, offset, secret):
        round_ = 0
        i = 0
        key = secret[0:]
        while round_ < 10:
            i = 0
            while i < 16:
                data[i + offset] = cls.S_BOX[(data[i + offset] ^ key[i]) & 0xFF]
                i += 1
            buf1 = data[1 + offset]
            data[1 + offset] = data[5 + offset]
            data[5 + offset] = data[9 + offset]
            data[9 + offset] = data[13 + offset]
            data[13 + offset] = buf1
            buf1 = data[2 + offset]
            buf2 = data[6 + offset]
            data[2 + offset] = data[10 + offset]
            data[6 + offset] = data[14 + offset]
            data[10 + offset] = buf1
            data[14 + offset] = buf2
            buf1 = data[15 + offset]
            data[15 + offset] = data[11 + offset]
            data[11 + offset] = data[7 + offset]
            data[7 + offset] = data[3 + offset]
            data[3 + offset] = buf1
            if round_ < 9:
                i = 0
                while i < 4:
                    buf4 = (i << 2) & 0xFF
                    buf1 = (data[buf4 + offset] ^ data[buf4 + 1 + offset] ^ data[buf4 + 2 + offset] ^ data[buf4 + 3 + offset]) & 0xFF
                    buf2 = data[buf4 + offset] & 0xFF
                    buf3 = (data[buf4 + offset] ^ data[buf4 + 1 + offset]) & 0xFF
                    buf3 = cls.galoisMultiply(buf3) & 0xFF
                    data[buf4 + offset] = (data[buf4 + offset] ^ buf3 ^ buf1) & 0xFF
                    buf3 = (data[buf4 + 1 + offset] ^ data[buf4 + 2 + offset]) & 0xFF
                    buf3 = cls.galoisMultiply(buf3) & 0xFF
                    data[buf4 + 1 + offset] = (data[buf4 + 1 + offset] ^ buf3 ^ buf1) & 0xFF
                    buf3 = (data[buf4 + 2 + offset] ^ data[buf4 + 3 + offset]) & 0xFF
                    buf3 = cls.galoisMultiply(buf3) & 0xFF
                    data[buf4 + 2 + offset] = (data[buf4 + 2 + offset] ^ buf3 ^ buf1) & 0xFF
                    buf3 = (data[buf4 + 3 + offset] ^ buf2) & 0xFF
                    buf3 = cls.galoisMultiply(buf3) & 0xFF
                    data[buf4 + 3 + offset] = (data[buf4 + 3 + offset] ^ buf3 ^ buf1) & 0xFF
                    i += 1
            key[0] = (cls.S_BOX[key[13] & 0xFF] ^ key[0] ^ cls.R_CON[round_]) & 0xFF
            key[1] = (cls.S_BOX[key[14] & 0xFF] ^ key[1]) & 0xFF
            key[2] = (cls.S_BOX[key[15] & 0xFF] ^ key[2]) & 0xFF
            key[3] = (cls.S_BOX[key[12] & 0xFF] ^ key[3]) & 0xFF
            i = 4
            while i < 16:
                key[i] = (key[i] ^ key[i - 4]) & 0xFF
                i += 1
            round_ += 1
        i = 0
        while i < 16:
            data[i + offset] = (data[i + offset] ^ key[i])
            i += 1

    def encryptAes(self, data):
        n = len(data) / 8
        if (n * 8) != len(data):
            raise ValueError("Invalid data.")
        iv = bytearray([0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6])
        block = bytearray(len(data) + len(iv))
        buf = bytearray(8 + len(iv))
        block[0:len(self.IV)] = self.IV[0:len(self.IV)]
        block[len(self.IV):len(self.IV) + len(data)] = data[0:len(data)]
        j = 0
        while j != 6:
            i = 1
            while i <= n:
                buf[0:len(self.IV)] = block[0: len(self.IV)]
                buf[len(self.IV):8 + len(self.IV)] = block[8 * i:8 * i + 8]
                self.processBlock(buf, 0, buf, 0)
                t = int(n * j + i)
                k = 1
                while t != 0:
                    v = int(t)
                    buf[len(self.IV) - k] ^= v
                    t = int(t >> 8)
                    k += 1
                block[0:8] = buf[0:8]
                block[8 * i:8 * i + 8] = buf[8:16]
                i += 1
            j += 1
        return block

    def decryptAes(self, input_):
        n = len(input_) / 8
        if (n * 8) != len(input_):
            raise ValueError("Invalid data.")
        iv = bytearray([0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6, 0xA6])
        if len(input_) > len(iv):
            block = bytearray(len(input_) - len(iv))
        else:
            block = bytearray(len(iv))
        a = bytearray(len(iv))
        buf = bytearray(8 + len(iv))
        a[0:] = input_[0:len(iv)]
        block[0:] = input_[len(iv):len(input_)]
        n = n - 1
        if n == 0:
            n = 1
        j = 5
        while j >= 0:
            i = n
            while i >= 1:
                buf[0:len(iv)] = a[0:len(iv)]
                buf[len(iv):8 + len(iv)] = block[8 * int(i - 1):8 * int(i)]
                t = n * j + i
                k = 1
                while t != 0:
                    v = int(t)
                    buf[len(self.IV)] ^= v
                    t = int((int(t) >> 8))
                    k += 1
                self.processBlock(buf, 0, buf, 0)
                a[0:] = buf[0:8]
                block[8:16] = buf[8 * (i - 1):8*i]
                i -= 1
            j -= 1
        if a != self.IV:
            raise ValueError("Invalid data")
        return block

    @classmethod
    def aes1Decrypt(cls, data, secret):
        buf1 = 0
        buf2 = 0
        buf3 = 0
        round_ = 0
        i = 0
        buf4 = 0
        key = secret[0:]
        while round_ < 10:
            key[0] = int((cls.S_BOX[key[13] & 0xFF] ^ key[0] ^ cls.R_CON[round_]))
            key[1] = int((cls.S_BOX[key[14] & 0xFF] ^ key[1]))
            key[2] = int((cls.S_BOX[key[15] & 0xFF] ^ key[2]))
            key[3] = int((cls.S_BOX[key[12] & 0xFF] ^ key[3]))
            while i < 16:
                key[i] = int((key[i] ^ key[i - 4]))
                i += 1
            round_ += 1
        while i < 16:
            data[i] = int((data[i] ^ key[i]))
            i += 1
        while round_ < 10:
            while i > 3:
                key[i] = int((key[i] ^ key[i - 4]))
                i -= 1
            key[0] = int((cls.S_BOX[key[13] & 0xFF] ^ key[0] ^ cls.R_CON[9 - round_]))
            key[1] = int((cls.S_BOX[key[14] & 0xFF] ^ key[1]))
            key[2] = int((cls.S_BOX[key[15] & 0xFF] ^ key[2]))
            key[3] = int((cls.S_BOX[key[12] & 0xFF] ^ key[3]))
            if round_ > 0:
                while i < 4:
                    buf4 = (i << 2) & 0xFF
                    buf1 = cls.galoisMultiply(cls.galoisMultiply(data[buf4] ^ data[buf4 + 2]))
                    buf2 = cls.galoisMultiply(cls.galoisMultiply(data[buf4 + 1] ^ data[buf4 + 3]))
                    data[buf4] ^= buf1
                    data[buf4 + 1] ^= buf2
                    data[buf4 + 2] ^= buf1
                    data[buf4 + 3] ^= buf2
                    buf1 = int((data[buf4] ^ data[buf4 + 1] ^ data[buf4 + 2] ^ data[buf4 + 3]))
                    buf2 = data[buf4]
                    buf3 = int((data[buf4] ^ data[buf4 + 1]))
                    buf3 = cls.galoisMultiply(buf3)
                    data[buf4] = int((data[buf4] ^ buf3 ^ buf1))
                    buf3 = int((data[buf4 + 1] ^ data[buf4 + 2]))
                    buf3 = cls.galoisMultiply(buf3)
                    data[buf4 + 1] = int((data[buf4 + 1] ^ buf3 ^ buf1))
                    buf3 = int((data[buf4 + 2] ^ data[buf4 + 3]))
                    buf3 = cls.galoisMultiply(buf3)
                    data[buf4 + 2] = int((data[buf4 + 2] ^ buf3 ^ buf1))
                    buf3 = int((data[buf4 + 3] ^ buf2))
                    buf3 = cls.galoisMultiply(buf3)
                    data[buf4 + 3] = int((data[buf4 + 3] ^ buf3 ^ buf1))
                    i += 1
            buf1 = data[13]
            data[13] = data[9]
            data[9] = data[5]
            data[5] = data[1]
            data[1] = buf1
            buf1 = data[10]
            buf2 = data[14]
            data[10] = data[2]
            data[14] = data[6]
            data[2] = buf1
            data[6] = buf2
            buf1 = data[3]
            data[3] = data[7]
            data[7] = data[11]
            data[11] = data[15]
            data[15] = buf1
            while i < 16:
                data[i] = int((cls.S_BOX_REVERSED[data[i] & 0xFF] ^ key[i]))
                i += 1
            round_ += 1
