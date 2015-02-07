from __future__ import division
import argparse
from lxml import html
import requests

# add city and mascot 
teams = [ 
 { "abbv" : "ATL", "city" : "Atlanta", "nickname" : "Hawks" }, 
 { "abbv" : "BOS", "city" : "Boston", "nickname" : "Celtics" },
 { "abbv" : "BRK", "city" : "Brooklyn", "nickname" : "Nets" },
 { "abbv" : "CHO", "city" : "Charlotte", "nickname" : "Hornets" },
 { "abbv" : "CHI", "city" : "Chicago", "nickname" : "Bulls" }, 
 { "abbv" : "CLE", "city" : "Cleveland", "nickname" : "Cavaliers" }, 
 { "abbv" : "DAL", "city" : "Dallas", "nickname" : "Mavericks" },
 { "abbv" : "DEN", "city" : "Denver", "nickname" : "Nuggets" }, 
 { "abbv" : "DET", "city" : "Detroit", "nickname" : "Pistons" }, 
 { "abbv" : "GSW", "city" : "Golden State", "nickname" : "Warriors" }, 
 { "abbv" : "HOU", "city" : "Houston", "nickname" : "Rockets" }, 
 { "abbv" : "IND", "city" : "Indiana", "nickname" : "Pacers" }, 
 { "abbv" : "LAC", "city" : "Los Angeles", "nickname" : "Clippers" }, 
 { "abbv" : "LAL", "city" : "Los Angeles", "nickname" : "Lakers" }, 
 { "abbv" : "MEM", "city" : "Memphis", "nickname" : "Grizzlies" }, 
 { "abbv" : "MIA", "city" : "Miami", "nickname" : "Heat" }, 
 { "abbv" : "MIL", "city" : "Milwaukee", "nickname" : "Bucks" }, 
 { "abbv" : "MIN", "city" : "Minnesota", "nickname" : "Timberwolves" }, 
 { "abbv" : "NOP", "city" : "New Orleans", "nickname" : "Pelicans" }, 
 { "abbv" : "NYK", "city" : "New York", "nickname" : "Knicks" }, 
 { "abbv" : "OKC", "city" : "Oklahoma City", "nickname" : "Thunder" }, 
 { "abbv" : "ORL", "city" : "Orlando", "nickname" : "Magic" }, 
 { "abbv" : "PHI", "city" : "Philadelphia", "nickname" : "76ers" },  
 { "abbv" : "PHO", "city" : "Phoenix", "nickname" : "Suns" }, 
 { "abbv" : "POR", "city" : "Portland", "nickname" : "Trail Blazers" }, 
 { "abbv" : "SAC", "city" : "Sacramento", "nickname" : "Kings" }, 
 { "abbv" : "SAS", "city" : "San Antonio", "nickname" : "Spurs" }, 
 { "abbv" : "TOR", "city" : "Toronto", "nickname" : "Raptors" }, 
 { "abbv" : "UTA", "city" : "Utah", "nickname" : "Jazz" }, 
 { "abbv" : "WAS", "city" : "Washington D.C.", "nickname" : "Wizards"} ]

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

 return values

parser = argparse.ArgumentParser(description="Calculate total points over/under for two NBA teams.")
parser.add_argument("away", help="Away Team Abbreviation (ex: GSW)")
parser.add_argument("home", help="Home Team Abbreviation (ex: OKC)")

args = vars(parser.parse_args())

away_values = scrape(args["away"])
home_values = scrape(args["home"])

away_total = round(float((away_values["pf"] + away_values["recent"] + home_values["pa"]) / 3), 2)
home_total = round(float((home_values["pf"] + home_values["recent"] + away_values["pa"]) / 3), 2)

print "%s: %.2f" % (away_values["team"], away_total)
print "%s: %.2f" % (home_values["team"], home_total)
print "TOT: %.2f" % (away_total + home_total)

#print away_values
#print home_values