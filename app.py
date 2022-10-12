import requests
import bs4
import flask
import threading
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

app = flask.Flask(__name__)

class Browser(threading.Thread):
	def __init__(self, thread_name="browser", thread_id="browser"):
		threading.Thread.__init__(self)
		self.thread_name = thread_name
		self.thread_id = thread_id

		options = Options()
		options.add_argument("--headless")
		options.add_argument("--disable-gpu")
		service = Service("geckodriver.exe")
		self.driver = webdriver.Firefox(options=options, service=service)
		
		self.loading = False

	def open_page(self, url):
		self.driver.get(url)
		self.loading = True
		while not '"contentUrl":' in self.driver.page_source:
			time.sleep(0.2)
		self.loading = False

	def get_source(self):
		return self.driver.page_source

browser = Browser()

@app.route("/")
def index():
	return flask.render_template("index.html")


extracting = False
@app.route("/api/extract", methods=["POST"])
def extract():
	global extracting
	if extracting:
		return flask.jsonify({"error": "Already extracting"})

	extracting = True
	url = flask.request.headers.get("url")
	if not url:
		return flask.jsonify({"error": "URL not provided."})

	browser.open_page(url)
	while browser.loading:
		time.sleep(0.2)
		app.logger.info("loading.")
	html = browser.get_source()
	soup = str(bs4.BeautifulSoup(html, "html.parser"))
	contentIndex = soup.find("contentUrl")
	commaIndex = soup.find(",", contentIndex)
	source = soup[contentIndex:commaIndex].replace("contentUrl", "").replace(":", "").replace('"', "").replace("https", "https:").strip()
	extracting = False
	if source == "":
		app.logger.info(soup)
	return flask.jsonify(source)


if __name__ == "__main__":
	app.run(debug=True, port=5003)