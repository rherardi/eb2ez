#!/usr/bin/env python3
"""
Eventbrite CSV Processor
Converts Eventbrite Attendee Reports to EZ Badge upload format
"""

import sys
import os
import csv
import argparse
from pathlib import Path


def print_help():
    """Print help message with command line syntax"""
    print("Usage: python eventbrite_processor.py <input_file.csv>")


def validate_csv_file(file_path):
    """
    Validate that the file exists and is a CSV file
    Returns True if valid, False otherwise
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist")
        return False
    
    # Check if file has .csv extension
    if not file_path.lower().endswith('.csv'):
        print(f"Error: {file_path} is not a CSV file")
        return False
    
    return True


def validate_eventbrite_headers(file_path):
    """
    Validate that the input file has the expected Eventbrite column headers
    Returns True if valid, False otherwise
    """
    expected_headers = [
        "Order #", "Order Date", "First Name", "Last Name", "Email", "Quantity",
        "Price Tier", "Ticket Type", "Attendee #", "Group", "Order Type", "Currency",
        "Total Paid", "Fees Paid", "Eventbrite Fees", "Eventbrite Payment Processing",
        "Attendee Status", "Home Address 1", "Home Address 2", "Home City", "Home State",
        "Home Zip", "Home Country", "How did you hear about this event?", "Are you a consultant?",
        "Are you an IEEE member?", "Are you an IEEE-CNSV Member?", "Where are you located (city+state or city+country)",
        "Please tell us where you heard about this event", "Of which IEEE Societies and/or Affinity Groups are you a member?",
        "Job Title", "Company"
    ]
    
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            
            # Check if all expected headers are present
            for expected_header in expected_headers:
                if expected_header not in headers:
                    print(f"Error: {file_path} does is not an Eventbrite Attendee Report")
                    return False
            
            return True
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False


def preprocess_data(data):
    """
    Preprocess the data according to the requirements
    """
    processed_data = []
    
    for row in data:
        # Create a copy of the row
        new_row = row.copy()
        
        # Transform "Are you a consultant?" values
        if "Are you a consultant?" in new_row:
            consultant_value = new_row["Are you a consultant?"]
            if consultant_value == "Yes":
                new_row["Are you a consultant?"] = "Consultant"
            elif consultant_value == "No":
                new_row["Are you a consultant?"] = " "
        
        # Transform "Are you an IEEE member?" values
        if "Are you an IEEE member?" in new_row:
            ieee_value = new_row["Are you an IEEE member?"]
            if ieee_value == "Yes":
                new_row["Are you an IEEE member?"] = "IEEE"
            elif ieee_value == "No":
                new_row["Are you an IEEE member?"] = " "
        
        # Transform "Are you an IEEE-CNSV Member?" values
        if "Are you an IEEE-CNSV Member?" in new_row:
            cnsv_value = new_row["Are you an IEEE-CNSV Member?"]
            if cnsv_value == "Yes":
                new_row["Are you an IEEE-CNSV Member?"] = "CNSV"
            elif cnsv_value == "No":
                new_row["Are you an IEEE-CNSV Member?"] = " "
        
        processed_data.append(new_row)
    
    return processed_data


def rename_columns(headers):
    """
    Rename column headers according to requirements
    """
    column_mapping = {
        "First Name": "FirstName",
        "Last Name": "LastName",
        "Company": "Company or Organization",
        "Are you an IEEE member?": "IEEE?",
        "Are you an IEEE-CNSV Member?": "CNSV?"
    }
    
    new_headers = []
    for header in headers:
        new_headers.append(column_mapping.get(header, header))
    
    return new_headers


def needs_quoting(value):
    """
    Determine if a value needs to be quoted based on CSV rules
    Returns True if value contains comma, newline, double-quote, or is just a space
    """
    if value == " ":  # Single space character
        return True
    if "," in value:  # Contains comma
        return True
    if "\n" in value or "\r" in value:  # Contains newline
        return True
    if '"' in value:  # Contains double-quote
        return True
    return False


def format_csv_value(value):
    """
    Format a value for CSV output, quoting only when necessary
    """
    if needs_quoting(value):
        # Escape any existing double quotes by doubling them
        escaped_value = value.replace('"', '""')
        return f'"{escaped_value}"'
    else:
        return value


def generate_output_file(input_file, data):
    """
    Generate the output file with the required format
    """
    # Define the exact output columns in order
    output_columns = [
        "FirstName", "LastName", "Email", "Company or Organization", "IEEE?", "CNSV?",
        "Are you a consultant?", "Are you on CNSV BOD?", "CB 6:1 - CNSV Email",
        "CB 6:2 - CNSV Website", "CB 6:3 - IEEE GRID", "CB 6:4 - Eventbrite Browsing",
        "CB 6:5 - Meetup", "CB 6:6 - Friend", "CB 6:7 - Other"
    ]
    
    # Create output filename
    input_path = Path(input_file)
    output_file = input_path.stem + "_EZ_BADGE_UPLOAD" + input_path.suffix
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            # Write header with trailing comma
            header_line = ','.join(format_csv_value(col) for col in output_columns) + ',\n'
            csvfile.write(header_line)
            
            # Write data rows
            for row in data:
                output_row = []
                for column in output_columns:
                    if column in row:
                        value = row[column]
                        # Replace empty values with space character
                        if value == "" or value is None:
                            value = " "
                        output_row.append(value)
                    else:
                        # Column not found, use space character
                        output_row.append(" ")
                
                # Write row with trailing comma
                row_line = ','.join(format_csv_value(val) for val in output_row) + ',\n'
                csvfile.write(row_line)
        
        print(f"Output file generated: {output_file}")
        return True
    
    except Exception as e:
        print(f"Error generating output file: {e}")
        return False


def process_csv_file(input_file):
    """
    Main processing function
    """
    try:
        # Read the CSV file
        with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            data = list(reader)
        
        # Preprocess the data
        processed_data = preprocess_data(data)
        
        # Rename headers for each row
        renamed_headers = rename_columns(headers)
        
        # Update the data with renamed headers
        updated_data = []
        for row in processed_data:
            new_row = {}
            for old_header, new_header in zip(headers, renamed_headers):
                new_row[new_header] = row[old_header]
            updated_data.append(new_row)
        
        # Generate output file
        return generate_output_file(input_file, updated_data)
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return False


def main():
    """
    Main function to handle command line arguments and orchestrate processing
    """
    # Handle command line arguments
    if len(sys.argv) == 1:
        # No arguments provided
        print_help()
        return
    
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        # Help requested
        print_help()
        return
    
    if len(sys.argv) != 2:
        # Wrong number of arguments
        print_help()
        return
    
    input_file = sys.argv[1]
    
    # Validate input file
    if not validate_csv_file(input_file):
        return
    
    # Validate Eventbrite headers
    if not validate_eventbrite_headers(input_file):
        return
    
    # Process the file
    if process_csv_file(input_file):
        print("Processing completed successfully!")
    else:
        print("Processing failed!")


if __name__ == "__main__":
    main()
