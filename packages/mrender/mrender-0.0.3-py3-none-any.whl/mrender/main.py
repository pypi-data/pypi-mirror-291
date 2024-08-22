from click import command
from click import option
from pathlib import Path
from lager import log
from mrender.md import Markdown
def recursive_read(file, include=None, data=None):
    include = include or {".json", ".md", ".txt", ".yaml", ".toml", ".py"}
    data = {}
    if Path(file).is_file() and Path(file).suffix in include and "__pycache__" not in str(file):
        log.info(f"Reading file: {file}")
        with Path(file).open() as f:
            data[file] = f.read()
            return data
    if Path(file).is_dir():
        for file_path in Path(file).iterdir():
            data[file_path] = recursive_read(file_path)
        return data
    return {}
@command("mrender")
@option("--input", "-i", help="Input file or directory")
@option("--output", "-o", help="Output file")
@option("--format", "-f", help="Output format", default="md")
@option("--depth", "-d", help="Depth of the output", default=0)
def cli(input, output, format, depth=0):
   data = recursive_read(input)
   if format == "md":
         md = Markdown(data, save=output)
         md.stream(depth=depth)

if __name__ == '__main__':
    cli()