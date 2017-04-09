'''
Programmer Name: Matina Matic
Description: This program creates a website where a user has a quiz in the beginning
             and based on the answers from the quiz creates a new table and computes
             the probabilities that the user will like the dress that is stored in different table.
             It uses naive bayes classifier in computing the probabilities and it will reorder the table
             based on the probabilities. The website will display the top dress from the table, two from
             the middle and two from the bottom. The user will be able to say if she likes the dresses.
             Those answers will be added to the table and the probabilities will be computed again using
             the same process. At the last page the dress with the highest probability will be displayed.
'''

from flask import Flask, render_template, request, redirect
import sqlite3
from prettytable import PrettyTable
from flask import *
import random

app = Flask(__name__)

#get the connection with the sqlite database
con = sqlite3.connect("shop.db", timeout=10)
cur = con.cursor()

#create new tables for every user
cur.execute("DROP TABLE IF EXISTS answers")
cur.execute("CREATE TABLE IF NOT EXISTS answers (style TEXT, color TEXT, comfort TEXT, yes_no TEXT);")
cur.execute("DROP TABLE IF EXISTS dress")
cur.execute("CREATE TABLE IF NOT EXISTS dress(pictureDress TEXT,style TEXT, color TEXT, comfort TEXT, probability FLOAT);")
cur.execute("DROP TABLE IF EXISTS dressProbability")
cur.execute("CREATE TABLE IF NOT EXISTS dressProbability(pictureName TEXT, style TEXT, color TEXT, comfort TEXT, probability FLOAT);")

#get the connection with the sqlite database
@app.before_request
def before_request():
    g.db = sqlite3.connect("shop.db")

@app.route('/')
@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        return redirect(url_for('start'))

    return render_template('start.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        return redirect(url_for('question'))

    return render_template('question.html')

@app.route('/sample', methods=['GET', 'POST'])
def sample():

    if request.method == 'POST':
        #get the styles from question.html
        style = request.form.getlist('style')
        style1 = style[0]
        style2 = style[1]
        style3 = style[2]

        # get the colors from question.html
        color = request.form.getlist('color')
        color1 = color[0]
        color2 = color[1]
        color3 = color[2]

        # get the comfort from question.html
        comfort = request.form.get('comfort')

        #print the answers with the nice table
        t = PrettyTable(['STYLE', 'COLOR', 'COMFORT', 'LIKE?'])
        for x in range(0, 3):
            t.add_row([style1, color[x], comfort, 'LIKE'])
            t.add_row([style2, color[x], comfort, 'LIKE'])
            t.add_row([style3, color[x], comfort, 'LIKE'])

        print(t)

        #insert the answers from a quiz into the answers table
        g.db.execute("INSERT INTO answers (style,color,comfort,yes_no) VALUES(?,?,?,?);",
                     (style1, color1, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style1, color2, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style1, color3, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style2, color1, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style2, color2, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style2, color3, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style3, color1, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style3, color2, comfort, "LIKE"))
        g.db.execute("INSERT INTO answers (style,color,comfort, yes_no) VALUES(?,?,?,?);",
                     (style3, color3, comfort, "LIKE"))
        g.db.commit()

        #find the total number of "LIKE"
        totalAnswer = (g.db.execute("SELECT COUNT(*) FROM answers WHERE yes_no = 'LIKE';").fetchone()[0])

        #insert pictures with their attributes in the dress table
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('1.jpg','chic', 'black', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('2.jpg','artsy', 'green', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('3.jpg','casual', 'pink', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('4.jpg','exotic', 'red', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('5.jpg','glamorous', 'black', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('6.jpg','classic', 'white', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('7.jpg','sporty', 'pink', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('8.jpg','chic', 'black', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('9.jpg','sexy', 'white', '1', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('10.jfif','exotic', 'black', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('11.jfif','sexy', 'black', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('12.jfif','exotic', 'white', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('13.jfif','sexy', 'black', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('14.jpg','artsy', 'pink', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('15.png','sexy', 'black', '1', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('16.jpg','glamorous', 'blue', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('17.jfif','chic', 'red', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('18.jpg','chic', 'orange', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('19.jfif','casual', 'black', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('20.jfif','casual', 'blue', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('21.jfif','classic', 'black', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('22.jpg','glamorous', 'white', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('23.jpg','chic', 'yellow', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('24.jfif','casual', 'black', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('25.jfif','sexy', 'white', '1', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('26.jfif','classic', 'red', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('27.jfif','casul', 'black', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('28.jfif','artsy', 'white', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('29.jfif','classic', 'black', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('30.jfif','chic', 'black', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('31.jfif','artsy', 'white', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('32.jfif','classic', 'blue', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('33.jfif','casual', 'black', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('34.jfif','artsy', 'white', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('35.jfif','chic', 'white', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('36.jfif','exotic', 'grey', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('37.jfif','chic', 'black', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('38.jfif','chic', 'green', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('39.jfif','artsy', 'black', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('40.jfif','artsy', 'black', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('41.jfif','glamorous', 'blue', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('42.jfif','sexy', 'white', '2', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('43.jfif','artsy', 'blue', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('44.jfif','sexy', 'black', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('45.jpg','chic', 'pink', '4', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('46.jfif','classic', 'green', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('47.jfif','artsy', 'red', '3', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('48.jpg','chic', 'green', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('49.jpg','chic', 'black', '5', NULL);", )
        g.db.execute(
            "INSERT INTO dress (pictureDress, style, color, comfort, probability) VALUES ('50.png','sexy', 'black', '1', NULL);", )

        g.db.commit()

        #find the total number of records in dress table
        totalDress = (g.db.execute("SELECT COUNT(*) FROM dress").fetchone()[0])
        #print (totalDress)


        #P(like|style,color,comfort) = P(l)*P(style|l)*P(color|l)*P(comfort|l)

        #Probablity P(style|L)
        styleDress = g.db.execute("SELECT style FROM dress;").fetchall()
        styleAnswer = g.db.execute("SELECT style FROM answers;").fetchall()

        probabilityStyle=[]

        #find the probability of the style given the dress is liked
        #using m-estimator =(nc+m*p)/n+m
        for i in range(len(styleDress)):
            nc = 0
            for j in range(len(styleAnswer)):
                #probabilityStyle = styleProb(styleDress, styleAnswer, totalAnswer)
                nc =  nc +findN(styleDress[i], styleAnswer[j])
            n = totalAnswer
            m = 0.5
            p = 1/9
            probabilityStyle.append ((nc + m * p) / (n + m))

        # Probablity P(color|L)
        colorDress = g.db.execute("SELECT color FROM dress;").fetchall()
        colorAnswer = g.db.execute("SELECT color FROM answers;").fetchall()

        probabilityColor = []

        # find the probability of the color given the dress is liked
        # using m-estimator =(nc+m*p)/n+m
        for i in range(len(colorDress)):
            nc = 0
            for j in range(len(colorAnswer)):
                # probabilityColor = colorProb(colorDress, colorAnswer, totalAnswer)
                nc = nc + findN(colorDress[i], colorAnswer[j])
            n = totalAnswer
            m = 0.5
            p = 1 / 11
            probabilityColor.append ((nc + m * p) / (n + m))


        # Probablity P(style|L)
        comfortDress = g.db.execute("SELECT comfort FROM dress;").fetchall()
        comfortAnswer = g.db.execute("SELECT comfort FROM answers;").fetchall()

        probabilityComfort = []

        # find the probability of the comfort given the dress is liked
        # using m-estimator =(nc+m*p)/n+m
        for i in range(len(comfortDress)):
            nc = 0
            for j in range(len(comfortAnswer)):
                # probabilityComfort = comfortProb(comfortDress, comfortAnswer, totalAnswer)
                nc = nc + findN(comfortDress[i], comfortAnswer[j])

            n = totalAnswer
            m = 0.5
            p = 1/5
            probabilityComfort.append ((nc + m * p) / (n + m))


        probability = []
        #find the probability that the dress is liked
        for i in range(len(probabilityStyle)):
            probability.append(probabilityStyle[i] * probabilityColor[i] * probabilityComfort[i])


        pictureName = g.db.execute("SELECT pictureDress FROM dress;").fetchall()
        pictureStyle = g.db.execute("SELECT style FROM dress;").fetchall()
        pictureColor = g.db.execute("SELECT color FROM dress;").fetchall()
        pictureComfort = g.db.execute("SELECT comfort FROM dress;").fetchall()

        CharToIgnore = "()\"\',"

        #ignore all characters that are not part of the picture name, style, color or comfort
        #and insert those dresses with atributes into dressProbability table
        for i in range(len(probability)):
            pictureNameStr = str(pictureName[i])
            pictureStyleStr = str(pictureStyle[i])
            pictureColorStr = str(pictureColor[i])
            pictureComfortStr = str(pictureComfort[i])
            for char in CharToIgnore:
                pictureNameStr = pictureNameStr.replace(char, "")
                pictureStyleStr = pictureStyleStr.replace(char, "")
                pictureColorStr = pictureColorStr.replace(char, "")
                pictureComfortStr = pictureComfortStr.replace(char, "")

            g.db.execute("INSERT INTO dressProbability (pictureName, style, color, comfort, probability) VALUES(?,?,?,?,?);",
                         (pictureNameStr, pictureStyleStr, pictureColorStr, pictureComfortStr, float(probability[i])))
        g.db.commit()

        return redirect(url_for('sample'))


    newPicture = g.db.execute("SELECT pictureName FROM dressProbability ORDER BY probability DESC ;").fetchall()
    length = len(newPicture)

    #take dress one from top two from the middle two from the bottom
    picture1 = str(newPicture[length - 1])
    picture2 = str(newPicture[length - 2])
    picture3 = str(newPicture[int(length / 2)])
    picture4 = str(newPicture[int((length / 2) - 1)])
    picture5 = str(newPicture[1])

    # ignore all characters that are not part of the picture name
    CharToIgnore = "()\"\',"
    for char in CharToIgnore:
        picture1 = picture1.replace(char, "")
        picture2 = picture2.replace(char, "")
        picture3 = picture3.replace(char, "")
        picture4 = picture4.replace(char, "")
        picture5 = picture5.replace(char, "")

    return render_template('sample.html', picture1 = picture1, picture2 = picture2, picture3 = picture3,
                           picture4=picture4, picture5= picture5)


#find nc
def findN(numDress, numAnswer):
    count = 0
    if numDress == numAnswer:
        count = count + 1

    return count

#use this functions to compute the probabilites using just naive bayes classifier
'''def styleProb(styleDress, styleAnswer, totalAnswer):
    count = 0
    if styleDress == styleAnswer:
        count = count +1

    probability = count / totalAnswer
    return probability

def colorProb(colorDress, colorAnswer, totalAnswer):
    count = 0
    if colorDress == colorAnswer:
        count = count +1

    probability = count / totalAnswer
    return probability

def comfortProb(comfortDress, comfortAnswer, totalAnswer):
    count = 0
    if comfortDress == comfortAnswer:
        count = count +1

    probability = count / totalAnswer
    return probability
'''

@app.route('/outfit', methods=['GET', 'POST'])
def outfit():
    if request.method == 'POST':

        #get answers from the sample.html file
        answer1 = request.form.get('answer1')
        answer2 = request.form.get('answer2')
        answer3 = request.form.get('answer3')
        answer4 = request.form.get('answer4')
        answer5 = request.form.get('answer5')

        #get the picture names from sample.html file
        picture1 = str(request.form.get('picture1'))
        picture2 = str(request.form.get('picture2'))
        picture3 = str(request.form.get('picture3'))
        picture4 = str(request.form.get('picture4'))
        picture5 = str(request.form.get('picture5'))

        dress1Style = str(
            g.db.execute("SELECT style FROM dressProbability WHERE pictureName = '%s'" % picture1).fetchall())
        dress1Color = str(
            g.db.execute("SELECT color FROM dressProbability WHERE pictureName = '%s'" % picture1).fetchall())
        dress1Comfort = str(
            g.db.execute("SELECT comfort FROM dressProbability WHERE pictureName = '%s'" % picture1).fetchall())

        dress2Style = str(
            g.db.execute("SELECT style FROM dressProbability WHERE pictureName = '%s'" % picture2).fetchall())
        dress2Color = str(
            g.db.execute("SELECT color FROM dressProbability WHERE pictureName = '%s'" % picture2).fetchall())
        dress2Comfort = str(
            g.db.execute("SELECT comfort FROM dressProbability WHERE pictureName = '%s'" % picture2).fetchall())

        dress3Style = str(
            g.db.execute("SELECT style FROM dressProbability WHERE pictureName = '%s'" % picture3).fetchall())
        dress3Color = str(
            g.db.execute("SELECT color FROM dressProbability WHERE pictureName = '%s'" % picture3).fetchall())
        dress3Comfort = str(
            g.db.execute("SELECT comfort FROM dressProbability WHERE pictureName = '%s'" % picture3).fetchall())

        dress4Style = str(
            g.db.execute("SELECT style FROM dressProbability WHERE pictureName = '%s'" % picture4).fetchall())
        dress4Color = str(
            g.db.execute("SELECT color FROM dressProbability WHERE pictureName = '%s'" % picture4).fetchall())
        dress4Comfort = str(
            g.db.execute("SELECT comfort FROM dressProbability WHERE pictureName = '%s'" % picture4).fetchall())

        dress5Style = str(
            g.db.execute("SELECT style FROM dressProbability WHERE pictureName = '%s'" % picture5).fetchall())
        dress5Color = str(
            g.db.execute("SELECT color FROM dressProbability WHERE pictureName = '%s'" % picture5).fetchall())
        dress5Comfort = str(
            g.db.execute("SELECT comfort FROM dressProbability WHERE pictureName = '%s'" % picture5).fetchall())

        # ignore all characters that are not part of the style, color or comfort
        CharToIgnore = "()\"\',"
        for char in CharToIgnore:
            dress1Style = dress1Style.replace(char, "")
            dress1Color = dress1Color.replace(char, "")
            dress1Comfort = dress1Comfort.replace(char, "")

            dress2Style = dress2Style.replace(char, "")
            dress2Color = dress2Color.replace(char, "")
            dress2Comfort = dress2Comfort.replace(char, "")

            dress3Style = dress3Style.replace(char, "")
            dress3Color = dress3Color.replace(char, "")
            dress3Comfort = dress3Comfort.replace(char, "")

            dress4Style = dress4Style.replace(char, "")
            dress4Color = dress4Color.replace(char, "")
            dress4Comfort = dress4Comfort.replace(char, "")

            dress5Style = dress5Style.replace(char, "")
            dress5Color = dress5Color.replace(char, "")
            dress5Comfort = dress5Comfort.replace(char, "")

        #insert new training examples into answers table based on the quiz
        if (answer1 == "Yes"):
            g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                         (dress1Style, dress1Color, dress1Comfort, "LIKE") )
        else:
            if(answer1 == "No"):
                g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                             (dress1Style, dress1Color, dress1Comfort, "DON'T LIKE"))


        if (answer2 == "Yes"):
            g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                         (dress2Style, dress2Color, dress2Comfort, "LIKE") )
        else:
            if(answer2 == "No"):
                g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                             (dress2Style, dress2Color, dress2Comfort, "DON'T LIKE"))


        if (answer3 == "Yes"):
            g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                         (dress3Style, dress3Color, dress3Comfort, "LIKE") )
        else:
            if(answer3 == "No"):
                g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                             (dress3Style, dress3Color, dress3Comfort, "DON'T LIKE"))


        if (answer4 == "Yes"):
            g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                         (dress4Style, dress4Color, dress4Comfort, "LIKE") )
        else:
            if(answer4 == "No"):
                g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                             (dress4Style, dress4Color, dress4Comfort, "DON'T LIKE"))


        if (answer5 == "Yes"):
            g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                         (dress5Style, dress5Color, dress5Comfort, "LIKE") )
        else:
            if(answer5 == "No"):
                g.db.execute("INSERT INTO answers (style, color, comfort, yes_no) VALUES(?,?,?,?);",
                             (dress5Style, dress5Color, dress5Comfort, "DON'T LIKE"))

        answer = g.db.execute("SELECT yes_no FROM answers").fetchall()

        #get the total number of "LIKE"
        totalAnswer = (g.db.execute("SELECT COUNT(*) FROM answers WHERE yes_no = 'LIKE';").fetchone()[0])

        #get the total number of dresses
        totalDress = (g.db.execute("SELECT COUNT(*) FROM dress").fetchone()[0])
        print(totalDress)

        # Probablity P(style|L)
        styleDress = g.db.execute("SELECT style FROM dress;").fetchall()
        styleAnswer = g.db.execute("SELECT style FROM answers;").fetchall()

        probabilityStyle = []

        # find the probability of the style given the dress is liked
        # using m-estimator =(nc+m*p)/n+m
        for i in range(len(styleDress)):
            nc = 0
            for j in range(len(styleAnswer)):
                # probabilityStyle = styleProb(styleDress, styleAnswer, totalAnswer)
                nc = nc + findN(styleDress[i], styleAnswer[j])
            n = totalAnswer
            m = 0.5
            p = 1 / 9
            probabilityStyle.append((nc + m * p) / (n + m))


        # Probablity P(color|L)
        colorDress = g.db.execute("SELECT color FROM dress;").fetchall()
        colorAnswer = g.db.execute("SELECT color FROM answers;").fetchall()

        probabilityColor = []

        # find the probability of the color given the dress is liked
        # using m-estimator =(nc+m*p)/n+m
        for i in range(len(colorDress)):
            nc = 0
            for j in range(len(colorAnswer)):
                # probabilityColor = colorProb(colorDress, colorAnswer, totalAnswer)
                nc = nc + findN(colorDress[i], colorAnswer[j])
            n = totalAnswer
            m = 0.5
            p = 1 / 11
            probabilityColor.append((nc + m * p) / (n + m))


        # Probablity P(style|L)
        comfortDress = g.db.execute("SELECT comfort FROM dress;").fetchall()
        comfortAnswer = g.db.execute("SELECT comfort FROM answers;").fetchall()

        probabilityComfort = []

        # find the probability of the comfort given the dress is liked
        # using m-estimator =(nc+m*p)/n+m
        for i in range(len(comfortDress)):
            nc = 0
            for j in range(len(comfortAnswer)):
                # probabilityComfort = comfortProb(comfortDress, comfortAnswer, totalAnswer)
                nc = nc + findN(comfortDress[i], comfortAnswer[j])
            n = totalAnswer
            m = 0.5
            p = 1 / 5
            probabilityComfort.append((nc + m * p) / (n + m))

        probability = []
        #find the probabilty that the dress is liked
        for i in range(len(probabilityStyle)):
            probability.append(probabilityStyle[i] * probabilityColor[i] * probabilityComfort[i])


        pictureName = g.db.execute("SELECT pictureDress FROM dress;").fetchall()
        pictureStyle = g.db.execute("SELECT style FROM dress;").fetchall()
        pictureColor = g.db.execute("SELECT color FROM dress;").fetchall()
        pictureComfort = g.db.execute("SELECT comfort FROM dress;").fetchall()

        CharToIgnore = "()\"\',"

        # ignore all characters that are not part of the picture name, style, color or comfort
        # and insert those dresses with atributes into dressProbability table
        for i in range(len(probability)):
            pictureNameStr = str(pictureName[i])
            pictureStyleStr = str(pictureStyle[i])
            pictureColorStr = str(pictureColor[i])
            pictureComfortStr = str(pictureComfort[i])
            for char in CharToIgnore:
                pictureNameStr = pictureNameStr.replace(char, "")
                pictureStyleStr = pictureStyleStr.replace(char, "")
                pictureColorStr = pictureColorStr.replace(char, "")
                pictureComfortStr = pictureComfortStr.replace(char, "")

            g.db.execute(
                "INSERT INTO dressProbability (pictureName, style, color, comfort, probability) VALUES(?,?,?,?,?);",
                (pictureNameStr, pictureStyleStr, pictureColorStr, pictureComfortStr, float(probability[i])))
        g.db.commit()

        return redirect(url_for('outfit'))

    newPicture = g.db.execute("SELECT pictureName FROM dressProbability ORDER BY probability DESC ;").fetchall()
    newProbability = g.db.execute("SELECT probability FROM dressProbability ORDER BY probability DESC ;").fetchall()
    topProbability = newProbability[0]

    topDresses = []

    #find all the dress that have the same probability as the top dress and store them in topDress array
    for i in range(len(newProbability)):
        if (compare(newProbability[i], topProbability)):
                topDresses.append(str(newPicture[i]))

    #pick the random dress with the highest probability
    topDress = random.choice(topDresses)

    CharToIgnore = "()\"\',"
    for char in CharToIgnore:
        topDress = topDress.replace(char, "")

    return render_template('outfit.html', topDress=topDress)

#check if the values are the same
def compare(a,b):
    if a == b:
        result = True
        return result


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)


