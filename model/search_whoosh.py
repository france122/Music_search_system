from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import *
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import open_dir
import os.path
from whoosh.index import create_in
from whoosh.writing import AsyncWriter
from jieba.analyse import ChineseAnalyzer


def search_results(keyword):
    search_result = []
    search_result.extend(whoosh_query(keyword))
    return search_result

def whoosh_query(keyword):
    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    idx = create_in("test", schema)
    writer = idx.writer()

    writer.commit()
    searcher = idx.searcher()
    parser = QueryParser("content", schema=idx.schema)
    q = parser.parse(keyword)
    results = searcher.search(q)
    return results

