#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境测试脚本
检查Vosk语音识别所需的环境和依赖
"""

import sys
import os
import platform

def test_python_version():
    """
    测试Python版本
    """
    print("=== Python 版本检查 ===")
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 6:
        print("✓ Python 版本符合要求 (3.6+)")
        return True
    else:
        print("✗ Python 版本过低，需要 3.6 或更高版本")
        return False

def test_dependencies():
    """
    测试依赖包
    """
    print("\n=== 依赖包检查 ===")
    
    dependencies = {
        'vosk': 'Vosk 语音识别库',
        'pyaudio': 'PyAudio 音频处理库',
        'json': 'JSON 处理库（内置）'
    }
    
    all_ok = True
    
    for package, description in dependencies.items():
        try:
            if package == 'json':
                import json
            elif package == 'vosk':
                import vosk
                print(f"✓ {description} - 版本: {vosk.__version__ if hasattr(vosk, '__version__') else '未知'}")
            elif package == 'pyaudio':
                import pyaudio
                print(f"✓ {description} - 已安装")
        except ImportError:
            print(f"✗ {description} - 未安装")
            all_ok = False
        except Exception as e:
            print(f"? {description} - 检查时出错: {e}")
            all_ok = False
    
    return all_ok

def test_audio_devices():
    """
    测试音频设备
    """
    print("\n=== 音频设备检查 ===")
    
    try:
        import pyaudio
        
        p = pyaudio.PyAudio()
        
        print(f"音频系统信息:")
        print(f"- 主机API数量: {p.get_host_api_count()}")
        print(f"- 设备数量: {p.get_device_count()}")
        
        input_devices = []
        output_devices = []
        
        for i in range(p.get_device_count()):
            try:
                info = p.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    input_devices.append((i, info['name'], info['maxInputChannels']))
                if info['maxOutputChannels'] > 0:
                    output_devices.append((i, info['name'], info['maxOutputChannels']))
            except Exception:
                continue
        
        print(f"\n输入设备 (麦克风):")
        if input_devices:
            for idx, name, channels in input_devices:
                print(f"  设备 {idx}: {name} ({channels} 通道)")
        else:
            print("  ✗ 未找到可用的输入设备")
            return False
        
        print(f"\n输出设备 (扬声器):")
        if output_devices:
            for idx, name, channels in output_devices[:3]:  # 只显示前3个
                print(f"  设备 {idx}: {name} ({channels} 通道)")
        
        p.terminate()
        print("\n✓ 音频设备检查完成")
        return len(input_devices) > 0
        
    except ImportError:
        print("✗ PyAudio 未安装，无法检查音频设备")
        return False
    except Exception as e:
        print(f"✗ 音频设备检查失败: {e}")
        return False

def test_model_files():
    """
    测试模型文件
    """
    print("\n=== 模型文件检查 ===")
    
    if os.path.exists("model"):
        print("✓ 找到模型文件夹 'model'")
        
        # 检查模型文件夹内容
        model_files = os.listdir("model")
        essential_files = ['am', 'graph', 'ivector']
        
        print("模型文件夹内容:")
        for file in model_files[:10]:  # 只显示前10个文件
            print(f"  - {file}")
        
        missing_files = []
        for essential in essential_files:
            found = any(essential in f for f in model_files)
            if found:
                print(f"✓ 找到必要文件: {essential}")
            else:
                missing_files.append(essential)
        
        if missing_files:
            print(f"✗ 缺少必要文件: {', '.join(missing_files)}")
            return False
        else:
            print("✓ 模型文件完整")
            return True
    else:
        print("✗ 未找到模型文件夹 'model'")
        print("请运行 'python download_model.py' 下载模型")
        return False

def test_vosk_functionality():
    """
    测试Vosk基本功能
    """
    print("\n=== Vosk 功能测试 ===")
    
    try:
        from vosk import Model, KaldiRecognizer
        
        if not os.path.exists("model"):
            print("✗ 无法测试Vosk功能：缺少模型文件")
            return False
        
        print("正在加载模型...")
        model = Model("model")
        rec = KaldiRecognizer(model, 16000)
        
        print("✓ Vosk 模型加载成功")
        print("✓ 识别器创建成功")
        
        # 测试空音频数据
        test_data = b'\x00' * 3200  # 0.1秒的静音数据
        result = rec.AcceptWaveform(test_data)
        
        print("✓ Vosk 基本功能正常")
        return True
        
    except ImportError:
        print("✗ Vosk 库未安装")
        return False
    except Exception as e:
        print(f"✗ Vosk 功能测试失败: {e}")
        return False

def main():
    """
    主测试函数
    """
    print("Vosk 语音识别环境测试")
    print("=" * 50)
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    print()
    
    tests = [
        ("Python版本", test_python_version),
        ("依赖包", test_dependencies),
        ("音频设备", test_audio_devices),
        ("模型文件", test_model_files),
        ("Vosk功能", test_vosk_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n测试 '{test_name}' 时发生错误: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("测试结果总结:")
    
    all_passed = True
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有测试通过！您的环境已准备就绪。")
        print("现在可以运行 'python real_time_speech_recognition.py' 开始语音识别。")
    else:
        print("⚠️  部分测试失败，请根据上述信息解决问题。")
        print("\n常见解决方案:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 下载模型: python download_model.py")
        print("3. 检查麦克风设备是否正常工作")

if __name__ == "__main__":
    main()