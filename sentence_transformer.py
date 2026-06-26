from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# LLM model downloaded in ~/.cache/huggingface/
model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)
titles = []
vecs = model.encode(titles)
score = cos_sim(vecs[0], vecs[1]).item()