from flask import Flask, request, redirect, render_template_string
import json, os

DATA_FILE = "data/subscribers.json"

app = Flask(__name__)

HTML = """
<h2>⚖ Libra – Court Case Tracker</h2>
<form method="post">
  Advocate Name:<br>
  <input name="advocate" required><br><br>
  Email:<br>
  <input name="email" required><br><br>
  <button type="submit">Start Tracking</button>
</form>

<h3>Tracked Advocates</h3>
<ul>
{% for s in subs %}
<li>{{s["advocate_name"]}} → {{s["email"]}}</li>
{% endfor %}
</ul>
"""

def load_subs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_subs(subs):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE,"w") as f:
        json.dump(subs,f,indent=2)

@app.route("/", methods=["GET","POST"])
def index():

    subs = load_subs()

    if request.method == "POST":

        adv = request.form["advocate"].upper()
        email = request.form["email"]

        subs.append({
            "name": adv,
            "email": email,
            "advocate_name": adv,
            "client_names":[]
        })

        save_subs(subs)

        return redirect("/")

    return render_template_string(HTML, subs=subs)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

