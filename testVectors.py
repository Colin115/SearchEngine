import json
import numpy as np
from parseFiles import eval_unique
from nltk.tokenize import word_tokenize
from gensim.models import KeyedVectors

# Download pre-trained Word2Vec embeddings (takes a few minutes)

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

vs = []
with open('vector_bible.json', 'r') as f:
    vs = json.load(f)

with open('vector.json', 'r') as f:
    vs += json.load(f)

'''
takes a list of phrases
converts all of them to vecotrs
sends the vectors back in a list with corresponding indexs
'''
def make_vector(phrases: list) -> list:
    vectors = []
    size = len(phrases)
    c = 0
    for phrase in phrases:
        c+=1
        print(f'{c/size*100:.2f}%')
        vectors.append(text_to_vector(phrase))
    return vectors



def text_to_vector(text) -> list:
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

'''
calculates the most similar n phrases to the query
returns n most similar

BOM starts at index = 21443 in phrases

'''
import time
def calculate_most_similar_n(bible, query, n=10, books=['bible', 'bom']) -> list:
    vectors = vs
    phrases = []
    ids = {}
    for book in bible:
        for chapter in bible[book]:
            for i, verse in enumerate(bible[book][chapter]):
                phrases.append(verse)
                ids[verse] = (book, chapter, i)


    '''
    uncomment to generate the vecotors
    
    
    vectors = make_vector(phrases)
    
    vs = [vector.tolist() for vector in vectors]
    # save the vector to a JSON file
    with open('vector_bible.json', 'w') as f:
        json.dump(vs, f)
    '''
    

    
    #seperate books
    bible_phrases = phrases[:21443]
    bible_vec = vectors[:21443]
    
    
    bom_phrases = phrases[21443:] 
    bom_vec = vectors[21443:]
    
    #change the vectors based off the books
    phrases = []
    vectors = []
    if 'bible' in books:
        phrases = bible_phrases
        vectors = bible_vec
    if 'bom' in books:
        phrases += bom_phrases
        vectors += bom_vec
    
    new_vector = make_vector([query])[0]
    
    similarity_lst = []
    t = time.time()
    for i, vector in enumerate(vectors):
        similarity = cosine_similarity(vector, new_vector) + eval_unique(query, phrases[i])
        similarity_lst.append((similarity, i))
    print(time.time()-t)
    similarity_lst.sort(key=lambda x: x[0], reverse=True)
    verse_nums = [ids[phrases[i[1]]] for i in similarity_lst[:n]]

    return verse_nums
