import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class SequenceModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        
        self.lstm = nn.LSTM()
        self.linear = nn.Linear()
        self.linear = nn.Linear()

    def forward(self, input):
        return
