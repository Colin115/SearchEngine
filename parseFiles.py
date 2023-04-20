'''
1 Nephi 1
Chapter 1

1 Nephi 1:1
 1 I, Nephi, having been born of goodly parents, therefore I was
taught somewhat in all the learning of my father; and having seen
many afflictions in the course of my days, nevertheless, having
been highly favored of the Lord in all my days; yea, having had a
great knowledge of the goodness and the mysteries of God,
therefore I make a record of my proceedings in my days.
'''

def parse_bom():
    books = ['Words of Morman']
    bom = {}
    with open('BOM.txt', 'r', encoding='UTF-8' ) as f:
        book = f.read()
        
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
        
        for book in books:
            #make each book have a dictionary of chapters
            bom[book] = {}
        
        new_verse = True
        cur_verse = []
        cur_book = '1 Nephi'
        cur_chapter = 1
        for i in range(len(lines)):
            if lines[i][0] == " ":
                #add old chapter to verse
                new_verse = True
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
    #bible = {"Ge":{}, "Exo":{}, "Lev":{}, "Num":{}, "Deu":{}, "Josh":{}, "Jdgs":{}, "Ruth":{}, "":{}, "Ezra":{}, "Neh":{}, "Est":{}}

    books = {}
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
         