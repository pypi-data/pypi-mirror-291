import torch


def check_cuda():
    # Check if CUDA is available
    if torch.cuda.is_available():
        print("torch:",torch.__version__)
        print("CUDA Available:", torch.cuda.is_available())
        print("CUDA Version:", torch.version.cuda)
        print("cudnn:",torch.backends.cudnn.version())
        print("GPU Details:", torch.cuda.get_device_name(0))
    
    return torch.cuda.is_available()