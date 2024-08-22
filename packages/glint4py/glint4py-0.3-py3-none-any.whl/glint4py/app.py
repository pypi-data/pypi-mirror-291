from glint import Glint
# glint4py (glint, oldversion)

from response import Response

app = Glint()

@app.route("/")
def index(request):
    return Response("Hello, World!")

@app.route("/about")
def about(request):
    return Response("This is the about page.")

# Middleware Beispiel
@app.use
def add_custom_header(response):
    response.body += "\nCustom-Header: Value"
    return response

if __name__ == "__main__":
    app.run()
