from os.path import join, dirname
import pandas as pd
import numpy as np
from pymongo import MongoClient
import re
import datetime
from geopy.geocoders import Nominatim
geolocator = Nominatim()
"""

Use this file to read in the project nurse data, perform text pre-processing
and store data in mongo. The fields we're interested in storing are:

  'How many years of experience do you have?' -> experience,
  'What's your highest level of education?' -> education,
  'What is your hourly rate ($/hr)?' -> salary,
  'Department' -> department,
  'What (City, State) are you located in?' -> location,
  'What is the Nurse - Patient Ratio?' -> patientNurseRatio

Check server/models/Record.js for an example of the schema.

"""
  
hour_list = ["hour", "hr", "/h"]
year_list = ["/year", "yr", "annual"]
biweek_list = ["every other week", "bi weekly", "every 2 weeks", "biweek"]
month_list = ["month"]


def findAllNumbersInString(string):
  return max(np.array(map(float,re.findall(r"[-+]?\d*\.\d+|\d+", string.translate(None, ",")))))

def reformatWage(string):
  if any(substring in string.lower() for substring in hour_list):
    # holder = np.array(map(float,re.findall(r"[-+]?\d*\.\d+|\d+", string)))
    # print holder, max(holder)
    return "{0:.2f}".format(findAllNumbersInString(string))
  elif any(substring in string.lower() for substring in year_list):
    return "{0:.2f}".format(findAllNumbersInString(string)/2080)#/2080
  elif any(substring in string.lower() for substring in biweek_list):
    return "{0:.2f}".format(findAllNumbersInString(string)/80)
  elif ("week" in string.lower()):
    return "{0:.2f}".format(findAllNumbersInString(string)/40)
  elif ("month" in string.lower()):
    return "{0:.2f}".format(findAllNumbersInString(string)/160)
  elif ("day" in string.lower()):
    return "{0:.2f}".format(findAllNumbersInString(string)/8)
  else:
    try: 
      holder = float(max(re.findall(r"[-+]?\d*\.\d+|\d+", string.translate(None, "$"))))
      if holder > 1000:
        return "{0:.2f}".format(holder/2080)
      else:
        return holder
    except ValueError:
      return "0"

def reformatRatioNormal(string): 
  # Look for all of the normal ratio cases i.e 5:1 or 1:5 assuming 1 is always the nurse
  try:
    ratioArray = re.findall(r"\d+\:\d+|\d+\,\d+", string)
    if (len(ratioArray)>0):
      ratioArray = re.split(":|,",ratioArray[0])
      if(float(ratioArray[0]) > float(ratioArray[1])):
        if (float(ratioArray[1]) == 0):
          return round(float(ratioArray[0]))
        else:
          return round(float(ratioArray[0])/float(ratioArray[1]))
      else:
        if (float(ratioArray[0]) == 0):
          return round(float(ratioArray[1]))
        else:
          return round(float(ratioArray[1])/float(ratioArray[0]))
    else:
      return None;
  except TypeError:
    return None;
      
def reformatRatioHyphen(string):
  #look for case where input is a range and take the average
  try:
    ratioArrayh = re.findall(r"\d+\-\d+", string)
    if (len (ratioArrayh)>0):
      # print split, string
      # print ratioArray[0].split("-")
      ratioArrayh =[float(i) for i in ratioArrayh[0].split("-")]
      # print np.mean(ratioArrayh)
      return np.mean(ratioArrayh)
    else: 
      return None
  except TypeError:
    return None

def reformatRatioTo(string):
  #look for case where input is written in form 1 to 5
  try:
    split = string.split("to")
    if (len(split)>1):
      # print split
      try:
        first = float(re.findall(r"\d+",split[0])[-1]) if len(re.findall(r"\d+",split[0])) >0 else 1 
        second = float(re.findall(r"\d+",split[1])[0]) if len(re.findall(r"\d+",split[1])) >0 else 1 
        # print first, second
        return max(first, second)/min(first, second)
      except ValueError:
        return max(re.findall(r"\d+",string))
    else:
      return None
  except AttributeError:
      return None

def reformatRatio(string):
  valueN = reformatRatioNormal(string)
  if (valueN != None):
    # print valueN, string
    return valueN
  else:
    valueH = reformatRatioHyphen(string)
    if(valueH != None):
      # print valueH, string
      return valueH
    else:
      valueTo = reformatRatioTo(string)
      if(valueTo != None):
        # print valueTo, string
        return valueTo
      else:
        try:
          # print string
          holder = re.findall(r"\d+\.\d+|\d+", string)
          # print holder
          if (len(holder) > 0):
            values = [float(i) for i in holder]
            # print values
            # print np.mean(values), string
            return np.mean(values)
        except (ValueError, TypeError) as e:
          # print 0,string
          return 0

def reformatExperience(string):
  # reformat experience into a number
  try:
    exp = re.findall(r"\d+", string)
    if (len(exp)> 0):
      # print exp
      exp = [float(i) for i in exp]
     
      return np.mean(exp)
    else:
      return 0
  except TypeError:
      return 0

def reformatLocation(string):
  try:
    loca  = geolocator.geocode(string)
    return loca.latitude, loca.longitude
  except AttributeError:
    return 0, 0

def main():
    wage = "What is your hourly rate ($/hr)?"
    ratio = "What is the Nurse - Patient Ratio?"
    experience = "How many years of experience do you have?"
    education = "What's your highest level of education?"
    department = "Department"
    location = "What (City, State) are you located in?"
    client = MongoClient('mongodb://localhost:27017/')
    db = client['clipboardinterview']
    df = pd.read_csv(join(dirname(__file__), '../data/projectnurse.csv'))
    # print df[department]
    posts = db.records
    for index, row in df.iterrows():
      s = float(reformatWage(row[wage]))
      r = reformatRatio(row[ratio])
      ex = reformatExperience(row[experience])
      loca  = reformatLocation(row[location])
      post = {"location":[loca[0], loca[1]],
              "education":row[education],
              "salary":s,
              "experience":ex,
              "department":row[department],
              "patientNurseRatio":r
      }
      post_id = posts.insert_one(post).inserted_id
      print index, post_id
      
    # print df["What is your hourly rate ($/hr)?"]
if __name__ == "__main__":
    main()
