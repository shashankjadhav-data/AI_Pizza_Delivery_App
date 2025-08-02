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
| Component        | Technology        |
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
### macOS Setup:

1. **Install Homebrew:**:
   ```bash
   winget /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
2. **Install Dependencies:**:
   ```bash
   winget brew install python ollama
   winget ollama pull mistral:7b
   winget pip3 install flask requests

## Running the App 🚀
1. **Start AI Service (Terminal 1):**:
   ```bash
   winget ollama serve
2. **Run Flask App (Terminal 2):**:
   ```bash
   winget python app.py
3. **Access Interface:**:
   ```Open browser and go to
   winget (http://localhost:5001)

## Project Structure 📂
AI_Pizza_Delivery_App/

          ├── app.py # Main Flask application
          
          ├── templates/
          │ └── index.html # Chat interface HTML
          ├── run.py # Optional script to run the app
          ├── requirements.txt # Python dependencies
          ├── flowchart.png # Mermaid flowchart
          ├── Report and Presentation # Project report and the presentation
          ├── LICENSE # MIT License
          ├── Screenshots/ # Sample output screenshots
          ├── Screen Recording/ # Sample output video
          └── README.md # This document
## Development Team 👥
| Name	                       | Contribution Area               |
|------------------------------|-----------------------------|
| Shashank Valmik Jadhav	     | Backend Architecture with AI Integration        |
|  Ajaz Sayed	                 | Prompt                       |
| Asit Ravindra Dhage	         | Frontend Development        |
| Om Shivale                   | Testing & Validation        |

    
## Usage Guide 📋
1. **Initiate Order**
2. **Customization** :
- Choose Pizza type
- Choose Pizza Size
- Choose Top[pings
- Choose Special Instructions
- Type Address
       
4. **Confirm the order (Yes/No)**
## Interface Features
- Tabbed View: Toggle between order summary and raw JSON
- Order Summary: Itemized pricing with total
- Manual Confirm: Alternative confirmation button

## Support ❓
- Check your Python Version
- Check the dependencies
- Check Ollama Server is running or not
- Check for the port conflicts: 
          winget lsof -i :5001
## MIT License - See LICENSE for full text in the github repo.
