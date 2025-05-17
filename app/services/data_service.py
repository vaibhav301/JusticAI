import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from sklearn.model_selection import train_test_split
import json
import os
from datetime import datetime

class DataService:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.raw_data_path = os.path.join(data_dir, 'raw')
        self.processed_data_path = os.path.join(data_dir, 'processed')
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.raw_data_path, exist_ok=True)
        os.makedirs(self.processed_data_path, exist_ok=True)
        
    def prepare_training_data(self, cases: List[Dict]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Prepare training data from case records."""
        # Convert cases to DataFrame
        df = pd.DataFrame(cases)
        
        # Clean and preprocess text
        df['processed_text'] = df['description'].apply(self._preprocess_text)
        
        # Convert verdicts to numerical labels
        verdict_map = {"Guilty": 0, "Not Guilty": 1, "Inconclusive": 2}
        df['label'] = df['verdict'].map(verdict_map)
        
        # Check if we have enough samples per class for stratification
        label_counts = df['label'].value_counts()
        can_stratify = all(count >= 2 for count in label_counts)
        n_classes = len(label_counts)
        test_size = max(int(0.2 * len(df)), n_classes) if can_stratify else int(0.2 * len(df))
        if test_size >= len(df):
            test_size = n_classes
        
        # Split into training and validation sets
        if can_stratify:
            train_df, val_df = train_test_split(
                df, 
                test_size=test_size, 
                random_state=42,
                stratify=df['label']
            )
        else:
            print("Warning: Some classes have fewer than 2 samples. Proceeding without stratification.")
            train_df, val_df = train_test_split(
                df, 
                test_size=test_size, 
                random_state=42
            )
        
        return train_df, val_df
    
    def save_training_data(self, train_df: pd.DataFrame, val_df: pd.DataFrame):
        """Save processed training data."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        train_df.to_csv(
            os.path.join(self.processed_data_path, f'train_{timestamp}.csv'),
            index=False
        )
        val_df.to_csv(
            os.path.join(self.processed_data_path, f'val_{timestamp}.csv'),
            index=False
        )
        
    def load_training_data(self, timestamp: str = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load the most recent or specified training data."""
        if timestamp is None:
            # Get most recent files
            train_files = [f for f in os.listdir(self.processed_data_path) if f.startswith('train_')]
            if not train_files:
                raise FileNotFoundError("No training data found")
            timestamp = sorted(train_files)[-1].split('_')[1].split('.')[0]
            
        train_df = pd.read_csv(
            os.path.join(self.processed_data_path, f'train_{timestamp}.csv')
        )
        val_df = pd.read_csv(
            os.path.join(self.processed_data_path, f'val_{timestamp}.csv')
        )
        
        return train_df, val_df
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text data."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def export_model_data(self, cases: List[Dict], format: str = 'json'):
        """Export case data for model training."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'json':
            output_path = os.path.join(self.raw_data_path, f'cases_{timestamp}.json')
            with open(output_path, 'w') as f:
                json.dump(cases, f, indent=2)
        elif format == 'csv':
            output_path = os.path.join(self.raw_data_path, f'cases_{timestamp}.csv')
            pd.DataFrame(cases).to_csv(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        return output_path
    
    def get_data_statistics(self, cases: List[Dict]) -> Dict:
        """Generate statistics about the case data."""
        df = pd.DataFrame(cases)
        
        stats = {
            'total_cases': len(cases),
            'verdict_distribution': df['verdict'].value_counts().to_dict(),
            'case_types': df['case_type'].value_counts().to_dict(),
            'avg_confidence': df['confidence_score'].mean(),
            'date_range': {
                'start': df['filing_date'].min(),
                'end': df['filing_date'].max()
            }
        }
        
        return stats 