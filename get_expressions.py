import spacy
from nltk import ngrams
from collections import Counter
import csv

# Step 1: Load text from file
file_path = "./Steinmeier_Speeches.txt"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Step 2: Process text with spaCy
nlp = spacy.load("de_core_news_sm")
nlp.max_length = 15_000_000  # or whatever your text length is
doc = nlp(text)

# Step 3: Lemmatize & filter for content words only
content_pos = {
    "NOUN",
    "VERB",
    "ADJ",
    "ADV",
    #"ADP" # Prepositions
}

tokens = [
    token.lemma_ # Lemmatize the token (e.g. keep the infinitive form for verbs)
    for token in doc
    if token.is_alpha # Only keep alphabetic tokens
    and not token.is_stop # Remove stop words (e.g. "und", "der")
    and token.pos_ in content_pos # Keep only content words
]

# Step 4: Extract trigrams (sequences of 3 content words)
trigrams = list(ngrams(tokens, 3))

# Step 5: Count trigram frequencies
freq = Counter(trigrams)
top_trigrams = freq.most_common(100)

# Step 6: Print top 20 trigrams
print("Top 20 frequent trigrams:\n")
for trigram, count in top_trigrams:
    print(" ".join(trigram), "-", count)

# Step 7: Save all trigrams to CSV
csv_path = "trigram_frequencies.csv"
with open(csv_path, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Trigram", "Count"])
    for trigram, count in freq.most_common():
        writer.writerow([" ".join(trigram), count])

print(f"\n✅ Trigram frequencies saved to {csv_path}")