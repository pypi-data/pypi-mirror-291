from mistletoe import markdown as render_markdown
from pathlib import Path
from shutil import rmtree
from sys import argv
from os import system

def main():
    print(" - Erasing output/ directory")
    try:
        rmtree("output")
    except FileNotFoundError:
        pass

    template_path = Path(__file__).parent / "template.html"

    with template_path.open("r") as template_file:
        template = template_file.read()

    for input_path in Path("input").rglob("*.md"):
        with input_path.open("r") as input_file:
            # Load up the Markdown
            markdown = input_file.read()

            # Render the content
            html_content = render_markdown(markdown)

            # Extract the Heading 1
            for line in markdown.split("\n"):
                if line.startswith("# "):
                    title = line[2:]
                    break
            else:
                print(f"{input_path} is missing Heading 1")
                return 1

            # Generate the output
            html_output = template.replace("TITLE", title).replace("CONTENT", html_content)

            # Get the output path
            output_path = Path(str(input_path).replace("input", "output", 1)[:-2]+"html")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to disk
            with output_path.open("w") as output_file:
                output_file.write(html_output)

            # Print status
            print(f" - Converted {input_path} to {output_path}")

    # Copy static files
    for ext in ["js", "png"]:
        for base_path in [Path("input"), template_path.parent]:
            for input_path in base_path.rglob(f"*.{ext}"):
                with input_path.open("rb") as input_file:
                    # Load up the JS/PNG
                    static_file = input_file.read()

                    # Get the output path
                    output_path = Path(str(input_path).replace(str(base_path), "output", 1))

                    # Ensure output directory exists
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    # Write to disk
                    with output_path.open("wb") as output_file:
                        output_file.write(static_file)

    if len(argv) >= 2:
        repo_url = argv[1]
        assert "git@github.com" in repo_url
        domain = repo_url.split("/")[-1]
        system(f"""
            cd output
            echo {domain} > CNAME
            git init
            git add .
            git commit -m '_'
            git remote add origin {repo_url}
            git push --force --set-upstream origin main
        """)
    return 0
