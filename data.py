from torch.utils.data import Dataset, DataLoader
import torch
import utils
import pandas as pd
import numpy as np

def gaussian_expansion(D, mu_min=-1, delta_mu=0.2, mu_max=1, sigma=0.2):
    mu = np.arange(mu_min, mu_max + delta_mu, delta_mu)
    diff = D[:,:,np.newaxis] - mu[np.newaxis, np.newaxis, :]
    return np.exp(-diff ** 2 / (2 * sigma))

class QM8Dataset(Dataset):
    def __init__(self, target, max_atoms, num_gauss):
        df = pd.read_json('data/preprocessed.json')
        self.target = torch.FloatTensor(df[target])
        Zs, Ds, sizes = [], [], []
        for i, x in df.iterrows():
            Zs.append(utils.pad_(torch.LongTensor(x.Z), max_atoms))
            Ds.append(utils.pad_Dhat(torch.FloatTensor(gaussian_expansion(np.array(x.D), -1, 0.2, 1)), max_atoms))
            sizes.append(len(x.Z))
        self.Zs = torch.stack(Zs)
        self.Ds = torch.stack(Ds)
        self.sizes = torch.LongTensor(sizes)
        
    def __getitem__(self, idx):
        return self.Zs[idx], self.Ds[idx], self.sizes[idx], self.target[idx]
    
    def __len__(self):
        return len(self.Zs)
