from flask import Flask, render_template
import serial

app= Flask(__name__)

global ser
ser= serial.Serial('/dev/ttyACM1', 9600)


@app.route("/")
def home():
	return render_template("home.html")
	
@app.route("/scanning", methods=["POST","GET"])
def scanning():
	serStr= ser.readline()
	print(serStr)
	return render_template("decision.html", serStr=serStr)

@app.route("/voting")
def index():
	return render_template("index.html")
	
	
if __name__=="__main__":
	app.run(debug=True)

