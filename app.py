from flask import Flask, render_template, request
import psycopg2
import random
import os

DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_SSL_MODE = os.environ['DATABASE_SSL_MODE']

conn = psycopg2.connect(DATABASE_URL, sslmode=DATABASE_SSL_MODE)

app = Flask(__name__)

cur = conn.cursor()

expanded_issues = {
    'science': '%(science|scientific|biology|microbiology|chemistry|physics)%',
    'math': '%(math|mathematic|calculus|statistic|algebra)%',
    'engineering': '%(engineer|engineering|machine|mechanical|turbine|appliance)%',
    'technology': '%(technology|tech|software|computer|fortran|turing|calculator)%',
    'art': '%(art|artist|illustration|painting|drawing|illustrate)%',
    'writing': '%(writing|writer|journalism|journalist|author|poem|literary)%',
    'spanish': '%(spanish)%',
    'economics': '%(economics|statistics|capitalism)%',
    'history': '%(history)%',
    'government': '%(government|politics|legal|prison)%',
    'psychology': '%(psychology)%',
    'anthropology': '%(anthropology)'
}

expanded_hobbies = {
    'photography': '%(photo|camera)%',
    'aviation': '%(aviation|aeronautic|airplane)%',
    'spirituality': '%(spirituality|quaker|hebrew|jewish|spiritual)%',
    'medicine': '%(medicine|doctor|physician|gynecological|ophthalmology|antibiotic|health|healthcare)%',
    'environment': '%(environment|sustain|conservation)%',
    'music': '%(music|compose|singer)%',
    'movies': '%(movie|documentary|film)%',
    'outer space': '%(space|nasa|satellite|astronaut|astronomy)%',
    'activism': '%(activism)%',
    'gender_sexuality': '%(gynecology|gynecological|vaginal|obstetric|breast)%',
    'writing': '%(journalism|writer|author|poem|literary)%',
    'painting': '%(paint|galleries|gallery)%',
    'fashion': '%(fashion|clothing|manicure|dressmaker|lipstick|underwear|undergarment|fabric|shoe|panty|stitch)'
}

@app.route('/')
def hello_world():
	return render_template('FRMcode.html')

@app.route('/role_model', methods=['POST'])
def createrolemodel():
    location = request.values["location"]
    hobbies = request.values["hobbies"]
    issues = request.values["issues"]
    # call my nlp function with these variables (locations, hobbies, issues)
    # write a function where i pass in the answers to 3 questions and it returns the name of the role model.
    
    profiles = pick_role_model(issues, hobbies, location)
    return render_template('role_model.html', profiles=profiles)
    
def searchdb(issues, hobbies, location):
    clean_location = location_clean(location)
    # query the db for matches
    cur.execute("SELECT profile_id FROM profiles WHERE topics SIMILAR TO %s AND topics SIMILAR TO %s AND topics SIMILAR TO %s",
        (expanded_issues[issues], expanded_hobbies[hobbies], clean_location))
        #(issues, hobbies, location))
    return cur.fetchall()

def random_chooser3(profile_possibilities):
    # choose up to 3 (or list length) random profiles from list
    if len(profile_possibilities) <= 3:
        return profile_possibilities
    return random.sample(profile_possibilities, 3)

def extract_fullname_hyperlink(chosen_profile_ids):
    output = []
    for id in chosen_profile_ids:
        cur.execute("SELECT fullname, hyperlink, summary, image_url FROM profiles WHERE profile_id = %s", (id,))
        found = cur.fetchall()
        if len(found) > 0:
            output.append({'name': found[0][0], 'link': found[0][1], 'summary': found[0][2], 'image_url': found[0][3]})
    print(output)
    return output 

def pick_role_model(issues, hobbies, location):
    profile_possibilities = searchdb(issues, hobbies, location)
    chosen_profile_ids = random_chooser3(profile_possibilities)
    final_profiles = extract_fullname_hyperlink(chosen_profile_ids)
    return final_profiles #This is gonna be a dictionary for name and link.  

def location_clean(raw_location):
    clean = raw_location.lower()
    clean = clean.replace(',', '').replace('.', '')
    clean = clean.replace(' ', '|')
    clean = "%(" + clean + ")%"
    return clean

