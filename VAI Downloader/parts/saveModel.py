import requests
import os

# +===============================+
# |   Function to Download and    |
# |        Save the Model         |
# +===============================+
def saveModel(PathSave, moddelData):
    name = moddelData["Name"]
    downloadUrl = moddelData["URL"]
    model = moddelData["model"]
    trigger = moddelData["trigger"]
    
    
    dataTemp = {
        "description": None,
        "sd version": model,
        "activation text": trigger,
        "preferred weight": 0.8,
    }
    
    # save the data to json file
    import json
    with open(os.path.join(PathSave, name + ".json"), "w") as f:
        json.dump(dataTemp, f, indent=4)
    
    
    print("Saving Model: " + name)
    modelName = name
    # +==================================+
    # | Removing Unnecessary Symbols     |
    # | on the Model Name                |
    # +==================================+
    modelName = modelName.replace("/", " ")
    modelName = modelName.replace("\\", " ")
    modelName = modelName.replace("|", " ")
    modelFormat = ".safetensors"
    
    modelFolder = PathSave
    # +===========================+
    # | Downloading the Model     |
    # +===========================+
    rs = requests.get(downloadUrl)
        
    # +===========================+
    # | Saving the Model          |
    # +===========================+
    with open(os.path.join(modelFolder, modelName + modelFormat), "wb") as f:
        f.write(rs.content)
        
# data = {
#     "URL": "https://www.google.com",
#     "Name": "Google",
#     "model": "SD 1",
#     "trigger": ["SD 1", "SD 2"]
# }
