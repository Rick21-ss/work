import os
import json
import subprocess
from azure.storage.blob import BlobServiceClient

class ConfigManager:
    def __init__(self, config_path="config.json", extra_config_path=None):
        self.config_path = config_path
        self.extra_config_path = extra_config_path
        self.config = self.load_config()
        if extra_config_path:
            self.extra_config = self.load_config(extra_config_path)
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"配置文件 {self.config_path} 未找到")
        except json.JSONDecodeError:
            raise Exception(f"配置文件 {self.config_path} 格式错误")

    def get_storage_config(self):
        return self.config["storage"]
    
    def get_download_config(self):
        return self.config["download"]
    
    def get_evaluation_config(self):
        return self.config["evaluation"]
    
    def get_upload_config(self):
        return self.config["upload"]

# 读取数据
def download_folder(config_manager):
    download_config = config_manager.get_download_config()
    storage_config = config_manager.get_storage_config()
    
    blob_folder_path = download_config["blob_folder_path"]
    local_folder_path = download_config["local_folder_path"]
    
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_config['account_name']}.blob.core.windows.net",
        credential=os.environ[storage_config["environment_key"]]
    )
    
    container_client = blob_service_client.get_container_client(storage_config["container_name"])
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
    
    print(f"下载完成，共下载 {downloaded_count} 个文件")
    return downloaded_count

# 使用OpenCompass评估命令
def run_evaluation(config_manager):
    eval_config = config_manager.get_evaluation_config()
    
    cmd = [
        "python", "run.py", 
        "--models", *eval_config["models"], 
        "--datasets", *eval_config["datasets"], 
        "-w", eval_config["work_dir"]
    ]
    
    if eval_config.get("debug", False):
        cmd.append("--debug")
    
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode == 0

# 回传结果
def upload_results(config_manager):
    upload_config = config_manager.get_upload_config()
    storage_config = config_manager.get_storage_config()
    
    local_results_folder = upload_config["local_results_folder"]
    blob_folder = upload_config["blob_results_folder"]
    
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_config['account_name']}.blob.core.windows.net",
        credential=os.environ[storage_config["environment_key"]]
    )
    
    container_client = blob_service_client.get_container_client(storage_config["container_name"])
    
    uploaded_count = 0
    
    for root, _, files in os.walk(local_results_folder):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_results_folder)
            blob_path = os.path.join(blob_folder, relative_path).replace("\\", "/")
            
            with open(local_path, "rb") as data:
                container_client.upload_blob(name=blob_path, data=data, overwrite=True)
            
            uploaded_count += 1
            print(f"上传: {blob_path}")
    
    print(f"结果上传完成，共上传 {uploaded_count} 个文件")
    return uploaded_count > 0

if __name__ == "__main__":
    # 初始化配置管理器
    main_config_manager = ConfigManager("config.json")  # 主配置
    

    
    # 执行流程
    download_folder(main_config_manager)
    run_evaluation(main_config_manager)
    upload_results(main_config_manager)