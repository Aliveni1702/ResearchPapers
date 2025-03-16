import csv
from io import StringIO
from prettytable import PrettyTable
from rest_framework import serializers

class PaperSerializer(serializers.Serializer):
    PubmedID = serializers.CharField(max_length=20)
    Title = serializers.CharField(max_length=500)
    Publication_Date = serializers.CharField(max_length=100)
    Non_academic_Authors = serializers.CharField(max_length=500)
    Company_Affiliations = serializers.CharField(max_length=500)
    Corresponding_Author_Email = serializers.EmailField()

# Function to filter papers by company affiliation (e.g., Biotech)
def filter_papers_by_biotech(papers):
    return [paper for paper in papers if any("Biotech" in affiliation for affiliation in paper.get('Company_Affiliations', []))]

# Function to convert papers data to CSV format
def papers_to_csv(papers):
    # Using StringIO to create an in-memory text stream
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    # Write CSV Header
    writer.writerow(['PubmedID', 'Title', 'Publication Date', 'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'])

    # Write Data Rows
    for paper in papers:
        writer.writerow([
            paper.get('PubmedID', ''),
            f'"{paper.get("Title", "")}"',  # Ensure titles are quoted if they contain commas
            paper.get('Publication_Date', ''),
            ', '.join(paper.get('Non_academic_Authors', [])),  # Join list items with commas if available
            ', '.join(paper.get('Company_Affiliations', [])),  # Join list items with commas if available
            paper.get('Corresponding_Author_Email', '')
        ])

    # Return the CSV data as a string
    return output.getvalue()

# Function to display papers as a table using PrettyTable
def display_table(papers):
    # Create a PrettyTable object
    table = PrettyTable()

    # Set column names for the table
    table.field_names = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]

    # Add the data rows
    for paper in papers:
        table.add_row([
            paper.get('PubmedID', ''),
            paper.get('Title', ''),
            paper.get('Publication_Date', ''),
            ', '.join(paper.get('Non_academic_Authors', [])),  # Join list items with commas if available
            ', '.join(paper.get('Company_Affiliations', [])),  # Join list items with commas if available
            paper.get('Corresponding_Author_Email', '')
        ])

    # Print the table to the console
    print(table)

# Manually provided data for testing
papers = [
    {
        'PubmedID': '1',
        'Title': 'Impact of CDA Dynamics .',
        'Publication_Date': '2024-01-10',
        'Non_academic_Authors': ['Dr. John Doe', 'Dr. Emily White'],
        'Company_Affiliations': ['Pharma Co.', 'Biotech Ltd.'],
        'Corresponding_Author_Email': 'john.doe@pharmaco.com'
    },
    {
        'PubmedID': '2',
        'Title': 'Universal driving .',
        'Publication_Date': '2023-11-22',
        'Non_academic_Authors': ['Dr. Alice Green'],
        'Company_Affiliations': ['HealthTech Inc.'],
        'Corresponding_Author_Email': 'alice.green@healthtech.com'
    },
    {
        'PubmedID': '3',
        'Title': 'Analysis ',
        'Publication_Date': '2023-10-05',
        'Non_academic_Authors': ['Dr. Bob Brown', 'Dr. Sarah Black'],
        'Company_Affiliations': ['NeuroTech Solutions'],
        'Corresponding_Author_Email': 'bob.brown@neurotech.com'
    }
]

# Filter papers to only include those with "Biotech" in the Company_Affiliations
filtered_papers = filter_papers_by_biotech(papers)

# Display the filtered papers as a table
display_table(filtered_papers)

# Convert filtered papers to CSV
csv_result = papers_to_csv(filtered_papers)

# Optionally, save the filtered CSV data to a file (uncomment the lines below to save to file)
def save_to_csv_file(csv_data, filename="filtered_papers.csv"):
    with open(filename, "w", newline="") as file:
        file.write(csv_data)
    print(f"Filtered CSV data saved to {filename}")

# Save the filtered CSV result to a file (optional)
save_to_csv_file(csv_result)
