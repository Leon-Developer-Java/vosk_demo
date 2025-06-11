#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载Vosk最小参数模型的脚本
"""

import os
import urllib.request
import zipfile
import shutil

def download_file(url, filename):
    """
    下载文件并显示进度
    """
    def progress_hook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, (downloaded * 100) // total_size)
            print(f"\r下载进度: {percent}% ({downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB)", end='', flush=True)
    
    print(f"正在下载: {filename}")
    urllib.request.urlretrieve(url, filename, progress_hook)
    print("\n下载完成！")

def extract_model(zip_path, extract_to="."):
    """
    解压模型文件
    """
    print(f"正在解压: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("解压完成！")

def setup_model(model_type="cn"):
    """
    设置模型
    
    Args:
        model_type (str): 模型类型，'cn' 为中文，'en' 为英文
    """
    models = {
        "cn": {
            "url": "https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip",
            "filename": "vosk-model-small-cn-0.22.zip",
            "folder": "vosk-model-small-cn-0.22",
            "size": "42MB",
            "description": "中文小型模型"
        },
        "en": {
            "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
            "filename": "vosk-model-small-en-us-0.15.zip",
            "folder": "vosk-model-small-en-us-0.15",
            "size": "40MB",
            "description": "英文小型模型"
        }
    }
    
    if model_type not in models:
        print(f"不支持的模型类型: {model_type}")
        print("支持的类型: cn (中文), en (英文)")
        return False
    
    model_info = models[model_type]
    
    print(f"=== 下载 {model_info['description']} ===")
    print(f"模型大小: {model_info['size']}")
    print(f"下载地址: {model_info['url']}")
    print()
    
    # 检查是否已存在模型
    if os.path.exists("model"):
        response = input("检测到已存在模型文件夹，是否覆盖？(y/n): ")
        if response.lower() != 'y':
            print("取消下载")
            return False
        shutil.rmtree("model")
    
    try:
        # 下载模型
        if not os.path.exists(model_info['filename']):
            download_file(model_info['url'], model_info['filename'])
        else:
            print(f"模型文件 {model_info['filename']} 已存在，跳过下载")
        
        # 解压模型
        extract_model(model_info['filename'])
        
        # 重命名文件夹
        if os.path.exists(model_info['folder']):
            os.rename(model_info['folder'], "model")
            print(f"模型已设置完成！文件夹已重命名为 'model'")
        else:
            print(f"警告：未找到解压后的文件夹 {model_info['folder']}")
            return False
        
        # 清理zip文件
        cleanup = input("是否删除下载的zip文件？(y/n): ")
        if cleanup.lower() == 'y':
            os.remove(model_info['filename'])
            print("zip文件已删除")
        
        print("\n=== 模型设置完成 ===")
        print("现在可以运行 real_time_speech_recognition.py 进行语音识别了！")
        return True
        
    except Exception as e:
        print(f"下载或设置过程中发生错误: {e}")
        return False

def main():
    """
    主函数
    """
    print("=== Vosk 模型下载工具 ===")
    print("此工具将下载最小参数的Vosk模型")
    print()
    
    print("可用的模型:")
    print("1. 中文模型 (vosk-model-small-cn-0.22, 42MB)")
    print("2. 英文模型 (vosk-model-small-en-us-0.15, 40MB)")
    print()
    
    while True:
        choice = input("请选择要下载的模型 (1/2): ").strip()
        
        if choice == "1":
            setup_model("cn")
            break
        elif choice == "2":
            setup_model("en")
            break
        else:
            print("无效选择，请输入 1 或 2")

if __name__ == "__main__":
    main()