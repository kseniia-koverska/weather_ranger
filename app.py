from flask import Flask, render_template, request
import sys
app = Flask(__name__, template_folder='frontend/Wetter/templates')

@app.route("/", methods=["GET","POST"])
def home():
	print("Python используется из:", sys.executable)
	if request.method == "POST":
		standort = request.form["standort"]
		datum = request.form["datum"]

		print("Standort:", standort)
		print("Datum:", datum)

	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)

