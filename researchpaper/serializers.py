import csv
from io import StringIO
from prettytable import PrettyTable
from rest_framework import serializers

class PaperSerializer(serializers.Serializer):
    PubmedID = serializers.CharField(max_length=20)
    Title = serializers.CharField(max_length=500)
    Publication_Date = serializers.CharField(max_length=100)
    Non_academic_Authors = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    Company_Affiliations = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    Corresponding_Author_Email = serializers.EmailField()

def papers_to_csv(papers):
    output = StringIO()
    
    writer = csv.writer(output, quoting=csv.QUOTE_ALL, lineterminator='\n')

    writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])

    for paper in papers:
        writer.writerow([
            paper.get("PubmedID", "").strip(),
            paper.get("Title", "").strip(),
            paper.get("Publication Date", "").strip(),
            "; ".join(paper.get("Non-academic Authors", [])).strip(),  # Ensure list items are joined properly
            "; ".join(paper.get("Company Affiliations", [])).strip(),
            paper.get("Corresponding Author Email", "").strip()
        ])

    return output.getvalue()

def display_table(papers):
    table = PrettyTable()
    table.field_names = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]

    for paper in papers:
        table.add_row([
            paper.get("PubmedID", ""),
            paper.get("Title", ""),
            paper.get("Publication Date", ""),
            "; ".join(paper.get("Non-academic Authors", [])),
            "; ".join(paper.get("Company Affiliations", [])),
            paper.get("Corresponding Author Email", "")
        ])

    print(table)
