import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class SequenceModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        
        self.lstm = nn.LSTM(input_size=3, hidden_size=20, num_layers=1, batch_first=True)
        self.batch_norm = nn.BatchNorm1d(num_features=20)  # Add batch normalization layer
        self.linear = nn.Linear(in_features=20, out_features=1)

    def forward(self, input):
        x, (hn, cn) = self.lstm(input.float())
        hn = self.batch_norm(hn.squeeze(0)).unsqueeze(0)

        return self.linear(torch.squeeze(hn)) # use linear activation for regression
