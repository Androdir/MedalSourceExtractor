import requests
import bs4
import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
	return flask.render_template("index.html")


@app.route("/api/extract", methods=["POST"])
def extract():
	url = flask.request.headers.get("url")
	if not url:
		return flask.jsonify({"error": "URL not provided."})

	try:
		url = requests.get(url, allow_redirects=True).url
		if not "medal" in url.lower():
			return flask.jsonify({"error": "URL is not a Medal page."})
	except Exception as e:
		return flask.jsonify({"error": "Invalid URL."})

	html = requests.get(url, allow_redirects=True).text
	soup = bs4.BeautifulSoup(html, "html.parser")
	script = soup.find("script").text
	contentIndex = script.find("contentUrl")
	commaIndex = script.find(",", contentIndex)
	return flask.jsonify(script[contentIndex:commaIndex].replace("contentUrl", "").replace(":", "").replace('"', "").strip())


if __name__ == "__main__":
	app.run(debug=True)
