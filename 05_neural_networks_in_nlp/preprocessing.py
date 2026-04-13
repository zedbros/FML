# Text preprocessing utilities for character-level language modeling
# Handles loading Shakespeare text and creating character vocabularies

import torch


def load_text(filepath='assets/input.txt'):
    """
    Load text file and return as string.
    
    Args:
        filepath: Path to text file
        
    Returns:
        text: String containing full text content
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def build_vocabulary(text):
    """
    Build character-level vocabulary from text.
    
    Args:
        text: String of text to build vocabulary from
        
    Returns:
        chars: Sorted list of unique characters
        vocab_size: Number of unique characters
        char_to_idx: Dictionary mapping characters to indices
        idx_to_char: Dictionary mapping indices to characters
    """
    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    char_to_idx = {ch: i for i, ch in enumerate(chars)}
    idx_to_char = {i: ch for i, ch in enumerate(chars)}
    
    return chars, vocab_size, char_to_idx, idx_to_char


def encode(text, char_to_idx):
    """
    Encode string to list of character indices.
    
    Args:
        text: String to encode
        char_to_idx: Dictionary mapping characters to indices
        
    Returns:
        List of integer indices
    """
    return [char_to_idx[ch] for ch in text]


def decode(indices, idx_to_char):
    """
    Decode list of indices to string.
    
    Args:
        indices: List of integer indices
        idx_to_char: Dictionary mapping indices to characters
        
    Returns:
        String of decoded text
    """
    return ''.join([idx_to_char[i] for i in indices])


def create_sliding_window_sequences(text, char_to_idx, seq_length=25):
    """
    Create training sequences using sliding window approach.
    Pre-creates all sequences - memory intensive but simple.
    
    Used in RNN episode where we train on all sequences.
    
    Args:
        text: String of text to process
        char_to_idx: Dictionary mapping characters to indices
        seq_length: Length of input sequences
        
    Returns:
        X: Tensor of shape [num_sequences, seq_length] containing input sequences
        y: Tensor of shape [num_sequences] containing target characters
    """
    # Convert text to indices
    data = encode(text, char_to_idx)
    
    # Create sequences with sliding window
    sequences = []
    targets = []
    
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i+seq_length])
        targets.append(data[i+seq_length])
    
    X = torch.tensor(sequences, dtype=torch.long)
    y = torch.tensor(targets, dtype=torch.long)
    
    return X, y


def prepare_data_splits(text, char_to_idx, train_split=0.9):
    """
    Prepare train/validation splits as tensors.
    Memory efficient - creates indexed data only.
    
    Used in transformer/nanogpt where batches are sampled on-the-fly.
    
    Args:
        text: String of text to process
        char_to_idx: Dictionary mapping characters to indices
        train_split: Fraction of data to use for training
        
    Returns:
        train_data: Tensor of training character indices
        val_data: Tensor of validation character indices
    """
    # Convert entire text to indices
    data = torch.tensor(encode(text, char_to_idx), dtype=torch.long)
    
    # Split into train and validation
    n = int(train_split * len(data))
    train_data = data[:n]
    val_data = data[n:]
    
    return train_data, val_data


def get_batch(data, block_size, batch_size, device='cpu'):
    """
    Sample random batch of sequences from data.
    Memory efficient - generates sequences on-the-fly.
    
    Used in transformer/nanogpt for efficient training.
    
    Args:
        data: Tensor of character indices
        block_size: Length of sequences to generate
        batch_size: Number of sequences in batch
        device: Device to place tensors on ('cpu' or 'cuda')
        
    Returns:
        x: Input sequences [batch_size, block_size]
        y: Target sequences [batch_size, block_size] (shifted by 1)
    """
    # Random starting indices for sequences
    ix = torch.randint(len(data) - block_size, (batch_size,))
    
    # Extract sequences
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    
    x, y = x.to(device), y.to(device)
    return x, y


if __name__ == '__main__':

    print("Loading Shakespeare corpus...")
    text = load_text('assets/input.txt')
    print(f"Text length: {len(text):,} characters")
    print(f"\nFirst 200 characters:\n{text[:200]}")
    print(f"\nLast 200 characters:\n{text[-200:]}")
    
    print("\n" + "="*60)
    print("Building vocabulary...")
    chars, vocab_size, char_to_idx, idx_to_char = build_vocabulary(text)
    print(f"Vocabulary size: {vocab_size}")
    print(f"Characters: {''.join(chars)}")
    
    print("\n" + "="*60)
    print("Testing encode/decode...")
    test_text = "Hello, World!"
    try:
        encoded = encode(test_text, char_to_idx)
        decoded = decode(encoded, idx_to_char)
        print(f"Original: {test_text}")
        print(f"Encoded: {encoded}")
        print(f"Decoded: {decoded}")
        print(f"✓ Encode/decode working correctly: {test_text == decoded}")
    except KeyError as e:
        print(f"✗ Character not in Shakespeare corpus: {e}")
    
    print("\n" + "="*60)
    print("Method 1: Sliding window sequences (RNN approach)")
    X, y = create_sliding_window_sequences(text, char_to_idx, seq_length=25)
    print(f"Number of sequences: {len(X):,}")
    print(f"Input shape: {X.shape} [num_sequences, seq_length]")
    print(f"Target shape: {y.shape} [num_sequences]")
    print(f"\nExample:")
    print(f"Input:  '{decode(X[0].tolist(), idx_to_char)}'")
    print(f"Target: '{idx_to_char[y[0].item()]}'")
    
    print("\n" + "="*60)
    print("Method 2: On-the-fly batch sampling (Transformer approach)")
    train_data, val_data = prepare_data_splits(text, char_to_idx, train_split=0.9)
    print(f"Train data size: {len(train_data):,} characters")
    print(f"Val data size: {len(val_data):,} characters")
    
    batch_x, batch_y = get_batch(train_data, block_size=32, batch_size=4)
    print(f"\nSampled batch:")
    print(f"Input shape: {batch_x.shape} [batch_size, block_size]")
    print(f"Target shape: {batch_y.shape} [batch_size, block_size]")
    print(f"\nFirst sequence in batch:")
    print(f"Input:  '{decode(batch_x[0].tolist(), idx_to_char)}'")
    print(f"Target: '{decode(batch_y[0].tolist(), idx_to_char)}'")
    
    print("\n" + "="*60)
    print("All preprocessing functions working correctly :-)")

