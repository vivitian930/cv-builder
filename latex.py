import typer
import markdown
from typing import Dict

app = typer.Typer()


def parse_markdown(file_path: str) -> str:
    with open(file_path, "r") as file:
        markdown_text = file.read()
    html = markdown.markdown(markdown_text)
    return html


def add_heading(text: str, level: int) -> str:
    tex = f"\\{'sub'*level}section{{{text}}}\n"
    return tex


def add_list(items: list, ordered: bool, indentation_level: int) -> str:
    if not items:
        return ""
    list_type = "enumerate" if ordered else "itemize"
    tex = f"\\{'sub'*indentation_level},{list_type}\n"
    for item in items:
        tex += f"\t\\item {item}\n"
    tex += f"\\{'sub'*indentation_level}end{list_type}\n"
    return tex


def add_body_text(text: str) -> str:
    tex = f"{text}\n"
    return tex


@app.command()
def build_resume(file_path: str, output_path: str):
    html = parse_markdown(file_path)
    tex = ""

    indentation_level = 0
    items = []
    sections = {}

    for line in html.splitlines():
        if line.startswith("<h"):
            level = int(line[2])
            text = line[line.index(">") + 1 : line.rindex("</")]
            section_name = text.strip().replace(" ", "_").lower()
            if section_name not in sections:
                sections[section_name] = ""
            sections[section_name] += add_heading(text, level)
        elif line.startswith("<ul>"):
            indentation_level += 1
            items = []
        elif line.startswith("<ol>"):
            indentation_level += 1
            items = []
        elif line.startswith("<li>"):
            if "</li>" in line:
                item = line[line.index(">") + 1 : line.rindex("</")]
            else:
                item = line[line.index(">") + 1 :]
            items.append(item)
        elif line.startswith("</ul>"):
            indentation_level -= 1
            section_tex = add_list(
                items, ordered=False, indentation_level=indentation_level
            )
            sections[section_name] += section_tex
        elif line.startswith("</ol>"):
            indentation_level -= 1
            section_tex = add_list(
                items, ordered=True, indentation_level=indentation_level
            )
            sections[section_name] += section_tex
        elif line.startswith("<p>"):
            text = line[line.index(">") + 1 : line.rindex("</")]
            section_tex = add_body_text(text)
            sections[section_name] += section_tex

    with open(output_path, "w") as file:
        with open("template.tex", "r") as template_file:
            template = template_file.read()
            template = template.replace(
                "{YOUR NAME HERE}", "Srinivas Koushik Kondubhatla"
            )
            template = template.replace(
                "{YOUR EMAIL HERE}", "srinivas.koushik4@gmail.com"
            )
            template = template.replace(
                "{YOUR LINKEDIN HERE}", "https://www.linkedin.com/in/srinivaskoushik4/"
            )
            template = template.replace("{YOUR PHONE HERE}", "+13522839364")
            for section_name, section_tex in sections.items():
                template = template.replace(f"{{{section_name.upper()}}}", section_tex)
            file.write(template)

    typer.echo(f"Resume generated and saved at: {output_path}")


if __name__ == "__main__":
    app()
