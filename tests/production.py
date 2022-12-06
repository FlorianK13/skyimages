from skyimages.dataset import SKIPPDDataSet
import torch

traindata = SKIPPDDataSet(download=False)
testdata = SKIPPDDataSet(download=False, train=False)

trainloader = torch.utils.data.DataLoader(
    traindata, batch_size=200, shuffle=True, num_workers=0
)
testloader = torch.utils.data.DataLoader(
    testdata, batch_size=20, shuffle=False, num_workers=0
)
