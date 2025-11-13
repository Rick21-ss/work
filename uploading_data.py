import os
from azure.storage.blob import BlobServiceClient
from opencompass.cli.main import main

# 配置参数
STORAGE_ACCOUNT_NAME = "rick21"
ACCOUNT_KEY = os.environ["AZURE_STORAGE_KEY"]
CONTAINER_NAME = "opencompass"

local_folder = "/Users/shuishui/Desktop/opencompass/data/ceval"#本地上传的数据的具体路径
blob_folder = "datasets/ceval"#存储桶中要存储的位置


# 批量上传文件夹中的所有文件
def upload_multiple_blobs():
    container_client = BlobServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=ACCOUNT_KEY
    ).get_container_client(CONTAINER_NAME)

    for root, _, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            blob_path = os.path.join(blob_folder, os.path.relpath(local_path, local_folder)).replace("\\", "/")
            with open(local_path, "rb") as data:
                container_client.upload_blob(name=blob_path, data=data, overwrite=True)

if __name__ == "__main__":
    
    upload_multiple_blobs()