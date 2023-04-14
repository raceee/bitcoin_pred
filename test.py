import features
from dataset import SequenceSet

col = features.get_collection("bitcoin_data", "features")

xx,yy = features.get_features_from_collection(col)

bit_dataset = SequenceSet(xx,yy)

print(bit_dataset.x)