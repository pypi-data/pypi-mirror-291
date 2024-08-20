from typing import Any, Union
from collections import defaultdict
from pathlib import Path
import click
import os
import json
import shutil
import subprocess


def calculate_code_stats(root_dir: str) -> dict[str, dict[str, Union[float, int]]]:
    language_extensions = {
        "Python": [".py", ".pyi"],
        "Vue": [".vue"],
        "TypeScript": [".ts"],
        "JavaScript": [".js"],
        "HTML": [".html"],
        "CSS": [".css"],
        "Markdown": [".md"],
        "TOML": [".toml"],
        "JSON": [".json"],
        "Dockerfile": ["Dockerfile"],
        "Makefile": ["Makefile"],
        "C": [".c"],
        "Prisma": [".prisma"],
        "Nginx": [".conf"],
        "Shell": [".sh"],
        "Other": [],  # Catch-all for other file types
    }

    stats = defaultdict[str, int]()
    total_lines = 0

    def count_lines(file_path: Path) -> int:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return sum(1 for line in file if line.strip())
        except UnicodeDecodeError:
            # If the file is not text (e.g., binary file), return 0 lines
            return 0

    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = Path(root) / file

            # Skip binary files, build artifacts, and hidden files
            if (
                file_path.suffix in [".so", ".o", ".lock", ".lockb"]
                or "build" in file_path.parts
                or file.startswith(".")
            ):
                continue

            language = "Other"
            for lang, extensions in language_extensions.items():
                if file_path.suffix in extensions or file_path.name in extensions:
                    language = lang
                    break

            lines = count_lines(file_path)
            stats[language] += lines
            total_lines += lines

    # Calculate percentages
    percentages: dict[str, dict[str, Union[float, int]]] = {}
    for language, lines in stats.items():
        percentage = (lines / total_lines) * 100 if total_lines > 0 else 0
        percentages[language] = {"percentage": round(percentage, 2), "lines": lines}

    return percentages


@click.group()
def main():
    """Project management CLI tool"""
    pass


@main.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option(
    "--output", "-o", default="project_summary.md", help="Output markdown file name"
)
def compress(project_path: str, output: str):
    """Compress project in a markdown file"""
    with open(output, "w") as f:
        for root, _, files in os.walk(project_path):
            level = root.replace(project_path, "").count(os.sep)
            indent = " " * 4 * level
            f.write(f"{indent}- {os.path.basename(root)}/\n")
            subindent = " " * 4 * (level + 1)
            for file in files:
                f.write(f"{subindent}- {file}\n")
    click.echo(f"Project compressed into {output}")


@main.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option(
    "--output", "-o", default="project_summary.json", help="Output JSON file name"
)
def export(project_path: str, output: str):
    """Export project as JSON"""
    project_structure = defaultdict[str, Any]()
    for root, _, files in os.walk(project_path):
        current_level = project_structure
        path = root.split(os.sep)
        for directory in path:
            if directory not in current_level:
                current_level[directory] = {}
            current_level = current_level[directory]
        for file in files:
            current_level[file] = None

    with open(output, "w") as f:
        json.dump(project_structure, f, indent=4)
    click.echo(f"Project exported to {output}")


@main.command()
@click.argument("project_path", type=click.Path(exists=True))
def clear(project_path: str):
    """Clear __pycache__ files"""
    for root, dirs, _ in os.walk(project_path):
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(cache_path)
            click.echo(f"Removed: {cache_path}")
    click.echo("All __pycache__ directories have been removed")


@main.command()
def clean():
    """Clean Ubuntu system"""
    commands = [
        "sudo apt-get update",
        "sudo apt-get upgrade -y",
        "sudo apt-get autoremove -y",
        "sudo apt-get autoclean",
        "sudo journalctl --vacuum-time=3d",
    ]
    for cmd in commands:
        click.echo(f"Running: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    click.echo("Ubuntu system cleaned")


@main.command()
def install():
    """Install default packages into Ubuntu system"""
    packages = ["git", "vim", "curl", "wget", "htop", "tmux", "python3-pip"]
    cmd = f"sudo apt-get install -y {' '.join(packages)}"
    click.echo(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)
    click.echo("Default packages installed")


@main.command()
@click.argument("project_path", type=click.Path(exists=True), default=".")
def stats(project_path: str):
    """Calculate code statistics for the project"""
    results = calculate_code_stats(project_path)

    click.echo("Code Statistics:")
    for language, data in sorted(
        results.items(), key=lambda x: x[1]["lines"], reverse=True
    ):
        click.echo(f"{language}: {data['percentage']}% ({data['lines']} lines)")


@main.command()
def setup():
    """Setup the project"""
    SCRIPT = """#!/bin/bash
apt update -y
 apt upgrade -y
 apt install -y git
 apt install -y python3-pip
 apt install -y python-is-python3
 apt install -y virtualenv
 apt install -y python3-venv
 apt install -y python3-dev
curl -fsSL https://test.docker.com  | sh
 usermod -aG docker $USER
 apt install -y docker-compose
 apt install nodejs -y
 apt install npm -y
npm install -g npm@latest
npm install -g yarn
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | sh
nvm install 16
nvm use 16
 apt install tree -y
 apt install net-tools -y
 apt install curl -y
 apt install wget -y
npm i -g serverless
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
 ./aws/install
rm -rf awscliv2.zip
rm -rf aws
 apt-get install apt-transport-https ca-certificates gnupg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" |  tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg |  apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
 apt-get update &&  apt-get install google-cloud-cli
"""
    os.system(SCRIPT)


@main.command()
def load():
    """Loads Spacy models"""
    SCRIPT = """#!/bin/bash
python -m spacy download en_core_web_sm
python -m spacy download es_core_news_sm
"""
    os.system(SCRIPT)

