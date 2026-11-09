#!/usr/bin/env bash
# Render build script for backend
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data required by the app
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng')"
