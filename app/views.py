from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import csv
import json


def index(request):
    error_messages = []

    if request.method == "POST" and request.FILES:
        csvfile = request.FILES['csv_file']
        decoded_file = csvfile.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        rows = list(reader)
        # Check if CSV has at least one row
        if len(rows) < 1:
            error_messages.append("The CSV file is empty.")
        else:
            # Read validation properties from JSON file
            with open("properties.json") as prop_file:
                properties = json.load(prop_file)["properties"]
                print(properties)

            # Check each row
            for i, row in enumerate(rows[1:]):
                # print(row)
                if len(row) != len(properties):
                    error_messages.append(
                        f"Invalid number of columns in row {i+1}.")
                else:
                    for j, column in enumerate(row):
                        if j == 0 and not column.isalpha() and properties[j] != "":
                            error_messages.append(f"Invalid value in column {j+1} of row {i+1}. "
                                                  f"Expected string value.")
                        elif j == 1 and not column.isnumeric() and properties[j] != "":
                            error_messages.append(f"Invalid value in column {j+1} of row {i+1}. "
                                                  f"Expected integer value.")
                        elif j == 2 and not column.isalpha() and properties[j] != "":
                            error_messages.append(f"Invalid value in column {j+1} of row {i+1}. "
                                                  f"Expected string value.")

    return render(request, "index.html", {"error_messages": error_messages})


def download(request):
    # Code for file download (unchanged)
    pass
