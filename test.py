import features
from dataset import SequenceSet
from training import SequenceModel
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

col = features.get_collection("bitcoin_data", "features")

xx,yy = features.get_features_from_collection(col)

x_train, x_test, y_train, y_test = train_test_split(xx,yy, test_size=30, random_state=42)
training_data = SequenceSet(x_train, y_train)
test_data = SequenceSet(x_test, y_test)
train_dataloader = DataLoader(training_data, batch_size=16, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=16, shuffle=True)

bit_dataset = SequenceSet(xx,yy)

model = SequenceModel()


print(bit_dataset.x)