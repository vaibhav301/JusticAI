import os
from app.services.data_service import DataService
from app.services.ml_service import MLService
from app.models.case import Case
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import torch
from transformers import Trainer, TrainingArguments
from datasets import Dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compute_metrics(pred):
    """Compute metrics for model evaluation."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def main():
    # Initialize services
    data_service = DataService()
    engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///justice_ai.db'))
    Session = sessionmaker(bind=engine)
    
    # Get cases from database
    session = Session()
    cases = session.query(Case).all()
    case_data = [case.to_dict() for case in cases]
    session.close()
    
    if not case_data:
        logger.error("No case data found in database")
        return
    
    # Prepare training data
    logger.info("Preparing training data...")
    train_df, val_df = data_service.prepare_training_data(case_data)
    
    # Save processed data
    data_service.save_training_data(train_df, val_df)
    
    # Convert to HuggingFace datasets
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    
    # Initialize model and tokenizer
    model_path = os.getenv('MODEL_PATH', 'models/legal_bert_model')
    ml_service = MLService(model_path)
    
    # Tokenize the datasets
    def tokenize_function(examples):
        return ml_service.tokenizer(
            examples['processed_text'],
            padding='max_length',
            truncation=True,
            max_length=256
        )
    
    train_dataset = train_dataset.map(tokenize_function, batched=True, batch_size=4)
    val_dataset = val_dataset.map(tokenize_function, batched=True, batch_size=4)
    
    # Set the format for PyTorch
    train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    val_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    
    # Prepare training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        warmup_steps=50,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=100,
        load_best_model_at_end=True,
        dataloader_num_workers=0,
        gradient_accumulation_steps=8,
        fp16=False,
        gradient_checkpointing=True,
        optim="adamw_torch",
        no_cuda=True,
        use_mps_device=False
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=ml_service.model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )
    
    # Train the model
    logger.info("Starting model training...")
    trainer.train()
    
    # Evaluate the model
    logger.info("Evaluating model...")
    metrics = trainer.evaluate()
    logger.info(f"Evaluation metrics: {metrics}")
    
    # Save the model
    logger.info("Saving model...")
    trainer.save_model(model_path)
    
    # Export training data for reference
    data_service.export_model_data(case_data, format='json')
    
    # Print data statistics
    stats = data_service.get_data_statistics(case_data)
    logger.info("Data statistics:")
    logger.info(f"Total cases: {stats['total_cases']}")
    logger.info(f"Verdict distribution: {stats['verdict_distribution']}")
    logger.info(f"Case types: {stats['case_types']}")
    logger.info(f"Average confidence: {stats['avg_confidence']:.2f}")

if __name__ == '__main__':
    main() 