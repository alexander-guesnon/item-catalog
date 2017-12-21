import requests
import random
import string
import httplib2
import json
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
from flask import Flask, render_template, request
from flask import abort, redirect, jsonify, url_for, flash
from flask import session as login_session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Items, Catagory
from loremipsum import get_sentences

app = Flask(__name__)
# PRIVATE KEY NOT FOR PRODUCTION USE
app.secret_key = 'L\x08\xbb\x82.".S\xf6\x0b\xff\xbb\xc4\x93\xcb\xf6W\x15\
\x03\xa8l\xfd\xb4\xa0\x02\x8a-\xca\x08\x0f\xda`'
engine = create_engine('sqlite:///items.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
'''
catagory

    Baseball
    Basketball
    Foosball
    Hockey
    Rock Climbing
    Skating
    SnowBoarding
    Soccer

itmes
    #Baseball
        Batting Helmet
        Bat
        Baseball
    #Basketball
        Basketball
        Backboard
        Backboard Net
    #Foosball
        Foosball Table
        Foosball Balls
        Foosball Players
    #Hockey
        Hockey Puck
        Hokey Stick
        Hockey Tape
    #Rock Climbing
        Rope
        Carabiner
        Harness
        Cam
    #Skating
        Skates
        Helmet
        Armpads
    #SnowBoarding
        Snowboard
        Snowboarding Helmet
        Goggles
    #Soccer
        Cleats
        Soccer Ball
        Soccer Net

tempItem = [["Batting Helmet", "Bat", "Baseball"],
            ["Basketball", "Backboard", "Backboard Net"],
            ["Foosball Table", "Foosball Balls", "Foosball Players"],
            ["Hockey Puck", "Hokey Stick", "Hockey Tape"],
            ["Rope", "Carabiner", "Harness", "Cam"],
            ["Skates", "Helmet", "Armpads"],
            ["Snowboard", "Snowboarding Helmet", "Goggles"],
            ["Cleats", "Soccer Ball", "Soccer Net"]]

def get_words():
    while(True):
        sentences_list = get_sentences(5)
        if(len(" ".join(sentences_list)) > 0 and
        len(" ".join(sentences_list)) <= 250):
            return " ".join(sentences_list)

'''


catagoryNames = session.query(Items).all()


for i in catagoryNames:
    print(i.name)
    print(i.catagory.name)
    print(i.user_id)
