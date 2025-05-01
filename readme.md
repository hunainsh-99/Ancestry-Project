# 🧬 ancestry composition demo

hey! i threw together this little Streamlit app to mess around with how PCA coordinates **approximate** ancestry mixes using non-negative least squares (NNLS). it’s totally a toy/demo—if u want real %’s (like in Vahaduo), u’d gotta run ADMIXTURE or qpAdm on your raw genotypes. but if u just wanna play in PC space, this is for u.

## what’s here

- **data/reference.csv**  
  my 25-PC reference panel (pop names × PC1…PC25)

- **data/eigenvalues.csv**  
  variance explained by each PC (used to weight the fit)

- **app.py**  
  the Streamlit app that:
  1. cleans & loads the reference  
  2. reads the eigenvalues & scales each PC by √(eigenvalue)  
  3. lets u paste any 25-dim vector  
  4. runs NNLS to pick the best mix of up to 8 pops  
  5. shows a table + bar chart of your “top 8 DNA %”

- **requirements.txt**  
  pandas, numpy, scipy, matplotlib, streamlit

## how to run

1. clone it
   ```bash
   git clone git@github.com:yourusername/ancestry-composition-demo.git
   cd ancestry-composition-demo
make a venv & install

bash
Copy
Edit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
launch

bash
Copy
Edit
streamlit run app.py
open http://localhost:8501 in ur browser

then paste a line like:

Copy
Edit
my_sample,0.073985,-0.001016,-0.110873,…,-0.006227
hit Compute Composition and see ur top 8 pops + %.

tech stack
python 3.10+

pandas & numpy for data

scipy’s nnls for the fit

streamlit for the UI

matplotlib for plotting

notes
not a replacement for ADMIXTURE/qpAdm—this is just a PCA-based demo

if u want “real” admixture % u gotta run a supervised ADMIXTURE or qpAdm workflow on your genotype data

next steps:

add an import for real ADMIXTURE .Q files

let u pick how many PCs to include

batch-mode for multiple samples

enjoy!
— Hunain Sheikh

## Project Structure

```plaintext
ancestry-composition-demo/
├── data/
│   ├── reference.csv
│   └── eigenvalues.csv
├── scripts/
│   └── plot_similarity_interactive.py
├── app.py
├── requirements.txt
└── README.md
