import json
from docx import Document
from docx.shared import Pt, Inches
from typing import List, Optional
from cv_builder.models import Resume
from cv_builder.user_interface import UserInterface
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def generate_resume(
    case_path: str = typer.Argument("cases/example", help="path"),
    json_file: Optional[str] = typer.Option(None, "--input", "-i", help="Path to input file")):
    


    input_path = Path(case_path).absolute()
    input_file = input_path / "input.json"
    ui = UserInterface(case_path=case_path)
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