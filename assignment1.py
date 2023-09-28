import pymongo
import json
import yaml


#open json file
with open("example_tim_data.json") as f:
    data = json.load(f)

#open yaml file
with open("testschema.yaml") as yfile:
    schema = yaml.load(yfile, yaml.Loader)

#create mongodb connection
client = pymongo.MongoClient()
db = client.thedatabase
team_data = db.team_data
team_in_match = db.team_in_match


failed = False
for i in range(len(data)):
    for j in data[i]:
        if not isinstance(data[i][j], type(schema[j])):
            print("Error: json data does not match schema template at: ", data[i][j])
            failed = True

    
    


#team class
class Team():
    def __init__(self, team_number):
        self.team_number = team_number
        self.balls = []
        self.matches = 0
        self.climbed = []

        #get all info for team
        for i in range(len(data)):
            if data[i]["team_num"] == self.team_number:
                self.balls.append(data[i]["num_balls"])
                self.matches += data[i]["match_num"]
                self.climbed.append(data[i]["climbed"])
        
    
    def calculate_average_balls_scored(self):
        return ((sum(self.balls)/len(self.balls)))
    
    def calculate_least_balls_scored(self):
        return (min(self.balls))
    
    def calculate_most_balls_scored(self):
        return (max(self.balls))
    
    def calculate_num_matches(self):
        return(self.matches)
    
    def calculate_percent_climb_success(self):
        return (self.climbed.count(True) / (len(self.climbed)))


#Find all teams
teams = []
for i in range(len(data)):
    if data[i]['team_num'] not in teams:
        teams.append(data[i]['team_num'])

#add original json file to database
if not failed:
    for i in range(len(data)):
        team_in_match.insert_one(data[i])

    #add calculated team data to database
    for num in teams:
        currentteam = Team(num)
        team_data.insert_one({ 'team_num': num,
                            'average_balls_scored': currentteam.calculate_average_balls_scored(),
                            'least_balls_scored': currentteam.calculate_least_balls_scored(),
                            'most_balls_scored': currentteam.calculate_most_balls_scored(),
                            'num_matches': currentteam.calculate_num_matches(),
                            'percent_climb_success': currentteam.calculate_percent_climb_success()})
