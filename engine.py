import nltk
import numpy as np
from parseFiles import *
import testVectors
import collections


#parse the file using 
bible: dict = {**parse_bible(), **parse_bom()}
    

# Create an empty inverted index
inverted_index = collections.defaultdict(list)

# Loop through all the verses in the Bible
def get_inverted_index():
    for book_name, book in bible.items():
        for chapter_num, chapter in book.items():
            for verse_num, verse in enumerate(chapter, start=1):
                # Tokenize the verse
                tokens = nltk.word_tokenize(verse)
                # Add each token to the inverted index
                for token in tokens:
                    inverted_index[token.lower()].append((book_name, chapter_num, verse_num))
    return inverted_index
                
                
'''
Calculates score based off of word count
'''
def search_inverted_index(query, inverted_index, bible, n=10):
    """
    Returns the top n search results for a given query using the given inverted index and bible.
    """
    # Tokenize the query and remove stop words
    query_tokens = [word.lower() for word in nltk.word_tokenize(query) if word.lower() not in stopwords]

    # Create a set of all the document IDs that contain any of the query terms
    doc_ids = set()
    for token in query_tokens:
        if token in inverted_index:
            # Append all the document IDs that contain the current token
            doc_ids.update(inverted_index[token])

    # Compute the score for each document that contains at least one query term
    scores = {}
    for doc_id in doc_ids:
        doc_score = 0
        for token in query_tokens:
            if token in inverted_index and (doc_id in inverted_index[token]):
                # Increase the score by the frequency of the token in the document
                doc_score += inverted_index[token].count(doc_id)
        scores[doc_id] = doc_score
            

    # Return the top n results sorted by score
    top_n_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]

    # Format the search results as strings
    results_strings = []
    '''for result in top_n_results:
        book, chapter, verse = result[0]
        verse_text = bible[book][chapter][verse-1]
        results_strings.append(f"{book} {chapter}:{verse} {verse_text}")'''
    for (book, chapter, verse_num), _ in top_n_results:
        results_strings.append((book, chapter, verse_num))
    return results_strings

'''
Bassicly the same as search_invert_index but it uses word_embeddings, idrk
'''
def search_inverted_index_similar(query: str, inverted_index, bible, word_embeddings, n=10):
    """
    Returns the top n search results for a given query using the given inverted index and bible.
    """
    # Tokenize the query and remove stop words
    query_tokens = [word.lower() for word in nltk.word_tokenize(query) if word.lower() not in stopwords]

    # Create a set of all the document IDs that contain any of the query terms
    doc_ids = set()
    for token in query_tokens:
        if token in inverted_index:
            # Append all the document IDs that contain the current token
            doc_ids.update(inverted_index[token])

    # Compute the cosine similarity between the query vector and each document vector that contains at least one query term
    scores = {}
    for doc_id in doc_ids:
        doc_vec = np.zeros(len(word_embeddings["the"])) # Initialize a zero vector
        for token in bible[doc_id[0]][doc_id[1]][doc_id[2]-1]:
            if token in word_embeddings:
                # Add the word vector to the document vector
                doc_vec += word_embeddings[token]
        doc_vec /= len(bible[doc_id[0]][doc_id[1]][doc_id[2]-1]) # Average the document vector over its length
        query_vec = np.zeros(len(word_embeddings["the"])) # Initialize a zero vector
        for token in query_tokens:
            if token in word_embeddings:
                # Add the word vector to the query vector
                query_vec += word_embeddings[token]
        query_vec /= len(query_tokens) # Average the query vector over its length
        score = np.dot(query_vec, doc_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)) # Compute cosine similarity
        scores[doc_id] = score

    # Return the top n results sorted by score
    top_n_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]

    # Format the search results as strings
    results_strings = []
    for result in top_n_results:
        book, chapter, verse = result[0]
        verse_text = bible[book][chapter][verse-1]
        
        r_string = ""
        if verse-2 >= 0:
            r_string += f"{book} {chapter}:{verse} {bible[book][chapter][verse-2]}\n"
            
        r_string += f"{book} {chapter}:{verse} {verse_text}"
        
        if verse < len(bible[book][chapter]):
            r_string += f"\n{book} {chapter}:{verse} {bible[book][chapter][verse]}"
        
        
        results_strings.append(r_string)
    
    return results_strings

'''
Formats verses
returns a list of results
each element formated as so: [previous verse, verse, next verse]
'''
def format_verse(results: list):
    results_strings = []
    for book, chapter, verse in results:
        verse_text = bible[book][chapter][verse-1]
        
        r_string = ""
        if verse-1 >= 0:
            r_string += f"{book} {chapter}:{verse-1} {bible[book][chapter][verse-2]}\n"
            
        r_string += f"{book} {chapter}:{verse} {verse_text}\n"
        
        if verse < len(bible[book][chapter]):
            r_string += f"{book} {chapter}:{verse+1} {bible[book][chapter][verse]}\n"
        
        
        results_strings.append(r_string)  
    return results_strings  


def main(query: str) -> None:
    results = testVectors.calculate_most_similar_n(bible, query)

    results = format_verse(results)
    with open('output.txt', 'w', encoding='utf-8') as f:
        for result in results:
            #print(result)
            f.write(f'{result}\n\n')
            
            
if __name__ == "__main__":
    q = input("What is your question: ")
    while q != "q":
        main(q)
        q = input("What is your question: ")

    

