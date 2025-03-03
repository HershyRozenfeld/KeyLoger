# KeyLogger Pro



## 📋 Overview

KeyLogger Pro is a comprehensive keystroke monitoring solution designed for security research and educational purposes. The system consists of three main components: a lightweight client application, a robust API server, and an intuitive web interface for seamless management.


> ⚠️ **Disclaimer**: This software is intended for educational purposes, legitimate security research, and authorized monitoring only. Always obtain proper consent before deployment.


## ✨ KeyLogger Features

### 🔹 Client Application

- **Real-time Keystroke Capture**: Uses `pynput` to efficiently log keystrokes
- **Flexible Storage Options**: Send to remote server or store locally
- **Customizable Reporting**: Adjustable frequency for data transmission
- **Encryption**: XOR encryption for secure data transfer
- **Automatic Status Reporting**: Regular device status updates
- **Remote Configuration**: Supports remote management of all settings
- **Time-Limited Operation**: Optional automatic shutdown after defined period


### 🔹 API Server

- **RESTful Architecture**: Well-structured Flask-based API
- **Device Management**: Comprehensive endpoint for managing connected devices
- **Data Collection**: Secure collection and decryption of keystroke data
- **Configuration Control**: Remote device configuration management
- **Data Visualization**: Endpoints for accessing and filtering collected data
- **Time Synchronization**: Israel timezone (Asia/Jerusalem) support


### 🔹 Web Interface

- **Modern Dashboard**: Clean, intuitive device monitoring
- **Real-time Status**: Live connection status indicators
- **Granular Control**: Complete device configuration management
  - Enable/disable monitoring
  - Adjust storage location
  - Set reporting frequency
  - Configure time limits
- **Advanced Log Analysis**: Filter and sort capabilities
  - Date/time filtering
  - Application window filtering
  - Chronological sorting options
- **Security Features**: Password-protected interface
- **Responsive Design**: Matrix-inspired theme with Hebrew language support


## 🚀 Installation

### Prerequisites

- Python 3.x
- Modern web browser (Chrome, Firefox, etc.)

### Client Requirements

```bash
pip install pynput requests
```

### Server Requirements

```bash
pip install flask flask-cors pytz
```

### Deployment Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/HershyRozenfeld/Key_Logger.git
   cd Key_Logger
   ```

2. **Start the API server**

   ```bash
   python server.py
   ```

3. **Deploy the client**

   ```bash
   python key_logger_manager.py
   ```

4. **Access the web interface**
   
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```


## 🔧 Technical Architecture

### Client Architecture

```
Client
 ├── Keystroke Collector (pynput)
 ├── Data Manager
 │   ├── Memory Buffer
 │   ├── XOR Encryption Module
 │   └── Storage Manager
 ├── Communication Module
 │   ├── Status Reporter
 │   └── Configuration Manager
 └── Time Control System
```

### Server Architecture

```
Server
 ├── API Controller
 │   ├── Status Endpoints
 │   ├── Data Endpoints
 │   └── File Management Endpoints
 ├── Data Processor
 │   ├── XOR Decryption Module
 │   └── JSON Storage Manager
 └── Web Interface
     ├── Device Dashboard
     ├── Configuration Panel
     └── Log Analyzer
```


## 🛡 Security Considerations

- Current implementation uses simple XOR encryption
- Password protection for web interface
- For production environments, consider implementing:
  - Strong encryption (AES)
  - HTTPS/TLS
  - User authentication
  - Access control lists
  - Audit logging


## 📊 Data Storage

All data is stored in JSON format with UTF-8 encoding to support Hebrew and other languages:

- `device_status.json`: Real-time device status information
- `all_devices_data.json`: Collected keystroke data
- `change_device_status.json`: Pending configuration changes


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for suggestions.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.


## 👥 Credits

Developed by **Hershy Rozenfeld** & **Moyshi Fogel**

---

<div align="center">
  <sub>Built with ❤️ for educational purposes only</sub>
</div>
