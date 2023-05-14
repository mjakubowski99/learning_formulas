from enums.DataEncodingState import DataEncodingState

class EncodingState:

    def __init__(self, state: DataEncodingState):
        self.state = state 

    def setState(self, state: DataEncodingState):
        self.state = state

    def isFillMissing(self):
        return self.state.value == DataEncodingState.FILL_MISSING.value
    
    def isFloatEncoding(self):
        return self.state.value == DataEncodingState.FLOAT_ENCODING.value
    
    def isObjectTagging(self):
        return self.state.value == DataEncodingState.OBJECT_TAGGING.value
    
    def isValueStandarization(self):
        return self.state.value == DataEncodingState.VALUE_STANDARIZATION.value
    
    def isBinaryEncoding(self):
        return self.state.value == DataEncodingState.BINARY_ENCODING.value
    