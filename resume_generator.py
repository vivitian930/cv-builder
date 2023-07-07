import argparse
import json
from docx import Document
from docx.shared import Pt, Inches
from typing import List, Optional
from models import Resume
from user_interface import UserInterface

def main():
    parser = argparse.ArgumentParser(description="Python Resume Generator")
    parser.add_argument("--input", help="Path to input file")

    args = parser.parse_args()

    ui = UserInterface()

    if args.input:
        # Read input from file
        with open(args.input, "r") as file:
            input_data = file.read()

        # Parse input JSON data
        data = json.loads(input_data)
        ui.resume = Resume(**data)

    else:
        # Capture user input
        ui.capture_personal_info()
        ui.capture_education()
        ui.capture_work_experience()
        ui.capture_research_experience()
        ui.capture_project_experience()
        ui.capture_personal_statement()

    # Display the resume
    ui.display_resume()

if __name__ == "__main__":
    main()