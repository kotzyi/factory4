import nvidia_smi


def use_gpu():
    nvidia_smi.nvmlInit()

    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)

    print("Total memory:", info.total)
    print("Free memory:", info.free)
    print("Used memory:", info.used)
    nvidia_smi.nvmlShutdown()

    if info.used > 1000000000:
        return True
    else:
        return False
