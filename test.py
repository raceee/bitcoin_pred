import features
from dataset import SequenceSet
from training import SequenceModel
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch
from torch.optim.lr_scheduler import ExponentialLR

col = features.get_collection("bitcoin_data", "features")

# data from db to pytorch dataloaders
xx,yy = features.get_features_from_collection(col)
x_train, x_test, y_train, y_test = train_test_split(xx,yy, test_size=30, random_state=42)
training_data = SequenceSet(x_train, y_train)
test_data = SequenceSet(x_test, y_test)
train_dataloader = DataLoader(training_data, batch_size=16, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=16, shuffle=True)

# Model delcaration
model = SequenceModel()

# optimizer
optimizer = torch.optim.Adam(model.parameters(),lr=1)
scheduler = ExponentialLR(optimizer, gamma=0.9)

best_epoch = {"epoch_num":0, "loss":1000000000}
epoch_count = 0
noprog = 0
while True:
    print("Epoch {} started".format(epoch_count))
    running_loss = 0
    for i, data in enumerate(train_dataloader):
        # print(data)
        input, label = data
        optimizer.zero_grad()
        pred = model(input)
        loss = torch.sqrt((torch.squeeze(pred) - label)**2).sum()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        # if i == len(train_dataloader) - 1:
        #     avg_loss = running_loss / (i * 16)
        #     print("Average Loss: {}".format(avg_loss))
        #     print("noprog ", noprog)
        #     if avg_loss >= best_epoch[1]:
        #         scheduler.step()
        #         noprog +=1
        #         if noprog >= 3:
        #             break
        #     if avg_loss < best_epoch[1]:
        #         best_epoch = (epoch_count, avg_loss)
        #         noprog = 0
    epoch_loss = running_loss / (len(train_dataloader) * 16)
    if best_epoch["loss"] >= epoch_loss:
        print("Average Loss: {}".format(epoch_loss))
        best_epoch = {"epoch_num":epoch_count, "loss":epoch_loss}
        no_prog = 0
    else:
        no_prog += 1
        if no_prog == 3:
            scheduler.step()
    epoch_count += 1





