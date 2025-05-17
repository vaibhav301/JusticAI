from flask import Blueprint, request, jsonify
from ..services.ml_service import MLService
from ..models.case import Case
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

api = Blueprint('api', __name__)
engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///justice_ai.db'))
Session = sessionmaker(bind=engine)

ml_service = MLService(os.getenv('MODEL_PATH', 'models/legal_bert_model'))

@api.route('/predict', methods=['POST'])
def predict_verdict():
    """Endpoint for predicting verdict based on case details."""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
            
        verdict, confidence = ml_service.predict(data['description'])
        
        # Create new case record
        session = Session()
        new_case = Case(
            case_number=data.get('case_number', f'CASE-{datetime.now().strftime("%Y%m%d%H%M%S")}'),
            title=data.get('title', 'Untitled Case'),
            description=data['description'],
            plaintiff=data.get('plaintiff', 'Unknown'),
            defendant=data.get('defendant', 'Unknown'),
            case_type=data.get('case_type', 'General'),
            verdict=verdict,
            confidence_score=confidence
        )
        
        session.add(new_case)
        session.commit()
        
        response = {
            'case_id': new_case.id,
            'verdict': verdict,
            'confidence': confidence,
            'case_number': new_case.case_number
        }
        
        session.close()
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/analyze-document', methods=['POST'])
def analyze_document():
    """Endpoint for analyzing legal documents."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        # Read file content
        content = file.read().decode('utf-8')
        
        # Analyze document
        analysis = ml_service.analyze_document(content)
        
        return jsonify(analysis), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/case/<int:case_id>', methods=['GET'])
def get_case(case_id):
    """Get details of a specific case."""
    try:
        session = Session()
        case = session.query(Case).get(case_id)
        
        if not case:
            return jsonify({'error': 'Case not found'}), 404
            
        response = case.to_dict()
        session.close()
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/history', methods=['GET'])
def get_history():
    """Get prediction history."""
    try:
        session = Session()
        cases = session.query(Case).order_by(Case.created_at.desc()).limit(10).all()
        
        response = [case.to_dict() for case in cases]
        session.close()
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 