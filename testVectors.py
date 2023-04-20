from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np

phrases = ["The dog is happy", "Finn likes hamburgers", "The dog hates me"]
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))  # use character n-grams
vectorizer.fit(phrases)  # fit vectorizer on all phrases


'''gpt'''
from transformers import AutoTokenizer, AutoModel
import torch

# Load pre-trained BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# Generate vector representation for input text
def get_text_vector(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        vector = torch.mean(outputs.last_hidden_state, dim=1)
        vector = torch.nn.functional.normalize(vector, p=2, dim=1)
    return vector
# Measure cosine similarity between two text vectors
def measure_similarity(vector1, vector2) -> float:
    #vector1 = get_text_vector(text1)
    #vector2 = get_text_vector(text2)
    similarity = cosine_similarity(vector1, vector2)
    return similarity[0][0]
''' end gpt '''



'''
takes a list of phrases
converts all of them to vecotrs
sends the vectors back in a list with corresponding indexs
'''
def make_vector(phrases: list) -> list:
    vectors = []
    print(2.1)
    c = 0
    for phrase in phrases:
        c += 1
        print(f'{c/len(phrases)*100:.2f}%')
        vector = get_text_vector(phrase)
        if vector is not None:
            vectors.append(vector.numpy())
    return vectors


'''
determines similarity between the users query and all the vecotors in list vectors
returns sorted list of the percent similarity and the index
'''
def compare_vectors(vectors, phrase_vector) -> list:
    similarity_lst = []
    for i, vector in enumerate(vectors):
        #print(i)
        #similarity = cosine_similarity(phrase_vector, vector)[0][0]
        similarity = measure_similarity(vector, phrase_vector)
        similarity_lst.append((similarity, i))
    similarity_lst.sort(reverse=True)
    return similarity_lst



'''
calculates the most similar n phrases to the query
returns n most similar
'''
def calculate_most_similar_n(bible, query, n=10) -> list:
    
    '''
    bible = {book:chapter}
    book = :{chapter: [list of verses]}
    bible[book][chapter][verse_num-1]
    '''
    phrases = []
    ids = {}
    for book in bible:
        for chapter in bible[book]:
            for i, verse in enumerate(bible[book][chapter]):
                phrases.append(verse)
                ids[verse] = (book, chapter, i)
                #print(verse)
    
    #phrases is a list of every verse
    # ids is a dictionary of every verse as a key and their 
    # book chapter and verse num as the value
    print(2)
    
    #uncommet to generate new list of vecotrs
    '''vectors = make_vector(phrases)

    # create the vector
    vs = [vector.tolist() for vector in vectors]

    # save the vector to a JSON file
    with open('vector.json', 'w') as f:
        json.dump(vs, f)
    '''
    vectors = []
    with open('vector.json', 'r') as f:
        vectors = json.load(f)

    # convert each list back to a NumPy array
    vectors = [np.array(vector) for vector in vectors]
    
    print(3)
    #new_vector = vectorizer.transform([query]).toarray()
    new_vector = get_text_vector(query).numpy()
    print(4)
    similairty_of_vectors = compare_vectors(vectors, new_vector)
    print(len(similairty_of_vectors))
    print(5)
    #top_n_verses 
    top_n_verses = []
    for i in range(min(len(similairty_of_vectors), n)):
        top_n_verses.append(similairty_of_vectors[i]) 
    
    top_n_verses = [phrases[i[1]] for i in top_n_verses]
    print(top_n_verses)
    verse_nums = []
    for i in top_n_verses:
        verse_nums.append(ids.get(i))
    
    return verse_nums
