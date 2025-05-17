# Justice AI Platform

Welcome to the Justice AI Platform! This project is a Python backend for an online justice platform that predicts verdicts based on previous case data and input text. It's designed to help legal professionals and researchers analyze case outcomes quickly and efficiently.

## What We Offer

- **Verdict Prediction:** Our platform uses a trained machine learning model to predict case verdicts. Just input a case description, and we'll tell you the likely outcome!
- **Document Analysis:** Need to understand a legal document quickly? Our system analyzes documents and extracts key insights, making your work easier.
- **Case Management:** Store and retrieve case details effortlessly. Our database keeps everything organized and accessible.
- **API Endpoints:** We provide a RESTful API for predictions, document analysis, and case history. Integrate our services into your applications seamlessly.

## How It Works

### 1. **Data Collection & Storage**
We store all case details in a SQLite database (`justice_ai.db`). Each case includes:
- Case number
- Title
- Description
- Plaintiff
- Defendant
- Verdict
- Confidence score

Our `init_db.py` script initializes the database with sample cases, so you can start right away!

### 2. **Data Processing**
Our `DataService` handles all the heavy lifting:
- **Export Data:** Raw case data is exported to `data/raw/`.
- **Preprocess Data:** We clean and tokenize the text, converting verdicts into numerical labels.
- **Split Data:** The data is split into training and validation sets for better model performance.
- **Save Processed Data:** Processed data is saved to `data/processed/`, ready for training.

### 3. **Model Training**
We use a specialized BERT model (Legal-BERT) fine-tuned on legal texts. Here's how it works:
- **Load Data:** Processed data is loaded from `data/processed/`.
- **Fine-tune Model:** Legal-BERT is trained on your case data, learning to predict verdicts accurately.
- **Save Model:** The trained model is saved to `models/legal_bert_model`, ready for predictions.

### 4. **API Endpoints**
Our Flask app (`run.py`) provides easy-to-use API endpoints:
- **`/api/predict`** (POST): Predict verdicts based on case descriptions.
- **`/api/analyze-document`** (POST): Analyze legal documents for key insights.
- **`/api/case/<case_id>`** (GET): Get details of a specific case.
- **`/api/history`** (GET): View prediction history.

### 5. **Testing**
We ensure everything works perfectly with our `test_apis.py` script:
- **Send Requests:** Sample requests are sent to the API.
- **Verify Responses:** We check that responses are correct and reliable.
- **Log Results:** Test results are logged for your review.

### 6. **Continuous Improvement**
As new cases are added, our model gets smarter:
- **Add Cases:** New cases are added to the database.
- **Retrain Model:** The model is retrained on the updated dataset.
- **Test & Deploy:** The updated model is tested and deployed, ensuring top-notch performance.

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd justice_ai
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```sh
   python init_db.py
   ```

5. **Train the model:**
   ```sh
   python train_model.py
   ```

6. **Run the API server:**
   ```sh
   python run.py
   ```

## Testing the API

Run our API tests to ensure everything is working smoothly:
```sh
python test_apis.py
```

## Upgrading the Model

Want to improve the model? Here's how:

1. **Add new cases to the database:**
   - Update `init_db.py` or use the API to insert new cases.

2. **Retrain the model:**
   ```sh
   python train_model.py
   ```

3. **Test the upgraded model:**
   ```sh
   python test_apis.py
   ```

4. **Deploy the new model:**
   - Replace the old model file in `models/legal_bert_model` with the new one.
   - Restart the Flask server:
     ```sh
     python run.py
     ```

## Automate Upgrades

Create a script (`upgrade_model.sh`) to automate the upgrade process:
```sh
#!/bin/bash

# Clear and reinitialize the database
python init_db.py

# Retrain the model
python train_model.py

# Test the API
python test_apis.py

# Restart the Flask server (if needed)
# pkill -f "python run.py"
# python run.py
```

## License

[MIT License](LICENSE)

---

We hope you find the Justice AI Platform helpful! If you have any questions or need further assistance, feel free to reach out. Happy coding! 