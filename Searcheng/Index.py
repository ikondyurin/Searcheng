"""
The module defines classes Position, Position_line and Indexer, required for indexation of texts
"""
import unicodedata
import shelve
from Token import Token, Tokenizer


class Position(object):
    """The entities of this class are produced during
    indexation using 'Indexer()'"""

    def __init__(self, start, length):
        self.start = start
        self.length = length

    @property
    def end(self):
        return self.start + self.length

    def __repr__(self):
        return "%s->%s" % (self.start, self.end)


class Position_line(Position):
    """Stores the number of the line where the token occurred as well"""

    def __init__(self, start, length, line_index):

        self.start = start
        self.line = line_index
        self.length = length

    @property
    def end(self):
        return self.start + self.length

    def __repr__(self):
        return "%s->%s at line %s" % (self.start, self.end, self.line)

    def __eq__(self, p2):
        return ((self.start == p2.start) and
                (self.end == p2.end) and
                (self.line == p2.line))

    def __lt__(self, p2):
        # we compare lines; in case they are similar we compare start and end of the positions
        if (self.line != p2.line):
            return (self.line < p2.line)
        elif (self.start != p2.start):
            return (self.start < p2.start)
        else:
            return (self.end < p2.end)


class Indexer(object):
    """The class performs indexation of a string using 'index'
    and 'index_from_file' method"""
        
    # early version
    def index(self, s):

        """
        :param s: input string
        :return: dictionary "token:set of positions"
        """

        if not isinstance(s, str):
            raise TypeError("Input \'%s\' is not string." % (s))

        d = {}
        t = Tokenizer()
        for x in t.itertokenize_alfdigit(s):
            # we consider only 'alpha' and 'digit' tokens, see 'Token' module
            if x.string not in d:
                d[x.string] = [Position(x.start, x.length)]
            else:
                d[x.string].append(Position(x.start, x.length))
        return (d)

    def index_from_file(self, file):

        """
        Splits the string into tokens and creates two-level dictionary with
        tokens as first level keys using non-alphabetical symbols as dividers

        :param file: the file to be indexed
        :type file: .txt
        :return: dictionary which contains obtained tokens as keys and
        dictionary (with file name as keys and set of token's positions as values)
        as values
        :rtype: dict
        """

        t = Tokenizer()
        d = {}

        with open(file, 'r', encoding='utf-8') as infile:
            for line_index, line in enumerate(infile):
                for x in t.itertokenize_alfdigit(line):
                    #                   if (x._type == "alpha") or (x._type == "digit"):
                    # two-level dictionary is used to store both token and file names
                    d.setdefault(x.string, {}).setdefault(file,
                                                          []).append(Position_line(x.start, x.length, line_index))
                line_index += 1
            return (d)

    def index_to_db(self, file, database):

        """
        Splits the string into tokens and creates two-level shelve database with
        tokens as first level keys. Also prints the result into txt file. 

        :param file: the file to be indexed
        :type file: .txt
        :param database: the name of the database in which the result will be saved.
        :param file: the file to be indexed
        :type database: .db
        """

        t = Tokenizer()
        db = shelve.open(database, writeback=True)

        with open(
                file, 'r', encoding='utf-8'
        ) as infile, open(
                    "%s_results.txt" % (file), 'w', encoding='utf-8'
        ) as outfile:
            for line_index, line in enumerate(infile):
                for x in t.itertokenize_alfdigit(line):
                    #                   if (x._type == "alpha") or (x._type == "digit"):
                    db.setdefault(x.string, {}).setdefault(file,[]).append(Position_line(x.start, x.length, line_index))
                line_index += 1
            for i in db:
                outfile.write(str(i) + ': ' + str(db[i]) + '\n')
        db.close()


