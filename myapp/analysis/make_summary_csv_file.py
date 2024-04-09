import csv
from collections import defaultdict

# Paths to the CSV file and where to save the summary
input_csv_path = '/Users/milosz/Desktop/test/predictions4.csv'
output_csv_path = '/Users/milosz/Desktop/test/summary_predictions4.csv'

# Read the predictions from the CSV file
predictions = defaultdict(list)
with open(input_csv_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        folder = row['File Path'].split('/')[-2]
        genre = row['Genre']
        probability = float(row['Probability'].strip('%'))
        predictions[(folder, genre)].append(probability)

# Calculate the average probability for each genre in each folder
summary = {}
for (folder, genre), probs in predictions.items():
    average_prob = sum(probs) / len(probs)
    if folder not in summary:
        summary[folder] = {genre: average_prob}
    else:
        summary[folder][genre] = average_prob

# Save the summary to a new CSV file
with open(output_csv_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Folder', 'Genre', 'Average Probability'])
    for folder, genres in summary.items():
        for genre, prob in genres.items():
            csv_writer.writerow([folder, genre, f"{prob:.2f}%"])

print(f"Summary of predictions saved to {output_csv_path}")
