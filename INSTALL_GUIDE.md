# Windows 安装指南

## PyAudio 安装问题解决方案

如果您在 Windows 上遇到 PyAudio 安装错误，请按照以下步骤解决：

### 错误信息
```
ERROR: Failed building wheel for pyaudio
error: Microsoft Visual C++ 14.0 or greater is required
```

### 解决方案

#### 方案一：使用预编译的 wheel 文件（推荐）

1. 访问 [Python Extension Packages for Windows](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. 下载适合您 Python 版本的 PyAudio wheel 文件
3. 使用 pip 安装下载的文件：
   ```bash
   pip install PyAudio-0.2.11-cp312-cp312-win_amd64.whl
   ```

#### 方案二：使用 pipwin（简单）

```bash
pip install pipwin
pipwin install pyaudio
```

#### 方案三：使用 conda（如果您使用 Anaconda）

```bash
conda install pyaudio
```

#### 方案四：安装 Microsoft Visual C++ Build Tools

1. 下载并安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. 重新运行：
   ```bash
   pip install -r requirements.txt
   ```

### 验证安装

安装完成后，运行测试脚本验证环境：

```bash
python test_environment.py
```

### 完整安装流程

1. **解决 PyAudio 问题**（选择上述方案之一）
2. **安装其他依赖**：
   ```bash
   pip install vosk
   ```
3. **下载模型**：
   ```bash
   python download_model.py
   ```
4. **运行程序**：
   ```bash
   python real_time_speech_recognition.py
   ```

### 常见问题

**Q: 我应该选择哪个方案？**
A: 推荐按顺序尝试：pipwin > conda > 预编译wheel > Build Tools

**Q: 如何确定我的 Python 版本？**
A: 运行 `python --version` 查看版本信息

**Q: 下载的 wheel 文件名称含义？**
A: `cp312` 表示 Python 3.12，`win_amd64` 表示 64位 Windows

### 技术支持

如果仍然遇到问题，请：
1. 运行 `python test_environment.py` 获取详细错误信息
2. 检查您的 Python 版本和系统架构
3. 确保使用管理员权限运行命令提示符