from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/"), methods=["GET","POST"])
def home():
	if request.method == "POST":
		standort = request.form["standort"]
		datum = request.form["datum"]

		print("Standort:", standort)
		print("Datum:", datum)

	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)
