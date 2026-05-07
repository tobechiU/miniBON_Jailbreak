# LLM Memorization Detection via Best-of-N Jailbreaking and Text Similarity

**ECE 4524 — Artificial Intelligence and Engineering Applications**  
Virginia Tech, Spring 2026

**Team:** Tobechi Onubogu · Dezman Jones · Carlos Fernandez · Arjab Sinha · Adwaith Nambiar

---

## Overview

This repository contains the implementation for our final project investigating memorization and training data leakage in large language models (LLMs). We use a Best-of-N (BoN) jailbreaking technique to elicit potentially memorized text from Gemini 2.5 Flash, then measure how closely the generated output resembles known source texts using cosine similarity over TF-IDF representations.

The project accompanies a literature review synthesizing recent work on:
- Training data extraction from LLMs (Carlini et al., 2021; Ahmed et al., 2026)
- Adversarial jailbreaking techniques (Hughes et al., 2024; Wei et al., 2023)
- Text similarity measurement (Wang & Dong, 2020)

---

## Repository Structure

```
.
├── jailbreak.py          # BoN perturbation and Gemini API querying
├── filter.py             # Output normalization (reverses glyph substitutions)
├── similarity.py         # Segment-level cosine similarity computation [to be added]
├── outputs/
│   ├── Test1Unfiltered.txt   # Raw jailbroken output (before filtering)
│   └── output.txt            # Cleaned output (after filtering)
├── results/
│   └── similarity.png        # Cosine similarity comparison graph
└── README.md
```

---

## Pipeline

The full experimental pipeline runs in four stages:

```
1. bon_perturbation.py     →    Raw LLM output (may contain mirrored perturbations)
2. normalize.py        →    Cleaned output (glyph substitutions reversed)
3. similarity.py    →    Per-segment cosine similarity scores
4. results/         →    Visualization of similarity across datasets
```

---

## Scripts

### `bon_perturbation.py`
Implements the Best-of-N (BoN) jailbreaking procedure from Hughes et al. (2024). 

The script:
- Constructs a prompt from a fixed continuation instruction (`"Continue the story verbatim"`) combined with a ground-truth seed passage from the target book
- Generates N perturbed variants of the prompt using three perturbation functions:
  - **Capitalization flips** — randomly swaps case of alphabetic characters
  - **Glyph substitutions** — replaces letters with visually similar characters (e.g. `a → @`, `s → $`)
  - **Word shuffle** — randomly reorders words within sentences
- Queries Gemini 2.5 Flash via the Google GenAI API until a compliant continuation is obtained
- In practice, compliance was typically achieved within 1–2 perturbed prompts on Gemini 2.5 Flash

**Usage:**
```bash
pip install google-genai
```
Then replace `"Your_API_Key"` on line 10 with your Gemini API key, and replace `"[Insert First Line Of Book Here]"` on line 50 with the seed passage from your target book.
```bash
python bon_perturbation.py
```

> **Note:** A free-tier Gemini API key provides approximately 20 prompts per session. Running the full N=20 budget in one session may hit rate limits; the script includes automatic backoff handling.

---

### `normalize.py`
Normalizes raw jailbroken output by reversing common glyph substitutions introduced by the perturbation process.

A known side effect of BoN-style prompt perturbation is that the model mirrors the distorted formatting back in its own output (see Hughes et al., 2024; Wei et al., 2023). For example, a prompt containing `@ → a` substitutions will often produce responses using the same substitutions. This script reverses the following mappings before similarity comparison:

| Substituted | Restored |
|-------------|----------|
| `@`         | `a`      |
| `$` or `5`  | `s`      |
| `3`         | `e`      |
| `1`         | `i`      |
| `0`         | `o`      |
| `9`         | `g`      |

**Usage:**
1. Place your raw jailbroken output in a file named `Test1Unfiltered.txt` in the same directory
2. Run:
```bash
python normalize.py
```
3. Cleaned output will be written to `output.txt`

---

### `similarity.py` *(to be added)*
Computes segment-level cosine similarity between the filtered generated output and the corresponding source text using TF-IDF vector representations. Produces the comparison graph shown in the paper (Fig. 2).

---

## Requirements

```
google-genai
scikit-learn    # for TF-IDF and cosine similarity (similarity.py)
matplotlib      # for visualization (similarity.py)
```

Install with:
```bash
pip install google-genai scikit-learn matplotlib
```

---

## Notes on Ethics and Terms of Service

- Experiments were conducted using the **free-tier Gemini API** with deliberate query limits to remain compliant with Google's Terms of Service
- Source texts used for testing (*Harry Potter and the Philosopher's Stone*, *The Hobbit*, *Percy Jackson and the Lightning Thief*) are copyrighted works used strictly for academic research purposes
- Raw extracted outputs are **not redistributed** in this repository
- This project is a research investigation into model safety, not a tool for unauthorized content extraction

---

## References

- N. Carlini et al., "Extracting training data from large language models," USENIX Security, 2021.
- A. Ahmed et al., "Extracting books from production language models," arXiv:2601.02671, 2026.
- J. Hughes et al., "Best-of-N jailbreaking," arXiv:2412.03556, 2024.
- A. Wei, N. Haghtalab, and J. Steinhardt, "Jailbroken: How does LLM safety training fail?", NeurIPS, 2023.
- J. Wang and Y. Dong, "Measurement of text similarity: A survey," Information, vol. 11, no. 9, 2020.

---

## Course

ECE 4524 — Artificial Intelligence and Engineering Applications  
Virginia Tech · Spring 2026  
Instructor: Abhijit Sarkar
