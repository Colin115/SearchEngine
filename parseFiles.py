from nltk.tokenize import word_tokenize


def parse_bom():
    
    bom = {}
    with open('BOM.txt', 'r', encoding='UTF-8' ) as f:
        book = f.read()
        books = []
        lines = book.split("\n")
        lines = list(filter(lambda x: x != "", lines))
        
        
        for i in range(len(lines)):
            if ':' in lines[i] and lines[i+1][0] == " ":
                
                b = lines[i]
                b = b.split()
                if b[0].isdigit():
                    cur_book = b[0] + " " + b[1]
                else:
                    cur_book = b[0]
                
                if cur_book not in books:
                    books.append(cur_book)
        books.append('Words of Morman')
        
        for book in books:
            #make each book have a dictionary of chapters
            bom[book] = {}
        
        cur_verse = []
        cur_book = '1 Nephi'
        cur_chapter = 1
        for i in range(len(lines)):
            if lines[i][0] == " ":
                #add old chapter to verse
                cur_verse.pop(-1)
                if bom[cur_book].get(cur_chapter) is not None:
                    bom[cur_book][cur_chapter].append(" ".join(cur_verse))
                else:
                    bom[cur_book][cur_chapter] = [" ".join(cur_verse)]
                
                cur_verse = [lines[i]]
                
                #get book and chapter
                prev_line = lines[i-1].split()
                if len(prev_line) == 3:
                    cur_book = prev_line[0] + " " + prev_line[1]
                    cur_chapter, _ = prev_line[2].split(":")
                elif 'Words' in prev_line and 'Mormon' in prev_line:
                    cur_book, cur_chapter = "Words of Morman", "1"
                else:
                    cur_book = prev_line[0]
                    cur_chapter, _ = prev_line[1].split(":")
            
            
            elif i==len(lines)-1:
                pass
            
            else:
                cur_verse.append(lines[i])
    return bom
         
def parse_bible():
    #bible = {"Ge":{}, "Exo":{}, "Lev":{}, "Num":{}, "Deu":{}, "Josh":{}, "Jdgs":{}, "Ruth":{}, "":{}, "Ezra":{}, "Neh":{}, "Est":{}, "Job":{}, "Psa":{}, "Prv":{}, "Eccl":{}, "SSol":{}, "Isa":{}, "Jer":{}, "Lam":{}, "Eze":{}, "Dan":{}, "Hos":{}, "Joel":{}, "Amos":{}, "Obad":{}, "Jonah":{}, "Mic":{}, "Nahum":{}, "Hab":{}, "Zep":{}, "Hag":{}, "Zec":{}, "Mal":{}, "Mat":{}, "Mark":{}, "Luke":{}, "John":{}, "Acts":{}, "Rom":{}, "Gal":{}, "Eph":{}, "Phi":{}, "Col":{}, "Titus":{}, "Phmn":{}, "Heb":{}, "Jas":{}, "Jude":{}, "Rev":{}, }
    bible = {"":{}, "Gen":{},"Exo":{},"Lev":{},"Num":{},"Deut":{},"Josh":{},"Judg":{},"Ruth":{},"1 Sam":{},"2 Sam":{},"1 Kgs":{},"2 Kgs":{},"1 Chr":{},"2 Chr":{},"Ezra":{},"Neh":{},"Esth":{},"Job":{},"Ps":{},"Prov":{},"Eccl":{},"Song":{},"Isa":{},"Jer":{},"Lam":{},"Ezek":{},"Dan":{},"Hos":{},"Joel":{},"Amos":{},"Obad":{},"Jonah":{},"Micah":{},"Nah":{},"Hab":{},"Zeph":{},"Hag":{},"Zech":{},"Mal":{},"Matt":{},"Mark":{},"Luke":{},"John":{},"Acts":{},"Rom":{},"1 Cor":{},"2 Cor":{},"Gal":{},"Eph":{},"Phil":{},"Col":{},"1 Thess":{},"2 Thess":{},"1 Tim":{},"2 Tim":{},"Titus":{},"Phlm":{},"Heb":{},"Jas":{},"1 Pet":{},"2 Pet":{},"1 John":{},"2 John":{},"3 John":{},"Jude":{},"Rev":{}}

    nums = {'1', '2', '3', '4', '5', '6' ,'7' ,'8', '9'}
    not_in = []
    with open('bible.txt', 'r', encoding='utf-8') as f:
        for line in f:
            
            count = 0
            book = ""
            while line[count] not in nums:
                book += line[count]
                count += 1
            
            line = line.replace(book, "", 1)
            line = line.strip("\n")
            chapter, verse = line[:line.index(":")], line[line.index(":"):]
            verse_num, verse = line[0:line.index(" ")], line[line.index(" "):]
            
            if bible.get(book) is not None:
                if bible[book].get(chapter) is not None:
                    bible[book][chapter].append(verse)
                else:
                    bible[book][chapter] = [verse]  
            else:
                if book not in not_in:
                    not_in.append(book)
    return bible       

def my_tokenizer(text):
    punct = ',.!?:;()[]{}-_`\'\"'
    tokens = text.lower().split()
    tokens = [t.strip(punct) for t in tokens]
    tokens = [t for t in tokens if len(t) > 0]
    return tokens

def calculate_fequencies() -> dict:   
    words = {}
    for book in bible:
        for chapter in bible[book]:
            for verse in bible[book][chapter]:
                for word in word_tokenize(verse):
                    word = word.lower()
                    if words.get(word) is None:
                        words[word] = 1
                    else:
                        words[word] += 1
    return words

''' Returns 1 for bassic, 2 for values that appear 3-12 time, 3 for words that appear once'''
def frequent_score(word: str, freq: dict) -> int:
    if freq.get(word) is None or freq.get(word) > 1000:
        return 1
    elif freq.get(word) > 0:
        return 3-(freq.get(word)/max_freq)*1.5


''' Returns quartile ranges Q1, Q3'''      
def get_data_info(data):
    # Step 1: Sort the data in ascending order
    data_sorted = sorted(data)

    # Step 2: Find the median (Q2)
    mid = len(data_sorted) // 2
    Q2 = data_sorted[mid]
    print(Q2)
    # Step 3: Find Q1 and Q3
    if len(data_sorted) % 2 == 0:
        Q1 = (data_sorted[mid//2] + data_sorted[mid//2-1]) / 2
        Q3 = (data_sorted[-mid//2-1] + data_sorted[-mid//2]) / 2
    else:
        Q1 = data_sorted[mid//2]
        Q3 = data_sorted[-mid//2-1]
    print(f'Q1: {Q1}\tQ2: {Q2}\tQ3: {Q3}')
    print(f'Length: {len(data_sorted)}\tMidpoint: {mid}')
    print(f'First 2 {data_sorted.index(2)}\t First 3 {data_sorted.index(3)}')
    return Q1, Q3

'''Take a verese and the query and finds how many unique words are shared'''
def eval_unique(query: str, verse: str):
    query = set([i for i in my_tokenizer(query)])
    verse = set([i for i in my_tokenizer(verse)])
    
    similar_words = list(filter(lambda x: x in verse and x not in ",.():;", query))

    #similar_words = list(filter(lambda x: x in verse and x not in ",.():;", query))
    score = 0
    if len(similar_words) == 0:
        return 0
    
    score = sum([frequent_score(word, words) for word in similar_words])
    score /= len(similar_words)
        
    return score
     



bible: dict = {**parse_bible(), **parse_bom()}
words: dict = calculate_fequencies()
max_freq = max(words.values())

