# AI Pizza Ordering System 🍕



## Table of Contents
- [Features](#features-)
- [Technologies](#technologies-)
- [Installation](#installation-)
  - [Windows](#windows-setup)
  - [macOS](#macos-setup)
- [Running the App](#running-the-app-)
- [Project Structure](#project-structure-)
- [Development Team](#development-team-)
- [Usage Guide](#usage-guide-)
- [Conversation Flow](#conversation-flow-)
- [Support](#support-)
- [License](#license-)

## Features ✨
- **Natural Language Processing**: Chat-based interface using Mistral:7b AI
- **Customizable Orders**: 
  - 3 sizes for all pizzas (Small/Medium/Large)
  - 7 extra toppings with individual pricing
  - 5 special dietary options
- **Order Management**:
  - Real-time price calculation
  - Dual confirmation system (auto/manual)
  - JSON order export
- **Responsive Design**: Works on desktop and mobile devices

## Technologies 🛠️
| Component        | Technology          |
|-----------------|--------------------|
| Backend         | Python Flask       |
| AI Engine       | Ollama Mistral:7b  |
| Frontend        | HTML5, CSS3, JS    |
| State Management| Flask Sessions     |
| Data Format     | JSON               |

## Installation ⚙️

### Windows Setup
1. **Install Python 3.11+**:
   ```powershell
   winget install Python.Python.3.11
2. **Install Install Ollama:**:
   ```powershell
   winget curl.exe -o ollama_install.exe https://ollama.com/download/OllamaSetup.exe
   winget Start-Process -Wait ollama_install.exe
   winget $env:Path += ";$env:LOCALAPPDATA\Ollama"
3. **Download AI Model:**:
   ```powershell
   winget ollama pull mistral:7b
4. **Install Dependencies:**:
   ```powershell
   winget pip install flask requests
