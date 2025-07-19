from enum import IntEnum

class ScPixel(IntEnum):
    # ETC2 / EAC
    EAC_R11 = 170
    EAC_SIGNED_R11 = 172
    EAC_RG11 = 174
    EAC_SIGNED_RG11 = 176
    ETC2_EAC_RGBA8 = 178
    ETC2_EAC_SRGBA8 = 179
    ETC2_RGB8 = 180
    ETC2_SRGB8 = 181
    ETC2_RGB8_PUNCHTHROUGH_ALPHA1 = 182
    ETC2_SRGB8_PUNCHTHROUGH_ALPHA1 = 183
    
    
    # ASTC SRGBA8
    ASTC_SRGBA8_4x4 = 186
    ASTC_SRGBA8_5x4 = 187
    ASTC_SRGBA8_5x5 = 188
    ASTC_SRGBA8_6x5 = 189
    ASTC_SRGBA8_6x6 = 190
    ASTC_SRGBA8_8x5 = 192
    ASTC_SRGBA8_8x6 = 193
    ASTC_SRGBA8_8x8 = 194
    ASTC_SRGBA8_10x5 = 195
    ASTC_SRGBA8_10x6 = 196
    ASTC_SRGBA8_10x8 = 197
    ASTC_SRGBA8_10x10 = 198
    ASTC_SRGBA8_12x10 = 199
    ASTC_SRGBA8_12x12 = 200
    
    # ASTC RGBA8
    ASTC_RGBA8_4x4 = 204
    ASTC_RGBA8_5x4 = 205
    ASTC_RGBA8_5x5 = 206
    ASTC_RGBA8_6x5 = 207
    ASTC_RGBA8_6x6 = 208
    ASTC_RGBA8_8x5 = 210
    ASTC_RGBA8_8x6 = 211
    ASTC_RGBA8_8x8 = 212
    ASTC_RGBA8_10x5 = 213
    ASTC_RGBA8_10x6 = 214
    ASTC_RGBA8_10x8 = 215
    ASTC_RGBA8_10x10 = 216
    ASTC_RGBA8_12x10 = 217
    ASTC_RGBA8_12x12 = 218
    
    # ETC1
    ETC1_RGB8 = 263
    
    @staticmethod
    def glInternalFormat(type):
        match(type):
            case ScPixel.ETC1_RGB8:
                return 0x648d
            
            case ScPixel.EAC_R11:
                return 0x9270
            case ScPixel.EAC_SIGNED_R11:
                return 0x9273
            case ScPixel.EAC_RG11:
                return 0x9272
            case ScPixel.EAC_SIGNED_RG11:
                return 0x9273
            case ScPixel.ETC2_EAC_RGBA8:
                return 0x9278
            case ScPixel.ETC2_EAC_SRGBA8:
                return 0x9279
            case ScPixel.ETC2_RGB8:
                return 0x9274
            case ScPixel.ETC2_SRGB8:
                return 0x9275
            case ScPixel.ETC2_RGB8_PUNCHTHROUGH_ALPHA1:
                return 0x9276
            case ScPixel.ETC2_SRGB8_PUNCHTHROUGH_ALPHA1:
                return 0x9277
            
            case ScPixel.ASTC_SRGBA8_4x4:
                return 0x93D0
            case ScPixel.ASTC_SRGBA8_5x4:
                return 0x93D1
            case ScPixel.ASTC_SRGBA8_5x5:
                return 0x93D2
            case ScPixel.ASTC_SRGBA8_6x5:
                return 0x93D3
            case ScPixel.ASTC_SRGBA8_6x6:
                return 0x93D4
            case ScPixel.ASTC_SRGBA8_8x5:
                return 0x93D5
            case ScPixel.ASTC_SRGBA8_8x6:
                return 0x93D6
            case ScPixel.ASTC_SRGBA8_8x8:
                return 0x93D7
            case ScPixel.ASTC_SRGBA8_10x5:
                return 0x93D8
            case ScPixel.ASTC_SRGBA8_10x6:
                return 0x93D9
            case ScPixel.ASTC_RGBA8_10x8:
                return 0x93DA
            case ScPixel.ASTC_RGBA8_10x10:
                return 0x93DB
            case ScPixel.ASTC_RGBA8_12x10:
                return 0x93DC
            case ScPixel.ASTC_RGBA8_12x12:
                return 0x93DD
            
            case ScPixel.ASTC_RGBA8_4x4:
                return 0x93B0
            case ScPixel.ASTC_RGBA8_5x4:
                return 0x93B1
            case ScPixel.ASTC_RGBA8_5x5:
                return 0x93B2
            case ScPixel.ASTC_RGBA8_6x5:
                return 0x93B3
            case ScPixel.ASTC_RGBA8_6x6:
                return 0x93B4
            case ScPixel.ASTC_RGBA8_8x5:
                return 0x93B5
            case ScPixel.ASTC_RGBA8_8x6:
                return 0x93B6
            case ScPixel.ASTC_RGBA8_8x8:
                return 0x93B7
            case ScPixel.ASTC_RGBA8_10x5:
                return 0x93B8
            case ScPixel.ASTC_RGBA8_10x6:
                return 0x93B9
            case ScPixel.ASTC_RGBA8_10x8:
                return 0x93BA
            case ScPixel.ASTC_RGBA8_10x10:
                return 0x93BB
            case ScPixel.ASTC_RGBA8_12x10:
                return 0x93BC
            case ScPixel.ASTC_RGBA8_12x12:
                return 0x93BD
            case _:
                return 0xFFFF