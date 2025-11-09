# SWaT Intrusion Detection System

> **ML Zoomcamp 2025 Midterm Project** - Real-time intrusion detection for industrial control systems

A high-performance FastAPI web service that detects cyber-attacks in industrial water treatment systems using machine learning.

---

## 📋 Table of Contents

- [Problem Description](#problem-description)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Model Details](#model-details)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)

---

## 🎯 Problem Description

### What is SWaT?

The **Secure Water Treatment (SWaT)** testbed is a scaled-down replica of a real-world water treatment facility used for cybersecurity research. It consists of six stages that simulate the entire water treatment process, from raw water intake to final distribution.

### The Challenge

Industrial control systems are increasingly targeted by cyber attackers. These attacks can:

- Manipulate sensor readings to hide malicious activities
- Damage physical equipment by sending incorrect control commands
- Disrupt essential services affecting public health and safety

### Our Solution

This project implements a **real-time ML-based Intrusion Detection System (IDS)** that:

- Monitors **51 sensors and actuators** across all 6 stages
- Analyzes real-time snapshots using machine learning
- Classifies each snapshot as **"Normal"** or **"Attack"** with confidence scores
- Provides a REST API for easy integration with SCADA systems

### Dataset

- **Source**: SWaT dataset (merged normal + attack scenarios)
- **Size**: 1.4M+ timestamped measurements
- **Features**: 51 sensors/actuators (flow, level, pressure, water quality indicators)
- **Attack Rate**: 3.79% (realistic imbalanced distribution)

---

## 📁 Project Structure

```
.
├── src/
│   ├── train.py              # Model training script
│   └── predict.py            # FastAPI web service
├── tests/
│   └── test_client.py        # API test client
├── notebooks/
│   └── notebook.ipynb        # EDA and experimentation
├── data/
│   ├── model.bin             # Trained model (generated, not in repo)
│   ├── dv.bin                # DictVectorizer (generated, not in repo)
│   └── merged.csv            # SWaT dataset (not in repo)
├── Dockerfile                # Production container
├── docker-compose.yml        # Easy deployment
├── requirements.txt          # Production dependencies
├── pyproject.toml            # Development dependencies (uv)
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- `uv` package manager ([Install here](https://github.com/astral-sh/uv))
- Docker (optional, for containerization)

### 1. Clone and Setup

```bash
git clone https://github.com/ugurcanuzunkaya/Datatalks-ML-Zoomcamp-2025-Midterm.git
cd Datatalks-ML-Zoomcamp-2025-Midterm

# Create virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
uv pip install pandas numpy scikit-learn matplotlib seaborn jupyterlab \
               xgboost fastapi uvicorn[standard] httpx ruff imbalanced-learn
```

### 2. Train the Model

```bash
python src/train.py
```

This will create `data/model.bin` and `data/dv.bin`.

### 3. Run the API Service

```bash
uvicorn src.predict:app --host 0.0.0.0 --port 9696
```

### 4. Test the Service

```bash
python tests/test_client.py
```

---

## 💻 Usage

### API Endpoints

#### Health Check

```bash
curl http://localhost:9696/health
```

#### Predict Attack

```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  -d '{
    "FIT101": 2.6,
    "LIT101": 528.9,
    "MV101": 0.0,
    "P101": 2,
    ...
  }'
```

**Response:**

```json
{
  "attack_probability": 0.0002,
  "classification": "Normal",
  "confidence": 0.9998
}
```

### Interactive Documentation

Visit `http://localhost:9696/docs` for Swagger UI with interactive testing.

---

## 🤖 Model Details

### Architecture

- **Algorithm**: Logistic Regression
- **Features**: 51 numerical sensors/actuators
- **Preprocessing**: DictVectorizer for feature encoding
- **Class Handling**: `class_weight='balanced'` (no SMOTE)
- **Training Data**: Original 3.79% attack rate preserved

### Performance Metrics

- **Accuracy**: 94.16%
- **Precision**: 39.08%
- **Recall**: 96.99%
- **F1-Score**: 55.72%

### Why No SMOTE?

Initial experiments with SMOTE (balancing to 50% attacks) caused the model to over-predict attacks. The final model uses only `class_weight='balanced'`, preserving the real-world distribution for better generalization.

### Model Training Strategy

1. **Stratified Split**: 80/20 chronological split within each class
2. **No Synthetic Data**: Uses original 1.1M training samples
3. **Balanced Loss**: Weighted loss function handles class imbalance
4. **Regularization**: Default L2 regularization (C=1.0)

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t swat-detector .

# Run container
docker run -d -p 9696:9696 --name swat-detector-container swat-detector
```

### Using Docker Compose

```bash
# Start service
docker-compose up -d

# Stop service
docker-compose down
```

### Production Features

- **Multi-stage build** for optimized image size (538MB)
- **Health checks** built-in
- **Auto-restart** on failure
- **Non-root user** for security

---

## 📊 API Documentation

### POST `/predict`

**Request Body**: JSON object with 51 sensor readings

**Required Fields** (all numerical):

- Flow Indicators: `FIT101`, `FIT201`, `FIT301`, `FIT401`, `FIT501-504`, `FIT601`
- Level Indicators: `LIT101`, `LIT301`, `LIT401`
- Motorized Valves: `MV101`, `MV201`, `MV301-304`
- Pumps: `P101-102`, `P201-206`, `P301-302`, `P401-404`, `P501-502`, `P601-603`
- Pressure Indicators: `DPIT301`, `PIT501-503`
- Analyzers: `AIT201-203`, `AIT401-402`, `AIT501-504`
- UV Unit: `UV401`

**Response**:

```json
{
  "attack_probability": float,  // 0.0 to 1.0
  "classification": string,      // "Normal" or "Attack"
  "confidence": float            // 0.0 to 1.0
}
```

### GET `/health`

**Response**:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

## 🛠️ Development

### Code Quality

```bash
# Lint check
ruff check .

# Format code
ruff format .
```

### Run Jupyter Notebook

```bash
jupyter lab
# Open notebooks/notebook.ipynb
```

### Project Setup with uv

This project uses `uv` for fast dependency management:

```bash
# Sync all dependencies
uv sync

# Add new package
uv pip install <package>
```

---

## 📝 Technologies

- **FastAPI** - Modern web framework
- **scikit-learn** - Machine learning
- **pandas/numpy** - Data processing
- **Docker** - Containerization
- **uvicorn** - ASGI server
- **uv** - Package management
- **ruff** - Linting and formatting

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ugurcan Uzunkaya**

- GitHub: [@ugurcanuzunkaya](https://github.com/ugurcanuzunkaya)
- Project: [Datatalks-ML-Zoomcamp-2025-Midterm](https://github.com/ugurcanuzunkaya/Datatalks-ML-Zoomcamp-2025-Midterm)

---

## 🙏 Acknowledgments

- **DataTalks.Club** - ML Zoomcamp program
- **SWaT Dataset** - iTrust, Singapore University of Technology and Design
- **ML Zoomcamp Community** - Support and feedback

---

**Note**: The `merged.csv` dataset is not included in this repository. Please obtain it from the official SWaT dataset sources.
