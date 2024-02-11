import requests
import os

# +===============================+
# |   Function to Download and    |
# |        Save the Model         |
# +===============================+
def saveModel(PathSave, name, downloadUrl):
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