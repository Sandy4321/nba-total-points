from __future__ import division
import argparse
from lxml import html
import requests

# add city and mascot 
teams = [ 
 { "abbv" : "ATL", "city" : "Atlanta", "nickname" : "Hawks", "off" : 3.4, "def" : 2.1}, 
 { "abbv" : "BOS", "city" : "Boston", "nickname" : "Celtics", "off" : -1.6, "def" : -0.6},
 { "abbv" : "BRK", "city" : "Brooklyn", "nickname" : "Nets", "off" : -2.2, "def" : -2.5},
 { "abbv" : "CHO", "city" : "Charlotte", "nickname" : "Hornets", "off" : -6.7, "def" : 1.2},
 { "abbv" : "CHI", "city" : "Chicago", "nickname" : "Bulls", "off" : 1.4, "def" : 1.1}, 
 { "abbv" : "CLE", "city" : "Cleveland", "nickname" : "Cavaliers", "off" : 6.2, "def" : -0.5}, 
 { "abbv" : "DAL", "city" : "Dallas", "nickname" : "Mavericks", "off" : 5.2, "def" : 0.7},
 { "abbv" : "DEN", "city" : "Denver", "nickname" : "Nuggets", "off" : -1.5, "def" : -2.8}, 
 { "abbv" : "DET", "city" : "Detroit", "nickname" : "Pistons", "off" : -1.2, "def" : -2.2}, 
 { "abbv" : "GSW", "city" : "Golden State", "nickname" : "Warriors", "off" : 5.9, "def" : 6.1}, 
 { "abbv" : "HOU", "city" : "Houston", "nickname" : "Rockets", "off" : 1.4, "def" : 1.8}, 
 { "abbv" : "IND", "city" : "Indiana", "nickname" : "Pacers", "off" : -2.8, "def" : 1.5}, 
 { "abbv" : "LAC", "city" : "Los Angeles", "nickname" : "Clippers", "off" : 3.7, "def" : 0.5}, 
 { "abbv" : "LAL", "city" : "Los Angeles", "nickname" : "Lakers", "off" : -4.5, "def" : -2.5}, 
 { "abbv" : "MEM", "city" : "Memphis", "nickname" : "Grizzlies", "off" : 1.7, "def" : 3.9}, 
 { "abbv" : "MIA", "city" : "Miami", "nickname" : "Heat", "off" : -2.1, "def" : -0.5}, 
 { "abbv" : "MIL", "city" : "Milwaukee", "nickname" : "Bucks", "off" : -0.9, "def" : 2.2}, 
 { "abbv" : "MIN", "city" : "Minnesota", "nickname" : "Timberwolves", "off" : -2.0, "def" : -4.4}, 
 { "abbv" : "NOP", "city" : "New Orleans", "nickname" : "Pelicans", "off" : 1.8, "def" : -2.8}, 
 { "abbv" : "NYK", "city" : "New York", "nickname" : "Knicks", "off" : -4.3, "def" : -6.8}, 
 { "abbv" : "OKC", "city" : "Oklahoma City", "nickname" : "Thunder", "off" : 2.1, "def" : 3.3}, 
 { "abbv" : "ORL", "city" : "Orlando", "nickname" : "Magic", "off" : -3.3, "def" : -2.5}, 
 { "abbv" : "PHI", "city" : "Philadelphia", "nickname" : "76ers", "off" : -11.4, "def" : 0.8},  
 { "abbv" : "PHO", "city" : "Phoenix", "nickname" : "Suns", "off" : 4.2, "def" : -1.0}, 
 { "abbv" : "POR", "city" : "Portland", "nickname" : "Trail Blazers", "off" : 2.3, "def" : 2.5}, 
 { "abbv" : "SAC", "city" : "Sacramento", "nickname" : "Kings", "off" : -2.6, "def" : -2.0}, 
 { "abbv" : "SAS", "city" : "San Antonio", "nickname" : "Spurs", "off" : 2.2, "def" : 4.0}, 
 { "abbv" : "TOR", "city" : "Toronto", "nickname" : "Raptors", "off" : 6.0, "def" : -1.9}, 
 { "abbv" : "UTA", "city" : "Utah", "nickname" : "Jazz", "off" : 0.6, "def" : -1.6}, 
 { "abbv" : "WAS", "city" : "Washington D.C.", "nickname" : "Wizards", "off" : -0.8, "def" : 2.8 }]

def scrape(team):

 values = {}
 
 values["team"] = team

 url = "http://www.basketball-reference.com/teams/%s/2015_games.html" % team
 page = requests.get(url)
 tree = html.fromstring(page.text)

 game_table_headers = tree.xpath("//div[@id='div_teams_games']/table/thead/tr/th")

 points_for = []
 points_against = []

 points_column = None
 points_against_column = None

 count = 0

 # find the pts and opp_pts column indexes (this probably won't change)
 for header in game_table_headers:
   stat = header.get("data-stat")
   if stat == "pts":
     points_column = count
   elif stat == "opp_pts":
     points_against_column = count
   count += 1

 game_results = tree.xpath("//div[@id='div_teams_games']/table/tbody/tr")
 for game in game_results:

   try:
     
     if (game[points_column - 1].text == "OT"):
       continue
     elif (game[points_column -1].text == "2OT"):
       continue
     
     game_for = int(game[points_column].text)
     game_against = int(game[points_against_column].text)

     points_for.append(game_for)
     points_against.append(game_against)

   except Exception as e: 
     pass

 values["pf"] = round(float(sum(points_for) / len(points_for)),2)
 values["recent"] = round(float(sum(points_for[-5:])/len(points_for[-5:])),2)
 values["pa"] = round(float(sum(points_against) / len(points_against)),2)
 values["last_5"] = points_for[-5:]

 values["last_7"] = points_for[-7:]
 values["last_7"].sort()
 values["last_7"].pop(0)
 values["last_7"].pop(len(values["last_7"]) - 1)
 values["last_7_recent"] = round(float(sum(values["last_7"])/len(values["last_7"])),2)

 return values

parser = argparse.ArgumentParser(description="Calculate total points over/under for two NBA teams.")
parser.add_argument("away", help="Away Team Abbreviation (ex: GSW)")
parser.add_argument("home", help="Home Team Abbreviation (ex: OKC)")

args = vars(parser.parse_args())

away_values = scrape(args["away"])
home_values = scrape(args["home"])

away_total = round(float((away_values["pf"] + away_values["recent"] + home_values["pa"]) / 3), 2)
home_total = round(float((home_values["pf"] + home_values["recent"] + away_values["pa"]) / 3), 2)

away_last7_total = round(float((away_values["pf"] + away_values["last_7_recent"] + home_values["pa"]) / 3), 2)
home_last7_total = round(float((home_values["pf"] + home_values["last_7_recent"] + away_values["pa"]) / 3), 2)


print "\n--- LAST 5 ---\n"

print "%s: %.2f -- %s" % (away_values["team"], away_total, away_values["last_5"])
print "%s: %.2f -- %s" % (home_values["team"], home_total, home_values["last_5"])
print "TOT: %.2f" % (away_total + home_total)

print "\n--- LAST 7 (drop high/low) ---\n"

print "%s: %.2f -- %s" % (away_values["team"], away_last7_total, away_values["last_7"])
print "%s: %.2f -- %s" % (home_values["team"], home_last7_total, home_values["last_7"])
print "TOT: %.2f" % (away_last7_total + home_last7_total)


#print away_values
#print home_values