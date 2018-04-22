from flask import Flask, render_template, request, session, redirect, url_for
import serial

app= Flask(__name__)
app.secret_key = "any random string"
global ser
ser= serial.Serial('/dev/ttyACM0', 9600)

# userData=["userinfo","typeofCampaign", "presidentVote", "vicePresidentVote","treasurerVote"]
global cardInfo
# cardInfo=[["4346DF2B",6,[]],["4ABBDF2B",5,[]],["708CDF2B",4,[]],["86E7DF2B",2,[]],["526EDF2B",1,[]]]
cardInfo= {"4346DF2B":6,"4ABBDF2B":5, "708CDF2B":4, "86E7DF2B":2, "526EDF2B":1 }
cardInfoThroughNumber= {6:"4346DF2B", 5:"4ABBDF2B", 4: "708CDF2B", 2: "86E7DF2B",1:"526EDF2B" }
userData=[]


@app.route("/")
def home():
	return render_template("admin.html")

@app.route("/startVote")
def startVote():
	serStr= ser.readline()
	# TODO: if id is in database, then have user choose a campagin, if not then try again
	# usingCard = cardInfo[serStr][1]
	serStr= str(serStr)
	serStr= serStr.strip()
	serStr= serStr[2:-5]
	serStr= serStr.replace(" ","")
	if serStr== "4ABBDF2B":
		return render_template("index.html")
	else:
		return "<h1>Not an Admin ID</h1>"


@app.route("/checkid", methods=["POST","GET"])
def checkid():
	return render_template("scanner.html")

@app.route("/pickcampaign", methods=["POST", "GET"])
def pickcampaign():
	serStr= ser.readline()
	# TODO: if id is in database, then have user choose a campagin, if not then try again
	# usingCard = cardInfo[serStr][1]
	serStr= str(serStr)
	serStr= serStr.strip()
	serStr= serStr[2:-5]
	serStr= serStr.replace(" ","")
	#~ serStr= serStr.replace(" ","")
	print(serStr)
	cardNumber= cardInfo[str(serStr)]
	print(cardNumber)
	if str(cardNumber) in session:
		userInfo= session[str(cardInfo[str(serStr)])][1]
		print(userInfo)
		return render_template("pickcampaign.html", userInfo=userInfo, cardNumber= cardNumber)
	else:
		return render_template("errorVoting.html")
	
	#~ return render_template("pickcampaign.html", userInfo=userInfo, cardNumber=cardNumber)



@app.route("/register", methods=["GET", "POST"])
def register():
	return render_template("registration.html")

@app.route("/saveinfo",methods=["POST"])
def saveinfo():
	if request.method == "POST":
		firstName= request.form["firstName"]
		lastName= request.form["lastName"]
		cardNumber= request.form["idnumber"]

		#checks for which card to add to
		# for x in cardInfo:
		# 	if int(cardNumber) in x:
		# 		whichArray= cardInfo.index(x)
		# 		whichLocation= x.index(int(cardNumber))
		# 		print(cardInfo.index(x), x.index(int(cardNumber)))
		# 	else:
		# 		pass
		# #adds info to the card
		# cardInfo[whichArray][2].append(firstName)
		# cardInfo[whichArray][2].append(lastName)
		# print(cardInfo[whichArray])
		cardHex= cardInfoThroughNumber[int(cardNumber)]
		print(cardHex)
		session[str(cardNumber)]= [cardHex,firstName+" "+lastName]
		print(session[str(cardNumber)])
		return redirect(url_for("home"))
	else:
		return render_template("registration.html")


@app.route("/voting", methods=["POST"])
def voting():
	#based on the choosen campagin it will give you a certain campagin
	if request.method == "POST":
		checkbox= request.form["optradio"]
		userData.append(checkbox)
		print(checkbox)
		if checkbox == "Presidential":
			return render_template("presidentialVote.html")
		elif checkbox == "NJ":
			return "<br><br><center><h1>Not available right now!</h1></center>"
		elif checkbox == "ballot":
			return render_template("ballot.html")
	else:
		print("didnt find campaign")
		return render_template("index.html")

@app.route("/ballotDone", methods=["POST"])
def ballotDone():
	if request.method == "POST":
		yesorno= request.form["optradio"]
		return "<h1>Thank You for Voting</h1>"



@app.route("/vicePresVote", methods=["POST"])
def vicePresVote():
	if request.method == "POST":
		presVote= request.form["optradio"]
		userData.append(presVote)
		print(presVote)
		return render_template("vicepresVote.html")
	else:
		print("didnt record a president vote")
		return render_template("presidentialVote.html")

@app.route("/treasurerVote", methods=["POST"])
def treasurerVote():
	if request.method == "POST":
		vicePresVote= request.form["optradio"]
		userData.append(vicePresVote)
		print(vicePresVote)
		return render_template("treasurerVote.html")
	else:
		print("didnt record a vice president vote")
		return render_template("vicePresVote.html")

@app.route("/thankYou", methods=["POST"])
def thankYou():
	if request.method == "POST":
		treasurerVote= request.form["optradio"]
		userData.append(treasurerVote)
		print(treasurerVote)
		#~ session[""]
		return render_template("thankYou.html", userData=userData)
	else:
		print("didnt record a treasurer vote")
		return render_template("treasurerVote.html")


if __name__=="__main__":
	app.run(debug=True)
