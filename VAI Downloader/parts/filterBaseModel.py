def CategorizeModelBase(input_str):
    if "SDXL" in input_str:
        return "SDXL"
    elif "SD 2" in input_str:
        return "SD 2"
    elif "SD 1" in input_str:
        return "SD 1"
    else:
        return "Unknown"