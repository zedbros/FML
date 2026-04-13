# PyTorch: see Episode 0
import torch
# Neural Network module - provides building blocks for neural networks
import torch.nn as nn
# Functional API - contains activation functions, loss functions, etc.
from torch.nn import functional as F

# Hyperparameters 
# ML-Theorie Seite 120: we choose these manually or through hyperparameter search (GridSearch, RandomizedSearch)
batch_size = 16 # how many independent sequences will we process in parallel?
block_size = 32 # what is the maximum context length for predictions?
# ML-Theorie Seite 58: max_iters controls how many gradient descent update steps we perform
max_iters = 5000
eval_interval = 100
# ML-Theorie Seite 58: learning_rate controls step size in gradient descent
learning_rate = 1e-3
device = 'cuda' if torch.cuda.is_available() else 'cpu'  # CUDA is a proprietary technology for NVIDIA GPUs to accelerate computation
eval_iters = 200# ML-Theorie Seite 119: n_embd, n_head, n_layer are all hyperparameters defining network architecture
n_embd = 64  # embedding dimension
n_head = 4  # number of attention heads
n_layer = 4  # number of transformer blocks
# ML-Theorie Seite 107-109: dropout is a regularization technique to prevent overfitting
dropout = 0.0


# Set random seed for reproducibility
torch.manual_seed(1337)

# Load the text file, containing Shakespeare's plays. Approx 1M characters.
# wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# here are all the unique characters that occur in this text
chars = sorted(list(set(text)))
vocab_size = len(chars)
# ML-Theorie Seite 65: Encoding - representing information in machine-friendly form
# ML-Theorie Seite 67: This is similar to Ordinal-Encoding - mapping categories to integers (0 to n-1)
# create a mapping from characters to integers
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string

# Train and test splits
# ML-Theorie Seite 88: Hold-out Cross Validation - splitting data into training and validation sets
# ML-Theorie Seite 94: Training data for learning, Validation data for evaluating generalization
data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9*len(data)) # first 90% will be train, rest val
train_data = data[:n]
val_data = data[n:]

# data loading
def get_batch(split):
    # generate a small batch of data of inputs x and targets y
    data = train_data if split == 'train' else val_data
    # Randomly sample starting positions for batch_size sequences
    ix = torch.randint(len(data) - block_size, (batch_size,))
    # x: input sequences of length block_size
    x = torch.stack([data[i:i+block_size] for i in ix])
    # y: target sequences (shifted by 1) - predicting next token
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    # Move data to GPU/CPU device
    x, y = x.to(device), y.to(device)
    return x, y

# ML-Theorie Seite 58: @torch.no_grad() disables gradient computation - not updating parameters here, only evaluating
@torch.no_grad()
def estimate_loss():
    out = {}
    # Set model to evaluation mode (disables dropout, etc.)
    model.eval()
    # Evaluate on both training and validation data
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            # ML-Theorie Seite 46: logits are model outputs before softmax, loss is the cost function value
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        # ML-Theorie Seite 44: Computing mean loss across multiple batches
        out[split] = losses.mean()
    # Set model back to training mode
    model.train()
    return out

class Head(nn.Module):
    """ one head of self-attention """

    def __init__(self, head_size):
        super().__init__()
        # ML-Theorie Seite 35: Linear layers implement weighted sums: ŷ = β₀ + β₁*x₁ + ... + βₚ*xₚ
        # ML-Theorie Seite 62: β (beta) are the learnable parameters
        # Key, Query, Value: three linear transformations for attention mechanism
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        # Register buffer (not a parameter, just a constant tensor for masking)
        # tril = lower triangular matrix - prevents attending to future tokens
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        # ML-Theorie Seite 107: Dropout is regularization to prevent overfitting (Page 86)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):  # forward pass; no need to code backpropagation here, PyTorch does it automatically
        # B = batch_size, T = sequence length (time), C = embedding dimension
        B,T,C = x.shape
        # ML-Theorie Seite 35: Apply linear transformations (weighted sums with learnable parameters β)
        k = self.key(x)   # (B,T,C)
        q = self.query(x) # (B,T,C)
        # compute attention scores ("affinities")
        # Matrix multiplication: query @ key_transposed
        # C**-0.5 is scaling factor to prevent softmax saturation
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)
        # Mask future positions (causal attention): set them to -inf before softmax
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)
        # ML-Theorie Seite 155: Softmax converts logits to probabilities that sum to 1
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        # ML-Theorie Seite 107: Apply dropout for regularization
        wei = self.dropout(wei)
        # perform the weighted aggregation of the values
        # ML-Theorie Seite 35: Another weighted sum, but weights are the attention scores
        v = self.value(x) # (B,T,C)
        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)
        return out

class MultiHeadAttention(nn.Module):
    """ multiple heads of self-attention in parallel """

    def __init__(self, num_heads, head_size):
        super().__init__()
        # Create multiple attention heads that run in parallel
        # Each head learns different attention patterns
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        # ML-Theorie Seite 35: Linear projection layer (weighted sum with learnable parameters)
        self.proj = nn.Linear(n_embd, n_embd)
        # ML-Theorie Seite 107: Dropout for regularization
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Run all heads in parallel and concatenate their outputs
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        # ML-Theorie Seite 35: Apply linear projection (another weighted sum)
        # ML-Theorie Seite 107: Apply dropout for regularization
        out = self.dropout(self.proj(out))
        return out

class FeedFoward(nn.Module):
    """ a simple linear layer followed by a non-linearity """

    def __init__(self, n_embd):
        super().__init__()
        # ML-Theorie Seite 35: Sequential composition of layers - data flows through each in order
        self.net = nn.Sequential(
            # ML-Theorie Seite 35: First linear layer (weighted sum): ŷ = β₀ + β₁*x₁ + ... + βₚ*xₚ
            # Expands dimension from n_embd to 4*n_embd
            nn.Linear(n_embd, 4 * n_embd),
            # ReLU activation function: introduces non-linearity
            # Makes the model capable of learning non-linear patterns
            nn.ReLU(),
            # ML-Theorie Seite 35: Second linear layer - projects back to n_embd dimension
            nn.Linear(4 * n_embd, n_embd),
            # ML-Theorie Seite 107: Dropout for regularization to prevent overfitting (Page 86)
            nn.Dropout(dropout),
        )

    def forward(self, x):
        # ML-Theorie Seite 35: Forward pass - apply all layers sequentially
        return self.net(x)

class Block(nn.Module):
    """ Transformer block: Combines attention (communication) and feedforward (computation) """

    def __init__(self, n_embd, n_head):
        # n_embd: embedding dimension, n_head: the number of heads we'd like
        # ML-Theorie Seite 119: These are hyperparameters of the network architecture
        super().__init__()
        head_size = n_embd // n_head
        # Multi-head self-attention layer
        self.sa = MultiHeadAttention(n_head, head_size)
        # Feed-forward network
        self.ffwd = FeedFoward(n_embd)
        # Layer normalization - normalizes inputs to have mean 0 and std 1
        # Similar to Page 112: StandardScaler, but applied per layer during training
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        # Residual connections: x = x + layer(x)
        # This is "skip connection" - helps with training deep networks
        # The "+" allows gradient to flow more easily during backpropagation
        # ML-Theorie Seite 35: LayerNorm then attention, add result to original x (residual)
        x = x + self.sa(self.ln1(x))
        # ML-Theorie Seite 35: LayerNorm then feedforward, add result to x (residual)
        x = x + self.ffwd(self.ln2(x))
        return x

class BigramLanguageModel(nn.Module):
    """ 
    Simple bigram language model: predicts next token/character based on previous token/character 
    Combines token embeddings, position embeddings, and n_layer of transformer blocks to predict next token.
    """

    def __init__(self):
        super().__init__()
        # ML-Theorie Seite 65: Embedding - representing tokens in machine-friendly numerical form
        # ML-Theorie Seite 67: Similar to encoding, but learned during training (not fixed like ordinal encoding)
        # Each token (character) gets mapped to an n_embd-dimensional vector
        # These are learnable parameters β that will be optimized (Page 62)
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        # Position embeddings - each position in sequence gets its own learned embedding
        # Allows model to know where each token is in the sequence
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        # ML-Theorie Seite 119: Stack of n_layer transformer blocks (network architecture hyperparameter)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        # ML-Theorie Seite 112: Final layer normalization (similar to StandardScaler)
        self.ln_f = nn.LayerNorm(n_embd) # final layer norm
        # ML-Theorie Seite 35: Final linear layer maps from n_embd dimensions to vocab_size (output layer)
        # Produces logits (unnormalized scores) for each possible next token
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        # idx: input token indices (B, T)
        # targets: target token indices (B, T) for computing loss
        B, T = idx.shape

        # idx and targets are both (B,T) tensor of integers
        # ML-Theorie Seite 67: Look up embeddings for each token (like an advanced ordinal encoding)
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        # Look up position embeddings for each position in sequence
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
        # ML-Theorie Seite 35: Add token and position embeddings (element-wise sum)
        x = tok_emb + pos_emb # (B,T,C)
        # Pass through all transformer blocks (attention + feedforward layers)
        x = self.blocks(x) # (B,T,C)
        # ML-Theorie Seite 112: Final layer normalization
        x = self.ln_f(x) # (B,T,C)
        # ML-Theorie Seite 35: Final linear layer produces logits (unnormalized scores)
        logits = self.lm_head(x) # (B,T,vocab_size)

        if targets is None:  # if no targets are provided, we don't compute the loss
            loss = None
        else:
            # Reshape for loss computation
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            # ML-Theorie Seite 156: Cross-Entropy loss - used for classification problems
            # ML-Theorie Seite 149: Maximum Likelihood cost function
            # ML-Theorie Seite 46: This is our cost function J(β) that we want to minimize
            # Measures how well model predictions match the actual next tokens
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):  # autoregressive generation - predicts next token based on previous tokens
        # idx is (B, T) array of indices in the current context
        # Generate max_new_tokens new tokens autoregressively (one at a time)
        for _ in range(max_new_tokens):
            # crop idx to the last block_size tokens
            # (model can only handle sequences up to block_size)
            idx_cond = idx[:, -block_size:]
            # get the predictions
            # ML-Theorie Seite 35: Forward pass through the model
            logits, loss = self(idx_cond)
            # focus only on the last time step (predicting next token)
            logits = logits[:, -1, :] # becomes (B, C)
            # ML-Theorie Seite 155: Apply softmax to convert logits to probabilities
            # ML-Theorie Seite 136: φ(z) = 1/(1+e^(-z)), softmax generalizes this to multiple classes
            # Probabilities sum to 1 and represent likelihood of each possible next token
            probs = F.softmax(logits, dim=-1) # (B, C)
            # sample from the distribution
            # Instead of always picking highest probability (greedy), sample randomly
            # This introduces diversity in generated text (temperature parameter)
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx

# Create an instance of the model
model = BigramLanguageModel()
# Move model to GPU/CPU device
m = model.to(device)
# print the number of parameters in the model
# ML-Theorie Seite 62: β (beta) are the learnable parameters that will be optimized
print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')

# create a PyTorch optimizer
# ML-Theorie Seite 58: Gradient Descent algorithm - updates parameters β^(k) = β^(k-1) - η·∇J(β^(k-1))
# AdamW is an advanced variant of gradient descent with adaptive learning rates
# ML-Theorie Seite 120: Using optimization algorithms to set learnable parameters
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

from datetime import datetime

# ML-Theorie Seite 58: Training loop - repeatedly apply gradient descent updates
# for max_iters iterations (hyperparameter)
for iter in range(max_iters):

    # every once in a while evaluate the loss on train and val sets
    if iter % eval_interval == 0 or iter == max_iters - 1:
        # ML-Theorie Seite 84: Check performance on both training and validation data
        # to detect overfitting (Page 86)
        losses = estimate_loss()
        print(f"{datetime.now()} step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

    # sample a batch of data
    # ML-Theorie Seite 22: Get inputs (xb) and targets (yb) for supervised learning
    xb, yb = get_batch('train')

    # evaluate the loss
    # ML-Theorie Seite 46: Compute cost function J(β) - measures prediction error
    logits, loss = model(xb, yb)
    # ML-Theorie Seite 58: Reset gradients before backward pass
    optimizer.zero_grad(set_to_none=True)
    # ML-Theorie Seite 58: Backpropagation - compute gradients ∇J(β) of loss w.r.t. all parameters
    # This uses the chain rule from calculus to efficiently compute partial derivatives
    loss.backward()
    # ML-Theorie Seite 58: Gradient descent step - update parameters: β^(k) = β^(k-1) - η·∇J(β^(k-1))
    # optimizer.step() applies this update using the computed gradients
    optimizer.step()

# generate from the model
# Start with empty context (just a newline character at position 0)
context = torch.zeros((1, 1), dtype=torch.long, device=device)
# ML-Theorie Seite 155: Use the trained model to generate new text
# Model applies softmax to get probabilities, samples from distribution
# ML-Theorie Seite 65: decode() converts integer tokens back to text characters
print(decode(m.generate(context, max_new_tokens=2000)[0].tolist()))


# This is nanoGPT. ChatGPT3 uses this exact architecture, just scaled up:
# - More layers (96 vs 4)
# - Larger embeddings (12288 vs 64)
# - More parameters (175B vs ~0.3M)
# - More data (internet-scale vs Shakespeare)
# - RLHF alignment (trained with human feedback)
