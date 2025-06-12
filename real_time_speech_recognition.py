#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时语音识别程序
使用Vosk最小参数模型进行实时语音识别
"""

import sys
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

def list_available_models():
    """
    列出可用的模型
    """
    models_dir = "models"
    if not os.path.exists(models_dir):
        return []
    
    models = []
    for item in os.listdir(models_dir):
        model_path = os.path.join(models_dir, item)
        if os.path.isdir(model_path):
            models.append(item)
    return models

def select_model():
    """
    选择要使用的模型
    """
    # 列出models目录中的模型
    available_models = list_available_models()
    if not available_models:
        print("错误：未找到任何模型")
        print("请先运行 download_model.py 下载模型")
        return None
    
    print("\n可用的模型：")
    for i, model in enumerate(available_models, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = input(f"\n请选择模型 (1-{len(available_models)}): ")
            index = int(choice) - 1
            if 0 <= index < len(available_models):
                selected_model = os.path.join("models", available_models[index])
                print(f"已选择模型: {selected_model}")
                return selected_model
            else:
                print("无效选择，请重新输入")
        except ValueError:
            print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n取消选择")
            return None

class RealTimeSpeechRecognizer:
    def __init__(self, model_path="model", sample_rate=16000):
        """
        初始化实时语音识别器
        
        Args:
            model_path (str): Vosk模型路径
            sample_rate (int): 音频采样率
        """
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.model = None
        self.recognizer = None
        self.audio = None
        self.stream = None
        
    def load_model(self):
        """
        加载Vosk模型
        """
        if not os.path.exists(self.model_path):
            print(f"错误：模型路径 '{self.model_path}' 不存在！")
            print("请从以下链接下载最小参数模型：")
            print("中文模型: https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip")
            print("英文模型: https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
            print("下载后解压到当前目录，并重命名为 'model'")
            return False
            
        try:
            print(f"正在加载模型: {self.model_path}")
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
            print("模型加载成功！")
            return True
        except Exception as e:
            print(f"模型加载失败: {e}")
            return False
    
    def setup_audio(self):
        """
        设置音频输入
        """
        try:
            self.audio = pyaudio.PyAudio()
            
            # 检查可用的音频设备
            print("\n可用的音频输入设备:")
            for i in range(self.audio.get_device_count()):
                info = self.audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    print(f"设备 {i}: {info['name']} (输入通道: {info['maxInputChannels']})")
            
            # 创建音频流
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=4096
            )
            
            print(f"\n音频流设置成功 (采样率: {self.sample_rate}Hz)")
            return True
            
        except Exception as e:
            print(f"音频设置失败: {e}")
            print("请确保您的麦克风设备正常工作")
            return False
    
    def start_recognition(self):
        """
        开始实时语音识别
        """
        if not self.load_model():
            return
            
        if not self.setup_audio():
            return
            
        print("\n=== 实时语音识别已启动 ===")
        print("请开始说话... (按 Ctrl+C 停止)")
        print("-" * 50)
        
        try:
            while True:
                # 读取音频数据
                data = self.stream.read(4096, exception_on_overflow=False)
                
                # 进行语音识别
                if self.recognizer.AcceptWaveform(data):
                    # 完整的识别结果
                    result = json.loads(self.recognizer.Result())
                    if result['text']:
                        print(f"     ----    识别结果: {result['text']}")
                else:
                    # 部分识别结果（实时显示）
                    partial_result = json.loads(self.recognizer.PartialResult())
                    if partial_result['partial']:
                        print(f"\r正在识别: {partial_result['partial']}", end='', flush=True)
                        
        except KeyboardInterrupt:
            print("\n\n=== 语音识别已停止 ===")
        except Exception as e:
            print(f"\n识别过程中发生错误: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        清理资源
        """
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()
        print("资源清理完成")

def main():
    """
    主函数
    """
    print("=== Vosk 实时语音识别程序 ===")
    print("使用Vosk模型进行实时语音识别")
    print()
    
    # 选择模型
    model_path = select_model()
    if not model_path:
        return
    
    # 创建识别器实例
    recognizer = RealTimeSpeechRecognizer(model_path=model_path)
    
    # 开始识别
    recognizer.start_recognition()

if __name__ == "__main__":
    main()