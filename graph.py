from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

with open("HarryPotterFiltered.txt", "r", encoding="utf-8") as f:
    hp_filt = f.read()

with open("thehobbit.txt", "r", encoding="utf-8") as f:
    hobbit_orig = f.read()

with open("TheHobbitFiltered2.txt", "r", encoding="utf-8") as f:
    hobbit_filt = f.read()

with open("PercyJacksonFiltered.txt", "r", encoding="utf-8") as f:
    percy_filt = f.read()

hp_orig = hp_filt[:len(hp_filt)//2]
percy_orig = percy_filt[:len(percy_filt)//2]


def split_text(text, n=6):
    length = len(text) // n
    return [text[i*length:(i+1)*length] for i in range(n)]


def similarity_series(t1, t2):
    seg1 = split_text(t1)
    seg2 = split_text(t2)
    sims = []
    for a, b in zip(seg1, seg2):
        vect = TfidfVectorizer().fit_transform([a, b])
        sim = cosine_similarity(vect[0], vect[1])[0][0]
        sims.append(sim)
    return sims


hp_sim = similarity_series(hp_filt, hp_orig)
hobbit_sim = similarity_series(hobbit_filt, hobbit_orig)
percy_sim = similarity_series(percy_filt, percy_orig)


plt.figure()

plt.plot(range(1,7), hp_sim, marker='o', label='Harry Potter')
plt.plot(range(1,7), hobbit_sim, marker='o', label='Hobbit')
plt.plot(range(1,7), percy_sim, marker='o', label='Percy Jackson')

plt.xlabel("Segment")
plt.ylabel("Cosine Similarity")
plt.title("Similarity Comparison Across Texts")
plt.legend()
plt.grid()

plt.show()