import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

def load_reference(path="data/reference.csv"):
    if not os.path.exists(path):
        print(f"❌ Reference file not found at {path}")
        sys.exit(1)
    return pd.read_csv(path, index_col=0)

def prompt_user_vector(n):
    prompt = f"\nPaste your vector as:\nlabel,{','.join(f'PC{i+1}' for i in range(n))}\n"
    raw = input(prompt)
    parts = [s.strip() for s in raw.split(",")]
    if len(parts) != n+1:
        print(f"❌ Got {len(parts)} values, expected {n+1}.")
        sys.exit(1)
    label = parts[0]
    try:
        vec = np.array(parts[1:], dtype=float).reshape(1, -1)
    except ValueError:
        print("❌ Coordinates must all be numbers.")
        sys.exit(1)
    return label, vec

def main():
    ref = load_reference()
    n = ref.shape[1]
    print(f"✅ Loaded {ref.shape[0]} populations with {n} PCs each.")

    label, user_vec = prompt_user_vector(n)

    sims = cosine_similarity(user_vec, ref.values)[0]
    scores = pd.Series(sims, index=ref.index).sort_values(ascending=False)

    print("\nAncestry similarity scores:")
    for pop, sc in scores.items():
        print(f" • {pop}: {sc:.4f}")

    plt.figure(figsize=(10, 5))
    scores.plot.bar()
    plt.title(f"Ancestry Similarity for '{label}'")
    plt.ylabel("Cosine similarity")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()

    os.makedirs("images", exist_ok=True)
    out_path = f"images/{label}_similarity.png"
    plt.savefig(out_path)
    print(f"\n📸 Chart saved to {out_path}\n")
    plt.show()

if __name__ == "__main__":
    main()
