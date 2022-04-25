from flask import Flask, request
import requests
app = Flask(__name__)

@app.route('/')
def root():
    return "<h1>Internal Server Error</h1><p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>"

@app.route('/search.html', methods=["GET", "POST"])
def query():
    if request.method == 'POST':
        search = request.form["query"].replace(" ","+")
        url = "https://www.google.com/search?q=" + search + "&hl=en-us&source=lnms&tbm=vid"
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
        text = resp.text.split("<a href=\"https://www.youtube.com/watch?v=")
        text.pop(0)
        codes = []
        for i in text: codes.append(i.split("\"")[0])
        x = 0
        for i in codes:
            del codes[x]
            x += 1
        all = "<div><ul>"
        for i in codes:
            titleurl = "https://youtube.com/watch?v=" + i
            titleresp = requests.get(titleurl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
            title = titleresp.text.split("<title>")[1].split(" - YouTube</title>")[0]
            all += "<li>" + title + " - ID: " + i + "<form action=\"video.html\" method=\"POST\"><input name=\"id\" id=\"view\" type=\"text\" value=\"" + i + "\"><input type=\"submit\" value=\"View\"></form></li>"
        all += "</ul></div>"
        return open("/home/TechDude/mepipe/search.html").read().replace("<div></div>", all)
    if request.method == 'GET':
        return open("/home/TechDude/mepipe/search.html").read()

@app.route('/video.html', methods=["GET", "POST"])
def video():
    if request.method == 'POST':
        return open("/home/TechDude/mepipe/video.html").read().replace("VIDEO_ID", request.form["id"])
