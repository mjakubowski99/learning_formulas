from enum import Enum

class DataEncodingState(Enum):
    FILL_MISSING = 'FILLING_MISSING'
    FLOAT_ENCODING = 'FLOAT_ENCODING'
    OBJECT_TAGGING = 'OBJECT_TAGGING'
    VALUE_STANDARIZATION = 'VALUE_STANDARIZATION'
    BINARY_ENCODING = 'BINARY_ENCODING'