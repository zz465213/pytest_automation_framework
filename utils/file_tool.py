import logging
import os
import shutil
import yaml


def cleanup_folder(temp_dir):
    """清理臨時文件和目錄"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        logging.info(f"🟢 已清理臨時目錄: {temp_dir}")
    else:
        logging.error(f"🔴 清理臨時目錄: {temp_dir} 失敗")
        raise Exception


def rename_file(old_path, new_path):
    """重命名文件"""
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return new_path
    else:
        logging.error(f"🔴 Allure 報告重命名失敗，請檢查新路徑{new_path}及舊路徑{old_path}")
        return old_path


def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        configs = yaml.load(f, Loader=yaml.FullLoader)
        return configs


def write_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
