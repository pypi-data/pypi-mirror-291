import torch


def test_cuda():
    print(torch.__version__)
    print(torch.cuda.is_available())
