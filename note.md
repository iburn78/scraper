# Envs
- Chrome for Testing 148.0.7778.96 (playwright chromium v1223) downloaded to /Users/andy/Library/Caches/ms-playwright/chromium-1223

<br><br>

# ollama show gemma4

### Model core
architecture (gemma4)
→ the transformer design + multimodal extensions (vision/audio/tools support)

parameters (8.0B)
→ number of learned weights (~8 billion fixed values)

context length (131072)
→ maximum tokens the model can “see” at once (prompt + history + output)

embedding length (2560)
→ size of internal vector representation per token

<br>

### Compression
quantization (Q4_K_M)
→ weights stored in compressed 4-bit format with scaling
→ reduces RAM + bandwidth usage → faster inference on local hardware

Capabilities (important correction)
completion → text generation (core function)
vision/audio → input understanding only (not generation)
tools → model can request external functions (you must implement them)
thinking → model supports reasoning mode, but not always explicitly separate unless enabled

So: capabilities are supported interfaces, not always active features.

<br>

### Sampling parameters (runtime behavior)
These control style and variability, not intelligence.
- temperature → randomness level
- top_p → probability cutoff sampling
- top_k → restrict candidate tokens

<br>

### Runtime
Model = (weights + architecture)
1. Prefill (fast parallel GPU pass over input)
- Prefill: parallel matrix operations → very fast (thousands tokens/sec)
2. KV cache creation
- storing intermediate calc values (used in a single request, many vectors per token (layer × heads × dimensions))
3. Decode loop:
- Decode (generation): sequential token-by-token → slow (tens tokens/sec)
- read weights from memory
- compute next token
- repeat (slow, sequential)