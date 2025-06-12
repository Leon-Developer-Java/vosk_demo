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

def setup_model(model_type="cn_small"):
    """
    设置模型
    
    Args:
        model_type (str): 模型类型
    """
    models = {
        "cn_small": {
            "url": "https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip",
            "filename": "vosk-model-small-cn-0.22.zip",
            "folder": "vosk-model-small-cn-0.22",
            "size": "42MB",
            "description": "中文小型模型（推荐）",
            "accuracy": "适合移动设备和树莓派，识别速度快"
        },
        "cn_standard": {
            "url": "https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip",
            "filename": "vosk-model-cn-0.22.zip",
            "folder": "vosk-model-cn-0.22",
            "size": "1.3GB",
            "description": "中文标准模型（高精度）",
            "accuracy": "服务器级别，识别精度更高"
        },
        "cn_kaldi": {
            "url": "https://alphacephei.com/vosk/models/vosk-model-cn-kaldi-multicn-0.15.zip",
            "filename": "vosk-model-cn-kaldi-multicn-0.15.zip",
            "folder": "vosk-model-cn-kaldi-multicn-0.15",
            "size": "1.5GB",
            "description": "中文Kaldi多方言模型",
            "accuracy": "支持多种中文方言，兼容性好"
        },
        "cn_old": {
            "url": "https://alphacephei.com/vosk/models/vosk-model-cn-0.15.zip",
            "filename": "vosk-model-cn-0.15.zip",
            "folder": "vosk-model-cn-0.15",
            "size": "1.67GB",
            "description": "中文旧版大模型",
            "accuracy": "较老版本，但稳定性好"
        },
        "en": {
            "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
            "filename": "vosk-model-small-en-us-0.15.zip",
            "folder": "vosk-model-small-en-us-0.15",
            "size": "40MB",
            "description": "英文小型模型",
            "accuracy": "适合英文语音识别"
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
    
    # 创建models目录用于存放所有模型
    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        print(f"创建模型存储目录: {models_dir}")
    
    # 检查是否已存在该特定模型
    model_path = os.path.join(models_dir, model_info['folder'])
    if os.path.exists(model_path):
        response = input(f"检测到已存在模型文件夹 '{model_info['folder']}'，是否覆盖？(y/n): ")
        if response.lower() != 'y':
            print("取消下载")
            return False
        shutil.rmtree(model_path)
    
    try:
        # 下载模型
        if not os.path.exists(model_info['filename']):
            download_file(model_info['url'], model_info['filename'])
        else:
            print(f"模型文件 {model_info['filename']} 已存在，跳过下载")
        
        # 解压模型到models目录
        extract_model(model_info['filename'], models_dir)
        
        # 检查解压结果
        if os.path.exists(model_path):
            print(f"模型已设置完成！模型位置: {model_path}")
        else:
            print(f"警告：未找到解压后的文件夹 {model_info['folder']}")
            return False
        
        # 清理zip文件
        cleanup = input("是否删除下载的zip文件？(y/n): ")
        if cleanup.lower() == 'y':
            os.remove(model_info['filename'])
            print("zip文件已删除")
        
        print("\n=== 模型设置完成 ===")
        print(f"模型类型: {model_info['description']}")
        print(f"模型路径: {model_path}")
        print("\n提示：在语音识别程序中使用时，请指定正确的模型路径。")
        print("现在可以运行 real_time_speech_recognition.py或simple_speech_recognition.py 进行语音识别了！")
        return True
        
    except Exception as e:
        print(f"下载或设置过程中发生错误: {e}")
        return False

def main():
    """
    主函数
    """
    print("Vosk 语音识别模型下载工具")
    print("="*50)
    print("请选择要下载的模型：")
    print("\n中文模型：")
    print("1. 中文小型模型（推荐） - 42MB")
    print("   适合移动设备和树莓派，识别速度快")
    print("2. 中文标准模型（高精度） - 1.3GB")
    print("   服务器级别，识别精度更高")
    print("3. 中文Kaldi多方言模型 - 1.5GB")
    print("   支持多种中文方言，兼容性好")
    print("4. 中文旧版大模型 - 1.67GB")
    print("   较老版本，但稳定性好")
    print("\n英文模型：")
    print("5. 英文小型模型 - 40MB")
    print("   适合英文语音识别")
    print("\n0. 退出")
    print("="*50)
    
    choice = input("请输入选择 (0-5): ")
    
    model_map = {
        "1": "cn_small",
        "2": "cn_standard", 
        "3": "cn_kaldi",
        "4": "cn_old",
        "5": "en"
    }
    
    if choice == "0":
        print("退出程序。")
        return
    elif choice in model_map:
        setup_model(model_map[choice])
        print("\n模型下载完成！")
        print("现在可以运行 real_time_speech_recognition.py或simple_speech_recognition.py 进行语音识别了！")
    else:
        print("无效选择！请输入 0-5 之间的数字。")
        return

if __name__ == "__main__":
    main()