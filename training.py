import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class SequenceModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        
        self.lstm = nn.LSTM(input_size=3, hidden_size=20, num_layers=1, batch_first=True)
        self.linear = nn.Linear(in_features=20, out_features=1)

    def forward(self, input):
        x, (hn, cn) = self.lstm(input.float())
        return self.linear(torch.squeeze(hn)) # use linear activation for regression

    def one_epoch(self, train_dataloader):
        running_loss = 0

        for i, data in train_dataloader:
            input, label = data
            self.fo
        return
    
    def test_one_epoch(self, test_dataloader):
        return

def training_():
    return

def test_():
    return

# if __name__ == "__main__":
#     while True:
