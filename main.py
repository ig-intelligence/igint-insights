from flask import Flask, request, Response
import json

from aggregate import metaanalysis

app = Flask(__name__)


@app.route('/insights/<user_id>', methods=['POST'])
def insights(user_id):
    analysed_posts = request.get_json()

    print('Received {} posts to aggregate'.format(len(analysed_posts)))

    insights = metaanalysis(analysed_posts)
    print(insights)

    return Response(json.dumps(insights), mimetype='application/json')


@app.route('/version')
def version():
    return '0.1.0'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
