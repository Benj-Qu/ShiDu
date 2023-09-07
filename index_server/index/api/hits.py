"""REST API for hits."""
import re
import flask
import index


def load_index():
    """Load files into memory."""
    inverted_index = {}
    stopwords = []
    pagerank = {}
    # Read the stopwords file
    with open("index_server/index/stopwords.txt",
              "r", encoding="utf-8") as file:
        stopwords = file.read().split()
    # Read the pagerank file
    with open("index_server/index/pagerank.out",
              "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            key, value = line.split(",")
            pagerank[int(key)] = float(value)
    # Read the inverted index file
    index_path = index.app.config["INDEX_PATH"]
    with open(f"index_server/index/inverted_index/{index_path}",
              "r", encoding="utf-8") as file:
        for line in file.read().splitlines():
            split_line = line.split()
            token = split_line.pop(0)
            idf = float(split_line.pop(0))
            docu_info = {}
            while len(split_line) > 0:
                docid = int(split_line.pop(0))
                frequency = int(split_line.pop(0))
                factor = float(split_line.pop(0))
                docu_info[docid] = (frequency, factor)
            inverted_index[token] = (idf, docu_info)
    index.data = {
        "stopwords": stopwords,
        "pagerank": pagerank,
        "index": inverted_index
    }


def clean_query(query):
    """Clean query."""
    terms = re.sub(r"[^a-zA-Z0-9 ]+", "", query).casefold().split()
    valid_terms = []
    for term in terms:
        if term not in index.data["stopwords"]:
            valid_terms.append(term)
    return valid_terms


def get_query_frequency(terms):
    """Get query frequency."""
    query_tf = {}
    for term in terms:
        if term in query_tf:
            query_tf[term] += 1
        else:
            query_tf[term] = 1
    return query_tf


def calculate_scores(docu_list, score_factors, weight, pagerank):
    """Calculate scores and sort the documents."""
    # Get query factor
    query_factor = 0
    for ele in score_factors["query_vector"]:
        query_factor += ele ** 2
    query_factor = query_factor ** 0.5
    # Calculate docu tfidf scores
    docu_tfidf = {}
    for docid in docu_list:
        docu_tfidf[docid] = sum(
            vec[0] * vec[1] for vec in zip(
                score_factors["query_vector"],
                score_factors["docu_vectors"][docid],
            )
        ) / (query_factor * score_factors["docu_factors"][docid])
    # Calculate the score
    docu_score = []
    for docid in docu_list:
        docu_score.append({
            "docid": docid,
            "score": weight * pagerank[docid] + (1-weight) * docu_tfidf[docid],
        })
    docu_score.sort(reverse=True, key=lambda info: info["score"])
    return docu_score


@index.app.route('/api/v1/hits/')
def get_hits():
    """Get hits."""
    query = flask.request.args.get("q", default="", type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)
    context = {}
    # Cleaning query
    terms = clean_query(query)
    # Intersection of docu sets
    docu_sets = []
    for term in terms:
        if term in index.data["index"]:
            _, docu_info = index.data["index"][term]
            docu_sets.append(set(docu_info.keys()))
        else:
            docu_sets.append(set())
    if len(docu_sets) == 0:
        docu_list = []
    else:
        docu_list = list(set.intersection(*docu_sets))
    # Score factor dict
    score_factors = {
        "query_tf": {},
        "query_vector": [],
        "docu_vectors": {},
        "docu_factors": {},
    }
    # Query term frequency
    score_factors["query_tf"] = get_query_frequency(terms)
    # Remove duplicate terms
    terms = list(set(terms))
    # Get query vector and document vectors
    for term in terms:
        if term not in index.data["index"]:
            context["hits"] = []
            return flask.jsonify(**context)
        idf, docu_info = index.data["index"][term]
        score_factors["query_vector"].append(
            score_factors["query_tf"][term] * idf
        )
        for docid in docu_list:
            frequency, factor = docu_info[docid]
            if docid in score_factors["docu_vectors"]:
                score_factors["docu_vectors"][docid].append(frequency * idf)
            else:
                score_factors["docu_vectors"][docid] = [frequency * idf]
                score_factors["docu_factors"][docid] = factor ** 0.5
    # Get context
    context["hits"] = calculate_scores(
        docu_list, score_factors, weight, index.data["pagerank"]
    )
    return flask.jsonify(**context)
