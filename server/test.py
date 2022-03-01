from ariadne import QueryType, gql, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, jsonify, request

type_defs = gql("""
  type Query {
    hello:String!
  }
""")

query = QueryType()

@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get("user-agent", "guest")
    return "Hello, {}!".format(user_agent)

schema = make_executable_schema(type_defs, query)

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST requests
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    
    status_code = 200 if success else 400

    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(debug=True)    