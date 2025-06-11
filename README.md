# Vosk 实时语音识别演示

这个项目演示了如何使用 Vosk 的最小参数模型进行实时语音识别。Vosk 是一个开源的离线语音识别工具包，支持多种语言。

## 特性

- 🎯 **最小参数模型**: 使用 Vosk 最小的预训练模型（40-42MB）
- 🚀 **实时识别**: 支持实时语音转文字
- 📱 **轻量级**: 适合在移动设备、树莓派等资源受限设备上运行
- 🌐 **离线工作**: 无需网络连接
- 🔧 **易于使用**: 提供简单易用的 Python 接口

## 支持的模型

| 语言 | 模型名称 | 大小 | 描述 |
|------|----------|------|------|
| 中文 | vosk-model-small-cn-0.22 | 42MB | 轻量级中文模型 |
| 英文 | vosk-model-small-en-us-0.15 | 40MB | 轻量级美式英语模型 |

## 安装依赖

1. 安装 Python 依赖包：
```bash
pip install -r requirements.txt
```

**注意**: 如果在 Windows 上安装 PyAudio 遇到问题，请参考 [Windows 安装指南](INSTALL_GUIDE.md) 获取详细解决方案。

## 使用方法

### 步骤 1: 下载模型

运行模型下载脚本：
```bash
python download_model.py
```

按照提示选择要下载的模型：
- 输入 `1` 下载中文模型
- 输入 `2` 下载英文模型

### 步骤 2: 运行语音识别

有两个版本可供选择：

#### 完整版（推荐）
```bash
python real_time_speech_recognition.py
```

特性：
- 详细的错误处理
- 音频设备检测
- 完整的日志输出
- 资源清理

#### 简化版
```bash
python simple_speech_recognition.py
```

特性：
- 代码简洁
- 快速启动
- 适合学习和测试

## 文件说明

- `requirements.txt` - Python 依赖包列表
- `download_model.py` - 模型下载脚本
- `real_time_speech_recognition.py` - 完整版实时语音识别程序
- `simple_speech_recognition.py` - 简化版语音识别程序
- `README.md` - 项目说明文档

## 使用示例

1. 首次使用：
```bash
# 安装依赖
pip install -r requirements.txt

# 下载模型
python download_model.py

# 运行语音识别
python real_time_speech_recognition.py
```

2. 程序运行后，对着麦克风说话，程序会实时显示识别结果。

3. 按 `Ctrl+C` 停止程序。

## 系统要求

- Python 3.6+
- 麦克风设备
- 至少 300MB 内存（运行时）
- 约 50MB 磁盘空间（模型文件）

## 故障排除

### 常见问题

1. **PyAudio 安装失败**
   - Windows: 使用 `pipwin install pyaudio`
   - Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`
   - macOS: `brew install portaudio`

2. **找不到麦克风设备**
   - 检查麦克风是否正确连接
   - 确认系统音频设置中麦克风可用
   - 运行程序时会显示可用的音频设备列表

3. **模型加载失败**
   - 确保已运行 `download_model.py` 下载模型
   - 检查 `model` 文件夹是否存在且包含模型文件
   - 重新下载模型

4. **识别准确率低**
   - 确保环境安静
   - 调整麦克风音量
   - 清晰发音
   - 考虑使用更大的模型（需要更多内存）

## 性能优化

- **内存使用**: 小型模型约占用 300MB 内存
- **CPU 使用**: 在现代 CPU 上实时处理无压力
- **延迟**: 通常在 100-300ms 之间

## 扩展功能

可以基于此项目扩展的功能：
- 语音命令识别
- 实时字幕生成
- 语音转文字记录
- 多语言切换
- 自定义词汇表

## 相关链接

- [Vosk 官方网站](https://alphacephei.com/vosk/)
- [Vosk GitHub](https://github.com/alphacep/vosk-api)
- [Vosk 模型下载](https://alphacephei.com/vosk/models)
- [Vosk 文档](https://alphacephei.com/vosk/install)

## 许可证

本项目代码使用 MIT 许可证。Vosk 模型使用 Apache 2.0 许可证。