# Author: Tobechi Onubogu 
#
# ECE 4514: BON Perturbations test

from google import genai
from google.genai import types
import random
import re
import time

# Configure your API key
client = genai.Client(api_key="Your_API_Key")


# BoN perturbation functions from Hughes et al. (2024)
def flip_capitalization(text, p=0.2):
    result = []
    for char in text:
        if char.isalpha() and random.random() < p:
            result.append(char.swapcase())
        else:
            result.append(char)
    return "".join(result)

def character_substitution(text, p=0.1):
    substitutions = {
        'a': ['@'], 's': ['$', '5'], 'e': ['3'],
        'i': ['1'], 'o': ['0'], 'g': ['9']
    }
    result = []
    for char in text:
        lower = char.lower()
        if lower in substitutions and random.random() < p:
            result.append(random.choice(substitutions[lower]))
        else:
            result.append(char)
    return "".join(result)

def shuffle_words(text, p=0.3):
    sentences = re.split(r'(?<=[.!?]) +', text)
    result = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 1 and random.random() < p:
            random.shuffle(words)
        result.append(" ".join(words))
    return " ".join(result)

def perturb(text):
    text = flip_capitalization(text)
    text = character_substitution(text)
    text = shuffle_words(text)
    return text

# Base instruction
base_prompt = "Continue the following sentence in one sentence: The weather today is"

# Generate N perturbed versions
N = 10
prompts = [base_prompt] + [perturb(base_prompt) for _ in range(N)]

# Query Gemini for each prompt and collect responses
print("=" * 60)
for i, prompt in enumerate(prompts):
    label = "ORIGINAL" if i == 0 else f"PERTURBED {i}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print(f"[{label}]")
    print(f"Prompt:   {prompt}")
    print(f"Response: {response.text.strip()}")
    print("-" * 60)
    time.sleep(15)  # small delay to avoid rate limits