import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, Any, Tuple

class MLService:
    def __init__(self, model_path: str):
        self.device = torch.device('cpu')  # Force CPU usage
        self.tokenizer = AutoTokenizer.from_pretrained('nlpaueb/legal-bert-base-uncased')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            'nlpaueb/legal-bert-base-uncased',
            num_labels=3,  # Guilty, Not Guilty, Inconclusive
            torch_dtype=torch.float32  # Use float32 for CPU
        ).to(self.device)
        
    def preprocess_text(self, text: str) -> torch.Tensor:
        """Preprocess the input text for the model."""
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=256,  # Reduced from 512
            return_tensors="pt"
        )
        return {k: v.to(self.device) for k, v in inputs.items()}
    
    def predict(self, text: str) -> Tuple[str, float]:
        """Make a prediction based on the input text."""
        inputs = self.preprocess_text(text)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            prediction = torch.argmax(probabilities, dim=1)
            confidence = probabilities[0][prediction].item()
            
        verdict_map = {0: "Guilty", 1: "Not Guilty", 2: "Inconclusive"}
        verdict = verdict_map[prediction.item()]
        
        return verdict, confidence
    
    def analyze_document(self, document_text: str) -> Dict[str, Any]:
        """Analyze a legal document and return detailed insights."""
        verdict, confidence = self.predict(document_text)
        
        # Extract key legal terms and their context
        # This is a simplified version - in production, you'd want more sophisticated analysis
        legal_terms = self._extract_legal_terms(document_text)
        
        return {
            "verdict": verdict,
            "confidence": confidence,
            "key_legal_terms": legal_terms,
            "analysis_summary": self._generate_summary(document_text)
        }
    
    def _extract_legal_terms(self, text: str) -> Dict[str, str]:
        """Extract key legal terms and their context from the text."""
        # This is a placeholder - in production, you'd want to use a proper legal term extractor
        common_terms = ["evidence", "testimony", "witness", "jurisdiction", "liability"]
        terms = {}
        
        for term in common_terms:
            if term in text.lower():
                start = text.lower().find(term)
                context = text[max(0, start-50):min(len(text), start+50)]
                terms[term] = context
                
        return terms
    
    def _generate_summary(self, text: str) -> str:
        """Generate a summary of the legal document."""
        # This is a placeholder - in production, you'd want to use a proper summarization model
        sentences = text.split('.')
        if len(sentences) > 3:
            return '. '.join(sentences[:3]) + '.'
        return text 