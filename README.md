# Stock Trading Python App

A Python application for stock trading analysis and operations.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher installed on your system
- pip (Python package installer)

### Virtual Environment Setup

#### 1. Create a Virtual Environment
```bash
# Navigate to the project directory
cd /path/to/stock-trading-python-app

# Create a virtual environment named 'pythonenv'
python3 -m venv pythonenv
```

#### 2. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source pythonenv/bin/activate
```

**On Windows:**
```bash
# Command Prompt
pythonenv\Scripts\activate

# PowerShell
pythonenv\Scripts\Activate.ps1
```

#### 3. Install Dependencies
```bash
# Make sure you're in the activated virtual environment
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
# Check if packages are installed correctly
pip list
```

### Deactivating the Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```

### Important Notes

- Always activate the virtual environment before working on the project
- The virtual environment folder (`pythonenv/`) should be added to `.gitignore` (already included)
- Never commit the virtual environment folder to version control
- If you need to recreate the environment, delete the `pythonenv/` folder and follow the setup steps again

### Troubleshooting

If you encounter issues:
1. Make sure Python 3.8+ is installed: `python3 --version`
2. Ensure pip is up to date: `pip install --upgrade pip`
3. If activation fails, try using the full path: `source ./pythonenv/bin/activate`