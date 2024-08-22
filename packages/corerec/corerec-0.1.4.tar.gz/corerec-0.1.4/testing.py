import engine.corerec as cr
# import vish_graphs as vg
import torch_geometric
from torch_geometric.data import Data
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
df = np.loadtxt("/Users/visheshyadav/Documents/Github/COrerec/src/SANDBOX/swad.csv", delimiter=",")
k = 23
g_d =Data(df)
d_l= DataLoader(df,batch_size=5,shuffle=False)

n=2
dm=128
nh=8
df1=512
input_dim= len(df[0])
model = cr.GraphTransformer(n,dm,nh,df1,input_dim=input_dim)
c=nn.MSELoss()
o=cr.optim.Adam(model.parameters(), lr=0.001)

# n_e=100
cr.train_model(model=model, data_loader=d_l, criterion=c, optimizer=o,num_epochs=100)

ni=2
re=cr.predict(model, df, node_index=ni, top_k=5,threshold=0.5)
print(re)

