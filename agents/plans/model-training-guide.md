# Model Training Guide for Stanza

## Table of Contents

1. [Getting Started](#getting-started)
2. [Training Pipeline Overview](#training-pipeline-overview)
3. [Preparing Training Data](#preparing-training-data)
4. [Training Different Models](#training-different-models)
5. [Advanced Topics](#advanced-topics)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [Resources](#resources)

## Getting Started

### Installation for Training

Install Stanza with training dependencies:

```bash
# From source with all dependencies
git clone https://github.com/stanfordnlp/stanza.git
cd stanza
pip install -e ".[dev,test,transformers]"

# Or with just
just install-all
```

### Verify Installation

```bash
python -c "import stanza; print(stanza.__version__)"
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
```

## Training Pipeline Overview

### Architecture

Stanza training pipeline consists of:

```
Data (CoNLL-U format)
    ↓
Preprocessing & Batching (TokensDataset)
    ↓
Model (Neural network with pretrained embeddings)
    ↓
Training Loop (Trainer class)
    ↓
Validation & Checkpointing
    ↓
Saved Model
```

### Key Components

1. Data: CoNLL-U formatted training files
2. Trainer: Main training orchestrator
3. Model: Task-specific neural model (e.g., Tagger, Parser, Classifier)
4. Pretrain: Word embeddings and character language models
5. Resources: Pretrained models and vocabularies

## Preparing Training Data

### Data Format

Stanza uses CoNLL-U format (https://universaldependencies.org/format.html):

```conllu
# sent_id = 1
# text = They buy.
1	They	they	PRON	PRP	Case=Nom|Number=Plur	2	nsubj	_	_
2	buy	buy	VERB	VBP	Number=Plur|Person=3|Tense=Pres	0	root	_	_
3	.	.	PUNCT	.	_	2	punct	_	_

```

### Data Validation

```python
from stanza.models.common import doc

def validate_data(conllu_file):
    """Validate CoNLL-U format"""
    with open(conllu_file, 'r', encoding='utf-8') as f:
        doc_list = doc.load_conll(f)
    
    print(f"Loaded {len(doc_list)} sentences")
    for i, d in enumerate(doc_list[:3]):
        print(f"Sentence {i}: {len(d.tokens)} tokens")
    
    return doc_list

# Usage
docs = validate_data('path/to/data.conllu')
```

### Train/Dev/Test Split

```python
import random
from pathlib import Path

def split_data(input_file, train_ratio=0.8, dev_ratio=0.1):
    """Split CoNLL-U data into train/dev/test"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newline (sentence separator)
    sentences = content.split('\n\n')
    sentences = [s for s in sentences if s.strip()]
    
    random.shuffle(sentences)
    
    n = len(sentences)
    train_n = int(n * train_ratio)
    dev_n = int(n * dev_ratio)
    
    base = Path(input_file).stem
    
    # Write splits
    with open(f'{base}.train.conllu', 'w') as f:
        f.write('\n\n'.join(sentences[:train_n]) + '\n\n')
    
    with open(f'{base}.dev.conllu', 'w') as f:
        f.write('\n\n'.join(sentences[train_n:train_n+dev_n]) + '\n\n')
    
    with open(f'{base}.test.conllu', 'w') as f:
        f.write('\n\n'.join(sentences[train_n+dev_n:]) + '\n\n')

# Usage
split_data('data.conllu', train_ratio=0.8, dev_ratio=0.1)
```

## Training Different Models

### 1. POS Tagger Training

```bash
cd stanza/models/pos

python train.py \
  --train_file path/to/data.train.conllu \
  --dev_file path/to/data.dev.conllu \
  --save_dir ./models \
  --save_name pos_model.pt \
  --max_epochs 10 \
  --batch_size 32
```

Python API:

```python
from stanza.models.pos import trainer

args = [
    '--train_file', 'path/to/data.train.conllu',
    '--dev_file', 'path/to/data.dev.conllu',
    '--save_dir', './models',
    '--save_name', 'pos_model.pt',
    '--max_epochs', '10',
    '--batch_size', '32',
]

trainer.main(trainer.parse_args(args))
```

### 2. Dependency Parser Training

```bash
cd stanza/models/depparse

python train.py \
  --train_file path/to/data.train.conllu \
  --dev_file path/to/data.dev.conllu \
  --save_dir ./models \
  --save_name parser.pt \
  --max_epochs 10 \
  --batch_size 32 \
  --lstm_hidden_dim 200 \
  --lstm_layers 2
```

### 3. Named Entity Recognizer (NER) Training

```bash
cd stanza/models/ner

python train.py \
  --train_file path/to/data.train.bio \
  --dev_file path/to/data.dev.bio \
  --save_dir ./models \
  --save_name ner_model.pt \
  --max_epochs 10
```

BIOES format example:

```
they	O
buy	O
medicine	B-PRODUCT
.	O
```

### 4. Lemmatizer Training

```bash
cd stanza/models/lemma

python train.py \
  --train_file path/to/data.train.conllu \
  --dev_file path/to/data.dev.conllu \
  --save_dir ./models \
  --save_name lemma_model.pt
```

### 5. Transformer-Based Classifier

```python
from stanza.models.classifiers.trainer import Trainer
from stanza.models.classifiers import data

args = [
    '--train_file', 'path/to/train.txt',
    '--dev_file', 'path/to/dev.txt',
    '--save_dir', './models',
    '--save_name', 'classifier.pt',
    '--bert_model', 'distilbert-base-uncased',
    '--max_epochs', '5',
    '--batch_size', '16',
]

args = parse_args(args)
train_set = data.read_dataset(args.train_file)
trainer = Trainer.build_new_model(args, train_set)
# Train...
```

## Advanced Topics

### Using Pretrained Embeddings

```bash
python train.py \
  --train_file data.train.conllu \
  --dev_file data.dev.conllu \
  --save_dir ./models \
  --pretrain_file path/to/pretrained_embeddings.txt \
  --max_epochs 10
```

Embedding file format (word2vec text format):

```
vocab_size embedding_dim
word1 -0.123 0.456 0.789 ...
word2 -0.321 0.654 0.987 ...
```

### Character Language Models

Stanza can use bidirectional character language models (CharLM):

```bash
python train.py \
  --train_file data.train.conllu \
  --dev_file data.dev.conllu \
  --save_dir ./models \
  --forward_charlm path/to/forward.charlm \
  --backward_charlm path/to/backward.charlm
```

### Transfer Learning

Load a pretrained model and fine-tune:

```python
from stanza.models.pos.trainer import Trainer

# Load existing model
trainer = Trainer.load(checkpoint_file='models/pos_model.pt.best')

# Update training parameters
trainer.args.max_epochs = 5
trainer.args.learning_rate = 0.0001

# Continue training
trainer.train(train_set, dev_set)
```

### Hyperparameter Tuning

```python
from stanza.models.pos import trainer
import itertools

# Grid search
learning_rates = [0.001, 0.0005, 0.0001]
hidden_dims = [100, 200, 300]
batch_sizes = [16, 32, 64]

results = []

for lr, hidden, batch in itertools.product(learning_rates, hidden_dims, batch_sizes):
    args = [
        '--train_file', 'data.train.conllu',
        '--dev_file', 'data.dev.conllu',
        '--learning_rate', str(lr),
        '--hidden_dim', str(hidden),
        '--batch_size', str(batch),
    ]
    
    parsed_args = trainer.parse_args(args)
    dev_f1, dev_acc = trainer.train(parsed_args)
    
    results.append({
        'lr': lr, 
        'hidden': hidden, 
        'batch': batch,
        'f1': dev_f1,
        'acc': dev_acc
    })

# Find best result
best = max(results, key=lambda x: x['f1'])
print(f"Best: LR={best['lr']}, Hidden={best['hidden']}, Batch={best['batch']}")
```

## Troubleshooting

### Out of Memory (OOM)

```bash
# Reduce batch size
python train.py --batch_size 8 ...

# Reduce model size
python train.py --hidden_dim 100 ...

# Use gradient accumulation (if supported)
python train.py --gradient_accumulation_steps 4 ...
```

### NaN Loss

Indicate learning rate too high or unstable input:

```bash
# Lower learning rate
python train.py --learning_rate 0.0001 ...

# Add gradient clipping
python train.py --grad_max_norm 1.0 ...
```

### Poor Results

1. Check data quality
2. Verify CoNLL-U format
3. Increase training epochs
4. Try different architecture
5. Use pretrained embeddings

### CUDA/GPU Issues

```bash
# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Force CPU training
CUDA_VISIBLE_DEVICES="" python train.py ...

# Use specific GPU
CUDA_VISIBLE_DEVICES=0 python train.py ...
```

## Best Practices

### 1. Data Quality

- Clean and normalize data
- Remove duplicate sentences
- Check for encoding issues (UTF-8)
- Validate annotation consistency
- Use large enough dataset (minimum 500-1000 sentences)

### 2. Experiment Tracking

```python
import json
from datetime import datetime

def log_experiment(model_type, args, results):
    """Log training experiment"""
    log = {
        'timestamp': datetime.now().isoformat(),
        'model': model_type,
        'args': args,
        'results': results,
    }
    
    with open('experiments.jsonl', 'a') as f:
        f.write(json.dumps(log) + '\n')

# Usage
log_experiment('pos_tagger', vars(parsed_args), {
    'dev_f1': 0.92,
    'test_f1': 0.90,
    'dev_acc': 0.94,
})
```

### 3. Model Validation

```python
def evaluate_model(model_path, test_file):
    """Evaluate model on test data"""
    import stanza
    
    # Load custom model
    nlp = stanza.Pipeline(
        'en',
        processors='tokenize,pos',
        pos_model_path=model_path,
    )
    
    # Evaluate on test file
    with open(test_file) as f:
        docs = stanza.doc.load_conll(f)
    
    metrics = nlp.models.pos.trainer.evaluate(docs)
    return metrics
```

### 4. Versioning

```bash
# Tag model versions
git tag -a models/pos_v1.0 -m "POS tagger v1.0 trained on universal dependencies"

# Store hyperparameters
cat > models/pos_v1.0_config.json << EOF
{
  "hidden_dim": 200,
  "lstm_layers": 2,
  "learning_rate": 0.001,
  "max_epochs": 10
}
EOF
```

### 5. Reproducibility

```python
import random
import torch
import numpy as np

def set_seed(seed=42):
    """Set random seed for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

# Run at start of training script
set_seed(42)
```

## Resources

### Official Documentation

- Stanza Training: https://stanfordnlp.github.io/stanza/training.html
- Universal Dependencies: https://universaldependencies.org/format.html
- CoNLL-U Format: https://universaldependencies.org/format.html

### Papers

- Qi et al. (2020): Stanza: A Python NLP Library
  https://arxiv.org/abs/2003.07082

- Dozat & Manning (2017): Deep Biaffine Attention for Dependency Parsing
  https://arxiv.org/abs/1611.02174

### Related Tutorials

- PyTorch Training Loops: https://pytorch.org/tutorials/
- Universal Dependencies Trees: https://universaldependencies.org/
- Word Embeddings: https://arxiv.org/abs/1301.3781

### Community

- GitHub Issues: https://github.com/stanfordnlp/stanza/issues
- Discussions: https://github.com/stanfordnlp/stanza/discussions
- Contributing: [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Example: Complete Training Workflow

```bash
#!/bin/bash
# Complete training pipeline

set -e

# 1. Data preparation
python scripts/split_data.py data.conllu --train 0.8 --dev 0.1

# 2. Install dependencies
pip install -e ".[dev,test]"

# 3. Train model
cd stanza/models/pos
python train.py \
  --train_file ../../../data.train.conllu \
  --dev_file ../../../data.dev.conllu \
  --save_dir ./trained_models \
  --save_name pos_model.pt \
  --max_epochs 10 \
  --batch_size 32 \
  --learning_rate 0.001

# 4. Evaluate
python -c "
import stanza
nlp = stanza.Pipeline('en', pos_model_path='trained_models/pos_model.pt.best')
# Test inference
doc = nlp('They buy medicine.')
for token in doc.sentences[0].tokens:
    print(f'{token.text}: {token.pos}')
"

echo "✓ Training complete"
```

---

Next Steps:

1. Choose a task to train (POS, NER, Parser, etc.)
2. Prepare your CoNLL-U formatted data
3. Run training with appropriate hyperparameters
4. Evaluate on test set
5. Iterate on hyperparameters based on results
6. Save best model and document configuration

Questions? Check [CONTRIBUTING.md](../../CONTRIBUTING.md) or open an issue on GitHub.
