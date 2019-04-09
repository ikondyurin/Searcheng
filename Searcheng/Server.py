from http.server import BaseHTTPRequestHandler, HTTPServer, CGIHTTPRequestHandler
import webbrowser
import os
import cgi
import sys
import html
from Searchfile import Searcher
from Index import Position_line, Position, Indexer
from Token import Token, Tokenizer


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        resp = "<html><head><title>Поиск</title></head><body><form method='POST' "
        resp += "action='search'><input name='Query' type='text' "
        resp += "value='Вводите это'><input name='Submit' type='submit'></form></body></html>"
        self.wfile.write(resp.encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                    'CONTENT_TYPE': self.headers['Content-type'],
                    })
        query = form.getfirst("Query", "")
        s = Searcher('voyna')
        res = s.perform_search(query, 2)
        out = ""
        out += "<html><body><form method='POST' action='search'>"
        out += "<input type=\"text\" name='Query' value=\"{}\"><input type='submit'>".format(query)
        out += "<ol>"
        if type(res) is str:
            out += "<b>{}</b></ol></body></html>".format(res)
        else:
            for doc in res:
                occ = res[doc]
                out += "<li><p>{}</p><ol>".format(doc)
                for o in occ:
                    out += "<li>{}</li>".format(o)
                out += "</ol></li>"
            out += "</ol></body></html>"
        self.wfile.write(bytes(out, 'utf-8'))
        
        #for i in res:
        
        #self.wfile.write(bytes(form['Name'].value, 'utf-8'))

def run(server_class=HTTPServer, handler_class=Handler):
    server = server_class(('', 8000), handler_class)
    server.serve_forever()

run()
#safari_path = 'open -a /Applications/Safari.app %s'
#url = '/Users/ivankondyrin/server.py'
#webbrowser.get(safari_path).open(url)





