from flask import Flask, request, render_template, jsonify
from elasticsearch import Elasticsearch
from flask_cors import CORS
import math

# Elasticsearch connection
ELASTIC_PASSWORD = "Zac3QMwS3=qFQ-iXKJj1"
es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS if accessing API from different domains

@app.route('/')
def index():
    return render_template('home.html')  # Ensure your HTML file is in templates folder

@app.route('/search')
def search():
    page_size = 10
    keyword = request.args.get('keyword', '').strip()  # Get keyword from the query
    if not keyword:
        return render_template('search.html', hits=[], keyword=keyword, page_no=1, page_total=0)

    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1
    min_word_count = 3  # Set minimum word count for applying match_phrase
    is_long_phrase = len(keyword.split()) >= min_word_count
    # Build the search body
    body = {
        'size': page_size,
        'from': page_size * (page_no - 1),
        'query': {
            'bool': {
                'should': [
                    {   # For exact match on any word in fields
                        'multi_match': {
                            'query': keyword,
                            'fields': [
                                'Song Name^4',  # Boost song name relevance
                                'Artist/Band^2',
                                'Album Name',
                                'Lyrics'
                            ],
                            'type': 'best_fields',  # For exact/multiword match
                            'operator': 'or'
                        }
                    },
                    *(
                        [{
                        'match_phrase': {
                            'Lyrics': {
                                'query': keyword,
                                'boost': 3  # Higher boost for full phrase match in Lyrics
                            }
                        }
                        }] if is_long_phrase else []
                    ),
                    {   # For partial match or fuzzy matching (slightly misspelled)
                        'multi_match': {
                            'query': keyword,
                            'fields': [
                                'Song Name^2',
                                'Artist/Band',
                                'Lyrics'
                            ],
                            'type': 'phrase_prefix'  # Partial match with prefix
                        }
                    },
                    {   # For even more flexibility on fuzzy matches
                        'multi_match': {
                            'query': keyword,
                            'fields': [
                                'Song Name',
                                'Artist/Band'
                            ],
                            'fuzziness': 2,  # Allow up to 2 character changes
                            'prefix_length': 1,  # Only apply fuzziness after 1st character
                            'boost': 1  # Lower boost for fuzzy matches
                        }
                    }
                ],
                'minimum_should_match': 1,  # Ensure at least one match
                'boost':2
            }
        },
        'sort': [  # Ranking: sort by relevance first, then by popularity if available
            {'_score': 'desc'},
            {'Release Date': 'desc'}
        ]
    }

    res = es.search(index='songs_v2', body=body)
    hits = [
        {
            'Song Name': doc['_source']['Song Name'],
            'Artist/Band': doc['_source']['Artist/Band'],
            'Duration': doc['_source']['Duration'],
            'Release Date': doc['_source']['Release Date'],
            'Image': doc['_source']['Image'],
            'Type': doc['_source']['Type'],
            'Album Name': doc['_source']['Album Name'],
            'Lyrics': doc['_source']['Lyrics']
        } for doc in res['hits']['hits']
    ]
    results = [hit["_source"] for hit in res['hits']['hits']]
    for hit in res['hits']['hits']:
            print(hit["_source"]["Song Name"], hit["_score"])
            print()
    page_total = math.ceil(res['hits']['total']['value'] / page_size)

    return render_template('search.html', keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)

if __name__ == "__main__":
    app.run()

