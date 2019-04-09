from Token import Tokenizer, Token

class Morphan(object):
    """Performs simple morhological analysis"""

    def stemming(self,token,length):

        """
        Returns all possible stems of a token
        
        :param token: input entity of 'Token' class
        :param length: longest flexion of the language in question
        :return: all possible stems of this token
        """
        
        if token.length <= length:
            yield(token)
        else:
            for l in range(token.length, token.length-length-1, -1):
                for stem in (self.cut(token,l)):
                    yield(stem)
    
    def cut(self,token,length):

        """
        Cuts the flexion of a given langth from a token's string

        :param token: a token to be cut
        :param length: length of the stem
        :return: new token named 'stem'
        """
        
        stem = Token(token.start, token.string, token._type)
        stem.length = length
        stem.string = token.string[:length]
        yield(stem)


class Morphan_rules(Morphan):
    """Performs morhological analysis based on a set of flexions"""
 
    def __init__(self, filename):

        """
        :param filename: name of the file containing all possible flexions of
        a language in question
        """

        self.flexions, self.longest = self.filetoset(filename)

    def stemming(self, token):

        """
        Returns only morphologically acceptable stems of this token

        :param token: input entity of 'Token' class
        :return: morphologically acceptable stems of this token
        """
    
        if token.length < self.longest:
            yield(token)
        else:
            for l in range(token.length, token.length-self.longest-1, -1):
                if token.string[l:] in self.flexions:
                    for stem in (self.cut(token, l)):
                        yield(stem)
                        continue

    @staticmethod
    def filetoset(file):

        """
        Parses the list of flexions and finds the longest flesion
        
        :param file: name of the file containing all possible flexions of
        a language in question
        :return: tuple ['set of flexions', 'longest flexion']
        """
        
        longest = ''
        with open (file, 'r', encoding='utf-8') as infile:
            for line in infile:
                endings = line.split('%')
                for i in endings:
                    if len(i) > len(longest):
                        longest = i
            return[(set(endings)), len(longest)]
        
        
if __name__ == "__main__":
    a = Tokenizer().itertokenize_alfdigit("Мама мылочные раммау кот")
    for i in a:
        for j in Morphan().stemming(i,3):
            print(j)
    a = Tokenizer().itertokenize_alfdigit("С тремя людьми сразу? amazing, вах, ну ты даёшь")
    for i in a:
        for j in Morphan_rules("/Users/ivankondurin/Documents/Scrapresults.txt").stemming(i):
            print(j)
    
        
