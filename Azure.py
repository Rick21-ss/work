import os
import subprocess
from azure.storage.blob import BlobServiceClient

# 配置参数
STORAGE_ACCOUNT_NAME = "rick21"
ACCOUNT_KEY = os.environ["AZURE_STORAGE_KEY"]
CONTAINER_NAME = "opencompass"

#读取数据
def download_folder(blob_folder_path, local_folder_path):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=ACCOUNT_KEY
    )
    
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    os.makedirs(local_folder_path, exist_ok=True)
    
    blob_list = container_client.list_blobs(name_starts_with=blob_folder_path)
    downloaded_count = 0
    
    for blob in blob_list:
        relative_path = blob.name.replace('datasets/', '', 1)
        local_file_path = os.path.join(local_folder_path, relative_path)
        
        local_dir = os.path.dirname(local_file_path)
        if local_dir:
            os.makedirs(local_dir, exist_ok=True)
        
        print(f"下载: {blob.name}")
        blob_client = container_client.get_blob_client(blob.name)
        
        with open(local_file_path, "wb") as download_file:
            download_stream = blob_client.download_blob()
            download_file.write(download_stream.readall())
        
        downloaded_count += 1
        print(f"完成: {local_file_path}")
    
    print(f"下载完成， 共下载 {downloaded_count} 个文件")

# 使用OpenCompass评估命令
def run_evaluation():
    cmd = [
        "python", "run.py", 
        "--models", "qwen_api", "qianfan_api", 
        "--datasets", "mmlu_gen", 
        "-w", "outputs/mmlu_test", 
        "--debug"
    ]
    
    result = subprocess.run(cmd)
    return result.returncode == 0

#回传结果
def upload_results(results_folder, blob_folder):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=ACCOUNT_KEY
    )
    
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    
    uploaded_count = 0
    
    for root, _, files in os.walk(results_folder):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, results_folder)
            blob_path = os.path.join(blob_folder, relative_path).replace("\\", "/")
            
            with open(local_path, "rb") as data:
                container_client.upload_blob(name=blob_path, data=data, overwrite=True)
            
            uploaded_count += 1
    print(f"结果上传完成完成")
    return uploaded_count > 0



if __name__ == "__main__":
    download_folder("datasets/mmlu", "/Users/shuishui/Desktop/opencompass/data")#("存储桶中的位置","本地的位置")
    run_evaluation()
    upload_results("outputs/mmlu_test", "results/mmlu_test")#("本地的位置","存储桶中的位置")