import features as features
from dataset import SequenceSet
from model import SequenceModel
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
import torch
from torch.optim.lr_scheduler import ExponentialLR
BATCH_SIZE = 16

col = features.get_collection("bitcoin_data", "features")

# data from db to pytorch dataloaders
xx,yy = features.get_features_from_collection(col) # TODO: see if there is any synthetic data for financial stuff
x_train, x_test, y_train, y_test = train_test_split(xx,yy, test_size=30, random_state=42)
training_data = SequenceSet(x_train, y_train)
test_data = SequenceSet(x_test, y_test)
train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=True)

# Model delcaration
model = SequenceModel()

# optimizer
optimizer = torch.optim.Adam(model.parameters(),lr=1)
scheduler = ExponentialLR(optimizer, gamma=0.9) # this might need to change one day

best_epoch = {"epoch_num":0, "training_loss":1000000000, "test_loss":1000000000} # TODO: #1 this needs to hold all historical losses
epoch_count = 0
noprog = 0
while True:
    print("Epoch {} started".format(epoch_count))
    running_loss = 0
    # training loop
    for i, data in enumerate(train_dataloader):
        input, label = data
        optimizer.zero_grad()
        model.train()
        pred = model(input)
        loss = torch.sqrt((torch.squeeze(pred) - label)**2).sum()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    train_epoch_loss = running_loss / (len(train_dataloader) * BATCH_SIZE)

    # test loop
    running_test_loss = 0
    for i, data in enumerate(test_dataloader):
        test_input, test_label = data
        model.eval()
        test_pred = model(test_input)
        running_test_loss += torch.sqrt((torch.squeeze(test_pred) - test_label)**2).sum().item()

    test_epoch_loss = running_test_loss / (len(test_dataloader) * BATCH_SIZE)

    # learning schedule rules
    if best_epoch["test_loss"] >= test_epoch_loss:
        print("Average Loss: ${}".format(test_epoch_loss))
        best_epoch = {"epoch_num":epoch_count,"training_loss":train_epoch_loss, "test_loss":test_epoch_loss}
        no_prog = 0
    else:
        no_prog += 1
        if no_prog == 39:
            break
        if no_prog % 3 == 0:
            scheduler.step()
    epoch_count += 1





