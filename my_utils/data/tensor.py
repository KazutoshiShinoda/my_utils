import torch


def to_list(tensor: torch.Tensor):
    return tensor.detach().cpu().tolist()
