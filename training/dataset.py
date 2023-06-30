import torch
from sklearn import preprocessing

class SequenceSet(torch.utils.data.Dataset):
    def __init__(self, X, Y) -> None:
        super().__init__()
        self.x = X
        self.y = Y
        

    def __len__(self):
        return self.x.shape[0]
    
    def normalize(self,X):
        print("normalizing")
        scaler_one = preprocessing.MinMaxScaler().fit(X[:,:,0])
        scaler_two = preprocessing.MinMaxScaler().fit(X[:,:,1])
        scaler_three = preprocessing.MinMaxScaler().fit(X[:,:,2])

        one_scaled = torch.from_numpy(scaler_one.transform(X[:,:,0]))
        two_scaled = torch.from_numpy(scaler_two.transform(X[:,:,1]))
        three_scaled = torch.from_numpy(scaler_three.transform(X[:,:,2]))

        return torch.stack([one_scaled, two_scaled, three_scaled], dim=2)

    def __getitem__(self, index:int):
        return self.x[index], self.y[index][0] # 0 on the y index just to return the price and not the other info
    