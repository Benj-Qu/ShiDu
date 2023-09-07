"""discription.

Index (main) view.

"""
import heapq
import threading
import flask
import requests
import search


@search.app.route('/', methods=["GET"])
def show_index():
    """Render the index page."""
    query = flask.request.args.get("q", type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)

    if query is None:
        context = {
            "documents": [],
            "doc_num": 0,
            "query": "",
            "weight": weight,
        }
        return flask.render_template("index.html", **context)

    param_dict = {"q": query, "w": weight}
    results = []
    get_results(param_dict, results)

    results = heapq.merge(*results,
                          key=lambda result: result["score"], reverse=True)

    context = {}
    connection = search.model.get_db()
    doc_list = []
    for i, doc in enumerate(results):
        if i == 10:
            break
        doc_list.append(
            connection.execute(
                "SELECT * "
                "FROM Documents "
                "WHERE docid = ? ",
                (doc["docid"], )
            ).fetchone()
        )
    context = {
        "documents": doc_list,
        "doc_num": len(doc_list),
        "query": query,
        "weight": weight,
    }
    return flask.render_template("index.html", **context)


def index_request(param_dict, i, results):
    """Request the index."""
    api_url = search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"][i]
    result = requests.get(api_url, params=param_dict, timeout=10)
    # result = json.loads(result)["hits"]
    print(result)
    results.append((result.json())["hits"])


def get_results(param_dict, results):
    """Get the results."""
    threads = []
    server_num = len(search.app.config["SEARCH_INDEX_SEGMENT_API_URLS"])
    for i in range(server_num):
        threads.append(
            threading.Thread(target=index_request,
                             args=(param_dict, i, results))
        )
        threads[i].start()

    for i in range(server_num):
        threads[i].join()
