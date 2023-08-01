import os
import typer
import markdown
import re
from bs4 import BeautifulSoup


app = typer.Typer()


def parse_markdown(file_path: str) -> str:
    with open(file_path, "r") as file:
        markdown_text = file.read()

    # Match nested lists and replace them with single level lists
    pattern = r"^(\s*)(\d+\.\s+)(?P<heading>.+?)(\n\s{3,})(-|\d+\.)"
    markdown_text = re.sub(pattern, r"\1### \g<heading>\n\4- ", markdown_text, flags=re.M)

    html = markdown.markdown(markdown_text)

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    # Replace HTML entities with corresponding characters
    entities = {"&amp;": "\&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'"}
    for entity, char in entities.items():
        soup = BeautifulSoup(str(soup).replace(entity, char), "html.parser")

    # Replace problematic Unicode characters with their LaTeX commands
    chars = {
        "（": "\\texttt{(}",
        "）": "\\texttt{)}",
        "，": ",",
        "α": "$\\alpha$",
        "&": "\\&",
        "%": "\\%",
    }
    for char, command in chars.items():
        soup = BeautifulSoup(str(soup).replace(char, command), "html.parser")

    for link in soup.find_all("a"):
        link.replace_with(f"\\href{{{link['href']}}}{{{link.text}}}")

    # Convert HTML to LaTeX
    latex = (
        str(soup)
        .replace("<ul>", "\\begin{itemize}")
        .replace("<ol>", "\\begin{enumerate}")
        .replace("</ul>", "\\end{itemize}")
        .replace("</ol>", "\\end{enumerate}")
        .replace("<li>", "\\item ")
        .replace("</li>", "\n")
        .replace("<h1>", "\\section*{")
        .replace("<h2>", "\\section*{")
        .replace("<h3>", "\\subsubsection*{")
        .replace("<h4>", "\\subsubsection*{")
        .replace("</h1>", "}\n")
        .replace("</h2>", "}\n")
        .replace("</h3>", "}\n")
        .replace("</h4>", "}\n")
        .replace("<p>", "")
        .replace("</p>", "\n")
    )

    # Replace escaped ampersands with the unescaped symbol
    latex = latex.replace("\\&amp;", "&")

    latex = latex.split("\n")
    indentation = -1
    for i, line in enumerate(latex):
        if "\\begin{" in line:
            indentation += 1
        elif "\\end{" in line:
            indentation -= 1
        latex[i] = "    " * indentation + line

    return "\n".join(latex)


def get_modules():
    return """
\\documentclass[letterpaper,10.8pt]{article}
\\usepackage{latexsym}
\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{marvosym}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{verbatim}
\\usepackage{enumitem}
\\usepackage[pdftex]{hyperref}
\\usepackage{fancyhdr}


\\pagestyle{fancy}
\\fancyhf{} % clear all header and footer fields
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

% Adjust margins
\\addtolength{\\oddsidemargin}{-0.575in}
\\addtolength{\\evensidemargin}{-0.575in}
\\addtolength{\\textwidth}{1in}
\\addtolength{\\topmargin}{-.5in}
\\addtolength{\\textheight}{1in}

\\urlstyle{rm}

\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

% Sections formatting
\\titleformat{\\section}{
  \\vspace{-3pt}\\scshape\\raggedright\\large
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

%-------------------------
% Custom commands
\\newcommand{\\resumeItem}[2]{
  \\item\\small{
    \\textbf{#1}{: #2 \\vspace{-2pt}}
  }
}

\\newcommand{\\resumeItemWithoutTitle}[1]{
  \\item\\small{
    {\\vspace{-2pt}}
  }
}

\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-1pt}\\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\textbf{#1} & #2 \\\\
      \\textit{\\small#3} & \\textit{\\small #4} \\\\
    \\end{tabular*}\\vspace{-5pt}
}


\\newcommand{\\resumeSubItem}[2]{\\resumeItem{#1}{#2}\\vspace{-4pt}}

\\renewcommand{\\labelitemii}{$\\circ$}

\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=*]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}

%-------------------------------------------
%%%%%%  CV STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\\begin{document}
"""


@app.command()
def build_resume(file_path: str):
    # Generate LaTeX string from Markdown
    latex = get_modules() + parse_markdown(file_path) + "\n\\end{document}"

    output_path = file_path.replace(".md", ".tex")

    # Write LaTeX string to file
    with open(output_path, "w") as file:
        file.write(latex)

    # Use pdflatex to compile LaTeX to PDF
    os.system(f"pdflatex {output_path}")

    # Print success message
    typer.echo(
        f"Resume generated and saved at: {os.path.splitext(output_path)[0] + '.pdf'}"
    )


if __name__ == "__main__":
    app()
