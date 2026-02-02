# Installation Guide - Industrial Pipe and Pump Calculator

Complete installation instructions for different platforms and use cases.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Detailed Installation](#detailed-installation)
4. [Platform-Specific Instructions](#platform-specific-instructions)
5. [Troubleshooting](#troubleshooting)
6. [Verification](#verification)

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+, Debian 10+)
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Disk Space**: 500 MB for installation
- **Internet**: Required for initial package download

### Recommended Requirements

- **Python**: 3.10 or 3.11
- **RAM**: 8 GB or more
- **Display**: 1920x1080 or higher resolution
- **Browser**: Chrome, Firefox, or Edge (latest versions)

## Quick Installation

### For Linux/macOS

```bash
# Clone the repository
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator

# Run the installation script
chmod +x run.sh
./run.sh
```

### For Windows

```cmd
REM Clone the repository
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator

REM Run the installation script
run.bat
```

The application will automatically:
1. Create a virtual environment
2. Install all dependencies
3. Launch the Streamlit application

## Detailed Installation

### Step 1: Install Python

#### Windows

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```cmd
   python --version
   ```

#### macOS

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Verify installation
python3 --version
```

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
```

### Step 2: Install Git

#### Windows

Download and install from [git-scm.com](https://git-scm.com/download/win)

#### macOS

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Or using Homebrew
brew install git
```

#### Linux

```bash
sudo apt install git
```

### Step 3: Clone the Repository

```bash
# HTTPS (recommended for read-only)
git clone https://github.com/your-username/pump-calculator.git

# Or SSH (if you have SSH keys configured)
git clone git@github.com:your-username/pump-calculator.git

# Navigate to project directory
cd pump-calculator
```

### Step 4: Create Virtual Environment

#### Linux/macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

#### Windows (Command Prompt)

```cmd
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate.bat

REM Verify activation
where python
```

#### Windows (PowerShell)

```powershell
# Create virtual environment
python -m venv venv

# Enable script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
venv\Scripts\Activate.ps1

# Verify activation
Get-Command python
```

### Step 5: Install Dependencies

```bash
# Ensure virtual environment is activated
# Update pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt

# Verify installations
pip list
```

### Step 6: Run the Application

```bash
# Ensure virtual environment is activated

# Start Streamlit application
streamlit run app.py
```

The application will open automatically in your default browser at:
- Local: http://localhost:8501
- Network: http://YOUR_IP:8501

## Platform-Specific Instructions

### Linux

#### Ubuntu/Debian

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Some packages may require additional libraries
sudo apt install python3-dev build-essential

# Clone and setup
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

#### Fedora/RHEL/CentOS

```bash
# Install system dependencies
sudo dnf install python3 python3-pip git

# Clone and setup
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

#### Arch Linux

```bash
# Install system dependencies
sudo pacman -S python python-pip git

# Clone and setup
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### macOS

#### Using Homebrew

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python@3.11 git

# Clone and setup
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Windows

#### Using Windows Terminal

```powershell
# Open Windows Terminal as Administrator

# Install Python from python.org (if not installed)
# Download: https://www.python.org/downloads/

# Install Git from git-scm.com (if not installed)
# Download: https://git-scm.com/download/win

# Clone and setup
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Troubleshooting

### Common Issues

#### Issue: "python: command not found"

**Solution:**
- **Linux/macOS**: Use `python3` instead of `python`
- **Windows**: Reinstall Python and check "Add Python to PATH"

#### Issue: "pip: command not found"

**Solution:**
```bash
# Linux/macOS
sudo apt install python3-pip  # Debian/Ubuntu
brew install python3          # macOS

# Windows
python -m ensurepip --upgrade
```

#### Issue: "Permission denied" when installing packages

**Solution:**
- Ensure virtual environment is activated
- Never use `sudo pip` (use virtual environment instead)
- On Windows, run as Administrator only if necessary

#### Issue: Virtual environment activation doesn't work

**Solution (Linux/macOS):**
```bash
# Try with explicit path
source ./venv/bin/activate

# Or use
. venv/bin/activate
```

**Solution (Windows PowerShell):**
```powershell
# Enable scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

#### Issue: NumPy or SciPy installation fails

**Solution (Linux):**
```bash
# Install development headers
sudo apt install python3-dev build-essential

# Or install from system packages
sudo apt install python3-numpy python3-scipy
```

**Solution (Windows):**
- Ensure you have Visual C++ Build Tools installed
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### Issue: Streamlit port already in use

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502

# Or kill the process using port 8501
# Linux/macOS
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

#### Issue: Module not found after installation

**Solution:**
```bash
# Verify virtual environment is activated
which python  # Linux/macOS
where python  # Windows

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Clear cache if needed
pip cache purge
```

### Dependency Conflicts

If you encounter dependency conflicts:

```bash
# Create a fresh virtual environment
deactivate  # If currently activated
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Recreate and install
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### Python Version Issues

If you have multiple Python versions:

```bash
# Linux/macOS - Specify Python version
python3.11 -m venv venv
source venv/bin/activate

# Windows - Specify Python version
py -3.11 -m venv venv
venv\Scripts\activate
```

## Verification

### Verify Installation

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Run test suite
python test_suite.py

# Run example calculations
python examples.py

# Check installed packages
pip list | grep -E "streamlit|numpy|pandas|plotly|scipy"
```

### Expected Output

```
[TEST] Testing HydraulicCalculator...
  [OK] Reynolds number calculation OK
  [OK] Velocity calculation OK
  [OK] Friction factor calculation OK
  [OK] Head loss calculation OK
  [OK] Pressure conversions OK
[OK] HydraulicCalculator: All tests passed!

[TEST] Testing PumpCalculator...
  [OK] Hydraulic power calculation OK
  [OK] Shaft power calculation OK
  [OK] NPSH calculation OK
  [OK] Specific speed calculation OK
  [OK] Affinity laws OK
  [OK] Pump classification OK
[OK] PumpCalculator: All tests passed!

[TEST] Testing Standards...
  [OK] Velocity check OK
  [OK] Reynolds check OK
  [OK] Pressure class selection OK
  [OK] Pipe size selection OK
  [OK] Erosion check OK
  [OK] Standards list OK
[OK] Standards: All tests passed!

[TEST] Testing System Integration...
  [OK] System integration OK
[OK] System Integration: All tests passed!

============================================================
  [OK] ALL TESTS PASSED SUCCESSFULLY!
============================================================
```

### Verify Streamlit

```bash
# Start application
streamlit run app.py

# Should see:
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://YOUR_IP:8501
```

### Application Check

Once the application opens in your browser:

1. **Interface Check**: Verify all tabs are visible
   - Pipe Calculation
   - Pump Calculation
   - Complete System
   - Visualizations
   - Calculation Report

2. **Quick Calculation Test**:
   - Go to "Pipe Calculation" tab
   - Enter sample values
   - Click "Calculate"
   - Verify results are displayed

3. **Visualization Check**:
   - Go to "Visualizations" tab
   - Verify graphs render correctly
   - Check dark theme is applied

## Additional Configuration

### Streamlit Configuration

Edit `.streamlit/config.toml` for customization:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Environment Variables

Create `.env` file for custom settings (optional):

```bash
# .env file
STREAMLIT_SERVER_PORT=8501
PYTHON_ENV=development
```

## Uninstallation

To remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
rm -rf pump-calculator  # Linux/macOS
rmdir /s pump-calculator  # Windows
```

## Getting Help

If you continue to experience issues:

1. **Check GitHub Issues**: https://github.com/your-username/pump-calculator/issues
2. **Review Documentation**: See README.md
3. **Create New Issue**: Provide details about your system and error messages
4. **Community Discussion**: Use GitHub Discussions for questions

## Next Steps

After successful installation:

1. **Read Documentation**: Review README.md for features and usage
2. **Run Examples**: Execute `python examples.py` to see usage patterns
3. **Explore Interface**: Try different calculations in the Streamlit app
4. **Review Standards**: Familiarize yourself with the engineering standards used
5. **Contribute**: See CONTRIBUTING.md if you want to contribute

---

**Last Updated:** February 2026  
**Version:** 1.0  
**For Additional Help:** https://github.com/your-username/pump-calculator/issues
