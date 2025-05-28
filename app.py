from flask import Flask, render_template, redirect
import random

app = Flask(__name__)

with open('locations.txt') as f:
    LOCATIONS = [line.strip().replace(',', '').replace(' ', '').lower() for line in f.readlines()]

with open('topics.txt') as f:
    TOPICS = [line.strip().replace(',', '').replace(' ', '').lower() for line in f.readlines()]

@app.route("/")
def homepage():
    return "Welcome to RespireWork.com"

@app.route("/pages/<slug>.html")
def seo_page(slug):
    # Parse the topic and location from the slug
    for loc in LOCATIONS:
        for topic in TOPICS:
            if slug == f"{topic}_{loc}":
                title = f"Trending {topic.capitalize()} in {loc.capitalize()}"
                description = f"Explore the latest on {topic} happening now in {loc.capitalize()} at RespireWork."
                return render_template("page.html", title=title, description=description)
    return redirect("https://www.respirework.com")
