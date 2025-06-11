#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版实时语音识别程序
使用Vosk最小参数模型
"""

import sys
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

def check_model():
    """
    检查模型是否存在
    """
    if not os.path.exists("model"):
        print("错误：未找到模型文件夹 'model'")
        print("请先运行 download_model.py 下载模型")
        return False
    return True

def main():
    """
    主函数 - 简化版语音识别
    """
    print("=== 简化版 Vosk 实时语音识别 ===")
    
    # 检查模型
    if not check_model():
        return
    
    # 加载模型
    print("正在加载模型...")
    try:
        model = Model("model")
        rec = KaldiRecognizer(model, 16000)
        print("模型加载成功！")
    except Exception as e:
        print(f"模型加载失败: {e}")
        return
    
    # 设置音频
    print("正在设置音频...")
    try:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        stream.start_stream()
        print("音频设置成功！")
    except Exception as e:
        print(f"音频设置失败: {e}")
        print("请确保麦克风设备正常工作")
        return
    
    print("\n开始语音识别...")
    print("请说话 (按 Ctrl+C 停止)")
    print("-" * 40)
    
    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if result['text']:
                    print(f" ---  识别结果: {result['text']}")
            else:
                partial = json.loads(rec.PartialResult())
                if partial['partial']:
                    print(f"\r正在识别: {partial['partial']}", end='', flush=True)
                    
    except KeyboardInterrupt:
        print("\n\n语音识别已停止")
    except Exception as e:
        print(f"\n发生错误: {e}")
    finally:
        # 清理资源
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("资源已清理")

if __name__ == "__main__":
    main()