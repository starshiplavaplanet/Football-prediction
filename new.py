import requests
from bs4 import BeautifulSoup

# Function to scrape results for a team
def scrape_team_results(team):
    url = "https://footystats.org/england/premier-league/team-stats/{}/last_5".format(team.lower().replace(" ", "-"))
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for result in soup.find_all("td", class_="text-center py-2"):
        if "W" in result.text:
            results.append("W")
        elif "D" in result.text:
            results.append("D")
        elif "L" in result.text:
            results.append("L")
    return results

# Function to predict outcome
def predict_outcome(team1, team2):
    team1_results = scrape_team_results(team1)
    team2_results = scrape_team_results(team2)
    team1_wins = team1_results.count("W")
    team1_draws = team1_results.count("D")
    team1_losses = team1_results.count("L")
    team2_wins = team2_results.count("W")
    team2_draws = team2_results.count("D")
    team2_losses = team2_results.count("L")

    print("Team 1 results:", team1_results)
    print("Team 2 results:", team2_results)
    
    if team1_wins > team2_wins:
        return "Home win"
    elif team2_wins > team1_wins:
        return "Away win"
    elif team1_draws > team2_draws:
        return "Home win"
    elif team2_draws > team1_draws:
        return "Away win"
    elif team1_losses < team2_losses:
        return "Home win"
    elif team2_losses < team1_losses:
        return "Away win"
    else:
        return "Draw"

# Ask the user for the number of matches to predict
num_matches = int(input("Enter the number of matches to predict: "))

# Open file to write results
with open("match_predictions.txt", "w") as file:
    for i in range(num_matches):
        # Ask the user for the teams playing
        team1 = input("Enter the name of the home team for match {}: ".format(i+1))
        team2 = input("Enter the name of the away team for match {}: ".format(i+1))
        prediction = predict_outcome(team1, team2)
        # Write prediction to file
        file.write("Match {}: {} vs {}. Prediction: {}\n".format(i+1, team1, team2, prediction))
        print("Prediction for match {}: {} vs {}: {}".format(i+1, team1, team2, prediction))

# Notify the user that the predictions are saved
print("Predictions saved to match_predictions.txt")
