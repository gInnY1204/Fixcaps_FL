import torch
import torch.utils.data as data
from torchvision.datasets import MNIST
import os, sys


class MNIST_truncated(data.Dataset):
    def __init__(
        self, root, dataidxs=None, train=True, transform=None, download=True,
    ):
        self.root = root
        self.dataidxs = dataidxs
        self.train = train
        self.transform = transform
        self.download = download
        self.num_classes = 10

        self.data, self.targets = self._build_truncated_dataset()

    def _build_truncated_dataset(self):
        sys.stdout = open(os.devnull, "w")
        base_dataset = MNIST(
            os.path.join(self.root, "mnist"),
            self.train,
            self.transform,
            None,
            self.download,
        )
        sys.stdout = sys.__stdout__

        data = base_dataset.data
        targets = torch.LongTensor(base_dataset.targets)

        if self.dataidxs is not None:
            data = data[self.dataidxs]
            targets = targets[self.dataidxs]

        return data, targets

    def __getitem__(self, index):
        img, targets = self.data[index], self.targets[index]

        if self.transform is not None:
            img = self.transform(img)

        return img, targets

    def __len__(self):
        return len(self.data)
