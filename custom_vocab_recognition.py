#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vosk API 运行时词汇表修改功能演示

这个脚本演示了如何使用Vosk API的运行时词汇表修改功能，
通过自定义词汇表来提高特定领域词汇的识别准确率。

作者: AI Assistant
日期: 2024
"""

import os
import sys
import json
import pyaudio
import vosk
import threading
import time
from typing import List, Optional

class CustomVocabRecognizer:
    """自定义词汇表语音识别器"""
    
    def __init__(self, model_path: str, vocab_file: str, sample_rate: int = 16000):
        """
        初始化自定义词汇表识别器
        
        Args:
            model_path (str): Vosk模型路径
            vocab_file (str): 自定义词汇表文件路径
            sample_rate (int): 音频采样率
        """
        self.model_path = model_path
        self.vocab_file = vocab_file
        self.sample_rate = sample_rate
        self.model = None
        self.recognizer = None
        self.audio = None
        self.stream = None
        self.custom_words = []
        self.is_running = False
        
    def load_custom_vocabulary(self) -> bool:
        """
        加载自定义词汇表
        
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            if not os.path.exists(self.vocab_file):
                print(f"错误：词汇表文件不存在: {self.vocab_file}")
                return False
                
            with open(self.vocab_file, 'r', encoding='utf-8') as f:
                # 读取所有行并去除空行和空白字符
                self.custom_words = [line.strip() for line in f.readlines() if line.strip()]
                
            print(f"成功加载自定义词汇表，共 {len(self.custom_words)} 个词汇")
            print(f"前10个词汇示例: {self.custom_words[:10]}")
            return True
            
        except Exception as e:
            print(f"加载词汇表时出错: {e}")
            return False
    
    def load_model(self) -> bool:
        """
        加载Vosk模型
        
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            if not os.path.exists(self.model_path):
                print(f"错误：模型路径不存在: {self.model_path}")
                return False
                
            print(f"正在加载模型: {self.model_path}")
            self.model = vosk.Model(self.model_path)
            print("模型加载成功")
            return True
            
        except Exception as e:
            print(f"加载模型时出错: {e}")
            return False
    
    def setup_recognizer(self, use_grammar_mode: bool = False) -> bool:
        """
        设置识别器并应用自定义词汇表
        
        Args:
            use_grammar_mode (bool): 是否使用语法模式
        
        Returns:
            bool: 设置成功返回True，失败返回False
        """
        try:
            # 创建识别器
            self.recognizer = vosk.KaldiRecognizer(self.model, self.sample_rate)
            
            if use_grammar_mode:
                # 使用语法模式
                grammar = self.create_advanced_grammar()
                self.recognizer.SetGrammar(grammar)
                print("已启用语法模式，将强制识别完整词组")
            else:
                # 使用词汇表模式
                words_json = json.dumps(self.custom_words, ensure_ascii=False)
                self.recognizer.SetWords(words_json)
                print(f"已设置自定义词汇表: {len(self.custom_words)} 个词汇")
            
            # 启用详细识别选项
            self.recognizer.SetWords(True)
            if hasattr(self.recognizer, 'SetPartialWords'):
                self.recognizer.SetPartialWords(True)
            
            print("识别器设置完成")
            return True
            
        except Exception as e:
            print(f"设置识别器时出错: {e}")
            return False
    
    def create_advanced_grammar(self) -> str:
        """
        创建高级语法规则，强制识别完整词组
        使用JSGF格式
        
        Returns:
            str: JSGF格式的语法规则
        """
        # 分类词汇
        long_functions = []  # 3-4字功能词
        short_words = []     # 1-2字词
        actions = []         # 动作词
        temperatures = []    # 温度词
        
        for word in self.custom_words:
            if len(word) >= 3 and any(suffix in word for suffix in ['功能', '模式', '预热', '零冷水', '增压']):
                long_functions.append(word)
            elif word in ['开', '关', '启动', '停止', '设置', '调到', '开启', '关闭']:
                actions.append(word)
            elif '度' in word:
                temperatures.append(word)
            else:
                short_words.append(word)
        
        # 创建JSGF语法规则
        grammar_lines = [
            "#JSGF V1.0 UTF-8 zh;",
            "grammar commands;",
            ""
        ]
        
        # 添加规则定义
        if long_functions:
            long_func_rule = " | ".join(long_functions[:50])  # 限制数量避免过长
            grammar_lines.append(f"<long_function> = {long_func_rule};")
        
        if actions:
            action_rule = " | ".join(actions)
            grammar_lines.append(f"<action> = {action_rule};")
        
        if temperatures:
            temp_rule = " | ".join(temperatures[:30])  # 限制数量
            grammar_lines.append(f"<temperature> = {temp_rule};")
        
        if short_words:
            short_rule = " | ".join(short_words[:50])  # 限制数量
            grammar_lines.append(f"<short_word> = {short_rule};")
        
        # 主规则
        main_rules = []
        if long_functions:
            main_rules.append("<long_function>")
        if actions and long_functions:
            main_rules.append("<action> <long_function>")
        if actions and short_words:
            main_rules.append("<action> <short_word>")
        if temperatures:
            main_rules.append("<temperature>")
            main_rules.append("调到 <temperature>")
        
        if main_rules:
            main_rule = " | ".join(main_rules)
            grammar_lines.append(f"public <command> = {main_rule};")
        else:
            # 如果没有分类成功，使用所有词汇
            all_words = " | ".join(self.custom_words[:100])  # 限制数量
            grammar_lines.append(f"public <command> = {all_words};")
        
        grammar_text = "\n".join(grammar_lines)
        print(f"创建JSGF语法规则: {len(long_functions)} 个长功能词, {len(actions)} 个动作词, {len(temperatures)} 个温度词")
        return grammar_text
    
    def setup_audio(self) -> bool:
        """
        设置音频输入
        
        Returns:
            bool: 设置成功返回True，失败返回False
        """
        try:
            self.audio = pyaudio.PyAudio()
            
            # 检查音频设备
            device_count = self.audio.get_device_count()
            print(f"检测到 {device_count} 个音频设备")
            
            # 查找默认输入设备
            default_input = self.audio.get_default_input_device_info()
            print(f"默认输入设备: {default_input['name']}")
            
            # 创建音频流
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=8192
            )
            
            print("音频设备设置完成")
            return True
            
        except Exception as e:
            print(f"设置音频设备时出错: {e}")
            return False
    
    def start_recognition(self, use_grammar_mode: bool = False):
        """
        开始语音识别
        
        Args:
            use_grammar_mode (bool): 是否使用语法模式
        """
        if not self.load_custom_vocabulary():
            return
            
        if not self.load_model():
            return
            
        if not self.setup_recognizer(use_grammar_mode):
            return
            
        if not self.setup_audio():
            return
        
        self.is_running = True
        mode_text = "语法模式" if use_grammar_mode else "词汇表模式"
        print(f"\n=== 自定义词汇表语音识别已启动 ({mode_text}) ===")
        print(f"已加载 {len(self.custom_words)} 个自定义词汇")
        if use_grammar_mode:
            print("语法模式：将强制识别完整词组，如'点动预热'、'儿童浴功能'等")
        print("请开始说话... (按 Ctrl+C 停止)")
        print("-" * 60)
        
        try:
            while self.is_running:
                # 读取音频数据
                data = self.stream.read(4096, exception_on_overflow=False)
                
                # 处理音频数据
                if self.recognizer.AcceptWaveform(data):
                    # 完整识别结果
                    result = json.loads(self.recognizer.Result())
                    if result.get('text'):
                        print(f"\n[完整识别] {result['text']}")
                        
                        # 检查是否包含自定义词汇
                        recognized_text = result['text']
                        matched_words = [word for word in self.custom_words if word in recognized_text]
                        if matched_words:
                            print(f"[匹配词汇] {', '.join(matched_words)}")
                else:
                    # 部分识别结果
                    partial_result = json.loads(self.recognizer.PartialResult())
                    if partial_result.get('partial'):
                        print(f"\r[实时识别] {partial_result['partial']}", end='', flush=True)
                        
        except KeyboardInterrupt:
            print("\n\n用户中断识别")
        except Exception as e:
            print(f"\n识别过程中出错: {e}")
        finally:
            self.stop_recognition()
    
    def stop_recognition(self):
        """
        停止语音识别并清理资源
        """
        self.is_running = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
        if self.audio:
            self.audio.terminate()
            
        print("\n语音识别已停止，资源已清理")
    
    def test_vocabulary_matching(self, test_text: str):
        """
        测试词汇匹配功能
        
        Args:
            test_text (str): 测试文本
        """
        print(f"\n=== 词汇匹配测试 ===")
        print(f"测试文本: {test_text}")
        
        matched_words = [word for word in self.custom_words if word in test_text]
        if matched_words:
            print(f"匹配的自定义词汇: {', '.join(matched_words)}")
        else:
            print("未找到匹配的自定义词汇")

def select_model() -> Optional[str]:
    """
    选择可用的模型
    
    Returns:
        Optional[str]: 选择的模型路径，如果没有可用模型则返回None
    """
    models_dir = "models"
    if not os.path.exists(models_dir):
        print(f"错误：模型目录不存在: {models_dir}")
        return None
    
    # 查找可用模型
    available_models = []
    for item in os.listdir(models_dir):
        model_path = os.path.join(models_dir, item)
        if os.path.isdir(model_path):
            available_models.append(model_path)
    
    if not available_models:
        print("错误：未找到可用的模型")
        return None
    
    print("\n可用的模型:")
    for i, model in enumerate(available_models, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = input(f"\n请选择模型 (1-{len(available_models)}): ").strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(available_models):
                    return available_models[index]
            print("无效选择，请重新输入")
        except KeyboardInterrupt:
            print("\n用户取消选择")
            return None

def main():
    """
    主函数
    """
    print("=== Vosk API 自定义词汇表语音识别演示 ===")
    print("这个程序演示了如何使用自定义词汇表提高特定领域的识别准确率")
    
    # 选择模型
    model_path = select_model()
    if not model_path:
        return
    
    # 词汇表文件路径
    vocab_file = "split_words.txt"
    
    # 创建识别器
    recognizer = CustomVocabRecognizer(model_path, vocab_file)
    
    # 测试词汇匹配
    recognizer.load_custom_vocabulary()
    recognizer.test_vocabulary_matching("请把温度调到三十五度")
    recognizer.test_vocabulary_matching("小万，开启AI节能模式")
    
    # 询问是否开始语音识别
    try:
        start_recognition = input("\n是否开始语音识别？(y/n): ").strip().lower()
        if start_recognition in ['y', 'yes', '是', '开始']:
            # 询问用户是否使用语法模式
            print("\n选择识别模式:")
            print("1. 词汇表模式 (默认)")
            print("2. 语法模式 (强制识别完整词组)")
            
            while True:
                choice = input("请选择模式 (1/2，直接回车默认选择1): ").strip()
                if choice == "" or choice == "1":
                    use_grammar_mode = False
                    break
                elif choice == "2":
                    use_grammar_mode = True
                    break
                else:
                    print("无效选择，请输入 1 或 2")
            
            recognizer.start_recognition(use_grammar_mode)
        else:
            print("程序结束")
    except KeyboardInterrupt:
        print("\n程序被用户中断")

if __name__ == "__main__":
    main()