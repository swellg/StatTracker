import csv
import requests
from beautifultable import BeautifulTable

# Array of player IDs
player_ids = ["5663e0604cf84264907af2bd0c182c82","eec90030f7f842baa1d197a9e1ffd90f","fd5e414693624562a0e3cb0a2d5d1e7c","5c9a7866356c4886ada9ec9b081db07e","4a1300e1306346ccbea8145c52f3eb4d","f55086ededb048baac87c36047ab7fee","93e9b511ccde45cfaefc9c30396ca100","c058d86d080046a880b358549b7b23b0","c17544c48b744920894c20f9c873fed1"]

# API setup
base_url = "https://fortniteapi.io/v1/stats?account={}"
headers = {
    "Authorization": "YOUR_API_KEY"
}

# Function to fetch player data
def fetch_player_data(player_id):
    response = requests.get(base_url.format(player_id), headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'global_stats' not in data:
            print(f"Data for {player_id} does not contain 'global_stats': {data}")
            return None
        return data
    else:
        print(f"Failed to retrieve data for {player_id}: {response.status_code}")
        return None

# Read the existing data from the file
previous_data = {}
file_path = "data_log.csv"
try:
    # Write the updated data to the text file with UTF-8 encoding
    with open(file_path, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Mode", "Name", "Placetop1", "Matchesplayed"])
        for mode in previous_data:
            for name in previous_data[mode]:
                stats = previous_data[mode][name]
                writer.writerow([mode, name, stats["placetop1"], stats["matchesplayed"]])
except FileNotFoundError:
    print("No previous data found, starting fresh.")

# Create a BeautifulTable instance and set headers
table = BeautifulTable()
table.columns.header = ["Name", "Level", "Solos", "Duos", "Trios", "Squads", "+ Since Last Time"]

# Process each player ID
for player_id in player_ids:
    data = fetch_player_data(player_id)
    if data and 'global_stats' in data:
        since_last_time = {}
        for mode, stats in data["global_stats"].items():
            if mode in previous_data and data['name'] in previous_data[mode]:
                previous_stats = previous_data[mode][data['name']]
                wins_diff = stats["placetop1"] - previous_stats['placetop1']
                matches_diff = stats["matchesplayed"] - previous_stats['matchesplayed']
                since_last_time[mode] = f"{wins_diff}/{matches_diff}"
                # Update the previous_data with the latest stats
                previous_data[mode][data['name']] = {
                    'placetop1': stats["placetop1"],
                    'matchesplayed': stats["matchesplayed"]
                }
            else:
                since_last_time[mode] = "0/0"
                if mode not in previous_data:
                    previous_data[mode] = {}
                previous_data[mode][data['name']] = {
                    'placetop1': stats["placetop1"],
                    'matchesplayed': stats["matchesplayed"]
                }

        # Construct the "+ Since Last Time" string with Roman numerals
        since_last_time_str = ' '.join([
            f"I: {since_last_time.get('solo', '0/0')}",
            f"II: {since_last_time.get('duo', '0/0')}",
            f"III: {since_last_time.get('trio', '0/0')}",
            f"IV: {since_last_time.get('squad', '0/0')}"
        ])

        # Add a row to the table
        table.rows.append([
            data["name"],
            data["account"]["level"],
            f"{data['global_stats'].get('solo', {}).get('placetop1', 0)} / {data['global_stats'].get('solo', {}).get('matchesplayed', 0)}",
            f"{data['global_stats'].get('duo', {}).get('placetop1', 0)} / {data['global_stats'].get('duo', {}).get('matchesplayed', 0)}",
            f"{data['global_stats'].get('trio', {}).get('placetop1', 0)} / {data['global_stats'].get('trio', {}).get('matchesplayed', 0)}",
            f"{data['global_stats'].get('squad', {}).get('placetop1', 0)} / {data['global_stats'].get('squad', {}).get('matchesplayed', 0)}",
            since_last_time_str
        ])
        table.columns.width = [18, 8, 15, 15, 15, 15, 37]


# Print the table
print(table)
# When writing the table to a file
with open('Example.txt', 'w', encoding='utf-8') as file:
    file.write(str(table))

# Write the updated data to the text file with UTF-8 encoding
with open(file_path, "w", newline='', encoding='utf-8') as file:  # Specify encoding here
    writer = csv.writer(file)
    writer.writerow(["Mode", "Name", "Placetop1", "Matchesplayed"])
    for mode in previous_data:
        for name in previous_data[mode]:
            stats = previous_data[mode][name]
            writer.writerow([mode, name, stats["placetop1"], stats["matchesplayed"]])
