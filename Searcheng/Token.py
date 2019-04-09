""" Module defines classes Token and Tokenizer."""
import unicodedata

class Tokenizer(object):
    """The class performs tokenisation of a string using 'tokenize' method"""

    def gettype(self,s):
        """
        Defines the type of each token's substring.

        Args:
        s -- the string, the type of which is to be defined
        """
        
        if (s.isalpha()):
            return "alpha"
        if (s.isdigit()):
            return "digit"
        if (s.isspace()):
            return "space"
        if (unicodedata.category(s)[0] == "P"):
            return "punctuation"
        else:
            return "unknown crap"

    def tokenize(self,s):
        """
        Splits the string into tokens and returns a list.

        Accepts string "s" as input. Splits "s" into tokens
        using non-alphabetical symbols as dividers and creates list
        "tokens" which contains obtained tokens.
        """

        prevtype = "unknown crap"
        tokens = []
        x = ''
        start = 0

        if not isinstance(s,str):
            print("Input \'%s\' is not string."%(s))
            raise TypeError
        for i,x in enumerate(s):
            if (self.gettype(x) != prevtype):
                if (i > 0):
                    string = s[start:i]
                    token_from_string = Token(start, string, prevtype)
                    tokens.append(token_from_string)
                prevtype = self.gettype(x)
                start = i
        #processes the last token, at the end of which the type of
        #string symbols does not change
        string = s[start:len(s)]
        token_from_string = Token(start, string, prevtype)
        if len(string) > 0:
            tokens.append(token_from_string)
        return(tokens)    
            
    def itertokenize(self,s):
        """
        Processes a string and generates tokens.

        Accepts string "s" as input. Splits "s" into tokens
        using non-alphabetical symbols as dividers.

        Args:
        s -- The string to be split.

        Yields:
        token_from_string -- The token obtained at each step.

        Raises:
        TypeError -- The argument contains elements
        which are not strings or anyhow non-iterable.
        """

        prevtype = "unknown crap"
        x = ''
        start = 0

        if not isinstance(s,str):
            raise TypeError("Input \'%s\' is not string."%(s))
        for i,x in enumerate(s):
            if (self.gettype(x) != prevtype):
                if (i > 0):
                    string = s[start:i]
                    token_from_string = Token(start, string, prevtype)
                    yield(token_from_string)
                prevtype = self.gettype(x)
                start = i
        #processes the last token, at the end of which the type of
        #string symbols does not change
        string = s[start:len(s)]
        token_from_string = Token(start, string, prevtype)
        if len(string) > 0:
            yield(token_from_string)

    def itertokenize_alfdigit(self,s):
        
        for token in self.itertokenize(s):
            if ((token._type == "alpha")
            or (token._type == "digit")):
                yield(token)
                
    def tokenize_alfdigit(self,s):

        tokens = []
        for token in self.itertokenize_alfdigit(s):
            tokens.append(token)
        return(tokens)    
            
class Token(object):
    """The entities of this class are produced during
    tokenisation using 'Tokenizer()'"""

    def __init__(self, start, string, _type):
        """
        Token contains a substring and information about its length and pos.

        Args:
        start -- The position of this token's substring in the original string.
        string -- The substring contained in this token.
        _type -- The string created using "_type" method of Tokenizer(), that
        defines the type of each token's substring. Can be: "alpha", "digit",
        "space", "punctuation", "unknown crap"
        """
 
        self.string = string
        self.start = start
        self.length = len(string)
        self._type = _type

    @property
    def end(self):
        return self.start + self.length 

    def __repr__(self):
        return self.string
 #       return "%s:[%s, %s, length = %s]"%(self.string,
 #                                      self.start, self._type, self.length)



if __name__ == "__main__":
    p = (Tokenizer().tokenize_alfdigit("Чем больше в дипломе воды -- там ., более 23 тщетн!ы труды"))
    print(p)
 
