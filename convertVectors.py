import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors

# Download pre-trained Word2Vec embeddings (takes a few minutes)

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

def text_to_vector(text):
    # Tokenize text into words
    words = word_tokenize(text.lower())
    
    # Convert each word to its embedding vector
    vectors = [model[key] for key in model.key_to_index if key in words]
    
    # Calculate the mean of all the embedding vectors to get the text vector
    if vectors:
        vector = np.mean(vectors, axis=0)
    else:
        vector = np.zeros(300)
    
    return vector


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    similarity = dot_product / norm_product
    return similarity

print(type(text_to_vector("hello")))