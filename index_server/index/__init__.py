"""Index  package initializer."""
import os
import flask
# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
import index.api  # noqa: E402  pylint: disable=wrong-import-position
# Load inverted index, stopwords, and pagerank into memory
app.data = tuple()
index.api.load_index()
