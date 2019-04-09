""" Module defines classes Searcher and Context used to perform search and build context windows."""
import unicodedata
import shelve
import re
from Token import Token, Tokenizer
from Index import Position_line, Position, Indexer

class Searcher(object):
    """
    The class performs search within shelve database using two methods.
    'search' method accepts a single string (regarded as
    a single word), while searchain accepts string of any length and splits it into tokens.
    """
    def __init__(self, database):
        self.db = shelve.open(database, writeback=False)
    
    def perform_search(self,searchain,window):
        search = self.searchain(searchain)
        res = self.context_of_search(search, window)
        if (len(res) == 0):
            res = "Поиск не дал результатов"
        return res
    
    def search(self,searchtoken):
        """
        Searches for locations and positions of a single string within shelve database.

        :param searchtoken: a string (regarded as a single word) NB: not 'Token'
        :type searchtoken: str
        :param database: the name of the database to be searched
        :type database: str
        :return: result_search -- dictionary "file: list of positions"
        :rtype: dict

        """
        
        #db = shelve.open(database, writeback=True)
        result_search = {}

        if not isinstance(searchtoken,str):
            raise TypeError("Input \'%s\' is not string."%(searchtoken))
        
        if searchtoken in self.db:
            # db[searhtoken] is a dic; key -- filename, value -- positions
            for file in self.db[searchtoken]:
                result_search.setdefault(file,[]).extend(self.db[searchtoken][file])

        #db.close()               
        return result_search

    def searchain(self,searchain):
        """
        Searches for locations and positions of a each word in the given
        string within shelve database. Returns the positions of these words ONLY
        in the files where all the words occured at least once. 

        :param searchain: a string to be searched (is tokenized during the search)
        :type searchain: str
        :param database: the name of the database to be searched
        :type database: str
        :return: result_chain dictionary "file: list of positions"
        :rtype: dict
        """
        
        t = Tokenizer()
        result_chain = {}
        setsearch = set()
        wordcheck = set()
        searchlist = []
        first = True
        
        for word in t.itertokenize_alfdigit(searchain):
            if word.string in wordcheck:
                continue
            search = self.search(word.string)
            searchlist.append(search)
            wordcheck.add(word.string)
            if first:
                setsearch = set(search.keys())
            else:                   
                setsearch &= set(search.keys())
            first = False

        for search in searchlist:
            for file in setsearch:
                result_chain.setdefault(file,[]).extend(search[file])

        # pairs with key = filename, value = joint positions of all tokens from query
        for pair in result_chain:
            result_chain[pair].sort(reverse = False)
        return(result_chain)

    def context_of_search(self, result, window):
        """
        Creates contexts of the search result for each file in the dictionary considering the given window size.

        :param result: dictionary "file: list of positions"
        :type result: dict
        :param window: size of the search window (in tokens/words)
        :type window: int
        :return: result_context -- a dictionary "file: list of contexts"
        :rtype: dict
        """

        result_context = {}
        
        for file in result:

            with open (file, 'r', encoding='utf-8') as f:
                it1 = enumerate(f)
                it2 = iter(result[file])
                cur_i, cur_line = next(it1)
                cur_pos = next(it2)
                while True:
                    if cur_i < cur_pos.line:
                        try:
                            cur_i, cur_line = next(it1)
                        except StopIteration:
                            break
                    elif cur_i > cur_pos.line:
                        try:
                            cur_pos = next(it2)
                        except StopIteration:
                            break                       
                    else:
                        result_context.setdefault(file,[]).append(Context([cur_pos], cur_line, window))
                        try:
                            cur_pos = next(it2)
                        except StopIteration:
                            break
                for pair in result_context:
                    self.normalize_context(result_context[pair])
                for pair2 in result_context:
                    self.extension(result_context[pair2])
                for pair3 in result_context:
                    self.normalize_context(result_context[pair3])
        return result_context 
                    
    def normalize_context(self, contexts):
        """
        Normalizes the initial result of "getcontext" method. Combines intersecting contexts.

        :param contexts: list of contexts
        :type contexts: list
        :return: same list
        :rtype: list
        """
        
        rindex = 1

        while rindex < len(contexts):

            if ((contexts[rindex].start <= contexts[rindex-1].end)
                and (contexts[rindex].line == contexts[rindex-1].line)):

                contexts[rindex-1].end = contexts[rindex].end
                contexts[rindex-1].positions += contexts[rindex].positions
                contexts.pop(rindex)
            else:
                rindex +=1

        return(contexts)

    def extension(self, contexts):
        """
        Extends context windows to the borders of the sentences.

        :param contexts: list of contexts
        :type contexts: list
        :return: same list
        :rtype: list
        """

        endpattern_right = "[.?!] "
        endpattern_left = " [.?!]"
            
        rindex = 0
        
        for rindex, r in enumerate(contexts):

            rightline = contexts[rindex].line[contexts[rindex].end:] 
            leftline = contexts[rindex].line[:contexts[rindex].start][::-1]
            #print({leftline: re.findall(endpattern_left, leftline), rightline: re.findall(endpattern_right, rightline)})
            patterns_right = re.finditer(endpattern_right, rightline)
            patterns_left = re.finditer(endpattern_left, leftline)

            try:
                contexts[rindex].end += next(patterns_right).start()
            except StopIteration:
                contexts[rindex].end = len(contexts[rindex].line)
            
            try:
                contexts[rindex].start -= next(patterns_left).start()
            except StopIteration:
                contexts[rindex].start = 0
    
        return(contexts)

    def __del__(self):
        self.db.close() 

class Context(object):
    """
    The class allows to create context windows with positions of the key words,
    text of the line and size of the window.

    build_context -- a method to calsulate start and end of the context window
    """
    
    def __init__(self, positions, line, window):
        """
        :param positions: list of positions of the key words. When a new context is created, len(positions) == 0 always
        :type positions: list
        :param line: text of the line where the key words occured
        :type line: str
        :param window: size of the window
        :type window: int
        """
        
        self.positions = positions
        self.window = window
        self.line = line
        self.start, self.end = self.build_context(window)

    def build_context(self, w):

        """
        Finds the beginning and the end for the context using the first key word, the line and the window size
        :param w: window size
        :type w: int
        :return: pair (start, end)
        :rtype: tuple
        """

        rightline = self.line[self.positions[0].end:]
        leftlinewrong = self.line[:self.positions[0].start]
        leftline = leftlinewrong[::-1]

        for wordindex, word in enumerate(Tokenizer().itertokenize_alfdigit(rightline)):
            if (wordindex >= w-1):
                break
        try:
            end = self.positions[0].end + word.end
        except UnboundLocalError:
            end = self.positions[0].end
        for wordindex2, word2 in enumerate(Tokenizer().itertokenize_alfdigit(leftline)):
            if (wordindex2 >= w-1):
                break
        try:
            start = self.positions[0].start - word2.end
        except UnboundLocalError:
            start = self.positions[0].start           
        return (start, end)
                       
    def __repr__(self):
        """
        Prints the context window and highlights the key words with HTML bold tag.

        :return: string including start and end of the context and the text included in it
        :rtype:
        """
        
        line = self.line[self.start:self.positions[0].start]
        for i, position in enumerate(self.positions):
            boldword = "<b>" + self.line[self.positions[i].start:self.positions[i].end] + "</b>"
            line += boldword
            try:
                line += self.line[self.positions[i].end:self.positions[i+1].start]
            except IndexError:
                line += self.line[self.positions[i].end:self.end]

        return line
        #return "%s -> %s '%s'"%(self.start, self.end, line)
        #return self.line[self.start:self.end]

                    

if __name__ == "__main__":
    #s = Indexer().index_to_db('wiki.txt', 'wikihotel')
    print(Searcher('voyna').perform_search('ему ему', 3))
