from preprocessing.missing_values.MissingValuesFiller import MissingValuesFiller
from preprocessing.decimal_encoding.DecimalEncoder import DecimalEncoder
from preprocessing.object_tagging.ObjectTagger import ObjectTagger

class Preprocessor:

    def __init__(
        self,
        missing_values_filler: MissingValuesFiller,
        decimal_encoder: DecimalEncoder,
        object_tagger: ObjectTagger
    ):
        self.missing_values_filler = missing_values_filler
        self.decimal_encoder = decimal_encoder
        self.object_tagger = object_tagger

    def run(self, df, target):
        df = self.missing_values_filler.fill_missing(df, target)
        df = self.decimal_encoder.encode(df, target)
        df = self.object_tagger.tag_objects(df, target)

        return df 