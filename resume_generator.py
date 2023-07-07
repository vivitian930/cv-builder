import json
from docx import Document
from docx.shared import Pt, Inches
from typing import List, Optional
from models import Resume
from user_interface import UserInterface
import typer

app = typer.Typer()

@app.command()
def generate_resume(input_file: Optional[str] = typer.Option(None, "--input", "-i", help="Path to input file")):
    ui = UserInterface()

    if input_file:
        # Read input from file
        with open(input_file, "r") as file:
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

def main():
    app()

if __name__ == "__main__":
    app()