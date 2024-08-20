import argparse
import os
import urllib.request

URL = "https://github.com/processing/p5.js/releases/latest/download/p5.min.js"

SKETCH = """function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(220);
}"""

HTML = """<!doctype html>
<html lang="en">
  <head>
    <script src="{p5src}"></script>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="style.css" />
    <meta charset="utf-8" />
  </head>

  <body>
    <main></main>
    <script src="sketch.js"></script>
  </body>
</html>"""

CSS = """html,
body {
  margin: 0;
  padding: 0;
}

canvas {
  display: block;
}"""


def main():
    parser = argparse.ArgumentParser(
        prog="p5gen", description="Generate a p5.js template"
    )
    parser.add_argument(
        "foldername", help="Name of the folder to create or to download files into"
    )
    parser.add_argument(
        "--title", "-t", default="Sketch", type=str, help="Title of sketch"
    )
    parser.add_argument(
        "--overwrite",
        "-o",
        default=False,
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "--cdn", "-c", default=False, action="store_true", help="Use p5.js from cdn"
    )

    args = parser.parse_args()

    fullpath = os.path.abspath(args.foldername)
    os.makedirs(fullpath, exist_ok=True)

    sketchpath = os.path.join(fullpath, "sketch.js")
    if not os.path.exists(sketchpath) or args.overwrite:
        with open(sketchpath, "w") as f:
            f.write(SKETCH)

    csspath = os.path.join(fullpath, "style.css")
    if not os.path.exists(csspath) or args.overwrite:
        with open(csspath, "w") as f:
            f.write(CSS)

    if args.cdn:
        p5src = URL
    else:
        p5src = "p5.min.js"
        urllib.request.urlretrieve(URL, os.path.join(args.foldername, p5src))

    indexpath = os.path.join(fullpath, "index.html")
    if not os.path.exists(indexpath) or args.overwrite:
        with open(indexpath, "w") as f:
            f.write(
                HTML.format(p5src=URL if args.cdn else "p5.min.js", title=args.title)
            )

    print("created a p5 sketch in", args.foldername)
