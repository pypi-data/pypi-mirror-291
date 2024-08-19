[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/N8yudTb1)


# NLP2
The objective of this project is to develop an automated emotion detection pipeline and cloud application for Banijay Benelux. The application should be able to process video/audio input and classify the emotions of each sentence spoken in the video/audio. The system should be able to handle multiple users and provide secure access to the data and models.

## Requirements
- python version 3.9
- nodejs
- npm
- ffmpeg

## Static Type Checking
You can run `mypy src/` for type checking.

## Setup
### 1. Download / clone the repository

Download the pre-trained model and place it into /src/models/trained_models/
https://drive.google.com/file/d/1RdrM3tzFRCKPSp2rklbKOjZg8IhLCgev/view?usp=sharing

### 2. Install dependencies
```sh
pip install poetry

poetry install

pip install openai-whisper

python -m spacy download en_core_web_lg
```


## Usage
The package is optimized for linux system. You are expected to run the API and front end using pm2.

### Menu
```sh
python src/main.py --interactive
```

### Front end
Options 1:
```sh
./front.sh
```

Option 2
```sh
cd ./src/front/NLP2-frontend/

npm install

npm run dev
```

### API
Option 1:
```sh
./api.sh
```

Option 2:
```sh
python ./src/apientry.py
```


### Docker

Linux:
```sh
./redeploy.sh
```

Windows: Use Docker Desktop or similar to build.


## Project Structure/
```
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   └── external/
    ├── docs/
    ├── models/
    ├── notebooks/
    ├── src/
    │   ├── __init__.py
    │   ├── data/
    │   │   ├── __init__.py
    │   │   └── s2p.py
    │   ├── evaluation/
    │   │   ├── __init__.py
    │   │   └── metrics.py
    │   │   └── visualizations.py
    │   ├── features/
    │   │   ├── __init__.py
    │   │   └── feature_extraction.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   └── data_setup.py
    │   │   └── model_loading.py
    │   │   └── predict_model.py
    │   │   └── train_model.py
    │   └── utils/
    │       ├── __init__.py
    │       └── helpers.py
    │       └── common.py
    ├── tests/
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── pyproject.toml
```

## Dependencies
```
python = ">=3.9,<3.10"
pandas = "^2.2.2"
spacy = "^3.7.4"
tensorflow = "2.10.0"
tensorflow-io-gcs-filesystem = "0.31.0"
scikit-learn = "^1.4.2"
nltk = "^3.8.1"
seaborn = "^0.13.2"
matplotlib = "^3.8.4"
transformers = "4.37.2"
more-itertools = "^10.2.0"
toolz = "^0.12.1"
textblob = "^0.18.0.post0"
azureml-core = "^1.56.0"
azureml-defaults = "^1.56.0.post1"
azureml-sdk = "^1.56.0"
inquirer = "^3.2.4"
tiktoken = "0.7.0"
numba = "0.59.1"
llvmlite = "0.42.0"
networkx = "3.2.1"
sympy = "1.12.1"
accelerate = "^0.31.0"
keras = "2.10.0"
protobuf = ">=3.9.2,<3.20"
tensorboard = ">=2.10,<2.16"
tensorflow-estimator = "2.10.0"
mlflow = "^2.14.1"
azureml = "^0.2.7"
fastapi = "^0.111.0"
deep_translator = "^1.11.4"
uvicorn = "^0.30.1"
pandas-stubs = "^2.2.2.240807"
pre-commit = "^3.8.0"
pytest = "^8.3.2"
pytest-cov = "^5.0.0"
mypy = "^1.11.1"
sphinx = "^7"
flake8 = "^7.1.1"
httpx = "^0.27.0"
```
