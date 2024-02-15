import os

from .configAccess import getConfig
config = getConfig()

A1111_PATH = config["A1111_PATH"]

# Dictionary of model paths
MODELPATH = {
    "LORA": A1111_PATH + "\stable-diffusion-webui\models\Lora",
    "CHECKPOINT": A1111_PATH + "\stable-diffusion-webui\models\Stable-diffusion",
    "HYPERNETWORK": A1111_PATH + "\stable-diffusion-webui\models\hypernetworks",
    "EMBEDDING": A1111_PATH + "\stable-diffusion-webui\embeddings"
}

def checkingFile():
    totalTensor = 0
    corruptedTensorFile = []
    corruptedData = []
    # +============================+
    # |  Checking the Model Path   |
    # +============================+
    for i in MODELPATH:
        for root, dirs, files in os.walk(MODELPATH[i]):
            for file in files:
                if file.endswith(".safetensors"):
                    totalTensor += 1
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path) / 1024
                    if file_size < 500:
                        filename, _ = os.path.splitext(file)
                        print("Corrupted File: " + filename)
                        file_pathWithoutName = os.path.dirname(file_path)
                        corruptedDataTensor = {
                            "Name": filename,
                            "Path": file_pathWithoutName,
                            "ëxtension": ".safetensors"
                        }
                        corruptedTensorFile.append(corruptedDataTensor)
    for i in corruptedTensorFile:
        dataToExterminate = {
            "Name": i["Name"],
            "Path": i["Path"],
            "Additional": []
        }
        # find file with same name but different extension
        for root, dirs, files in os.walk(i["Path"]):
            for file in files:
                if file.startswith(i["Name"]):
                    pathToFile = os.path.join(root, file)
                    dataToExterminate["Additional"].append(pathToFile)
                    
        # print(dataToExterminate)
        corruptedData.append(dataToExterminate)
                    
    # for i in corruptedData:
    #     print(i["Additional"])
    
    # delete corrupted file
    for i in corruptedData:
        for iAdditional in i["Additional"]:
            os.remove(iAdditional)

                          
    
    print("Total Tensor: " + str(totalTensor))
    
    
# checkFile()
            
            