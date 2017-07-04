# Generates pages for Pelican static site generator.

import os
import os.path
from pelicanconfig import pelicanroot
from jinja2 import Template

postTemplate = """Title: {{ post.title }}
Date: {{ post.created }}
Category: Blog

{{ post.body }}

"""

def pelican_generate(posts):
    template = Template(postTemplate)
    for post in posts:
        renderedText = template.render(post=post)
        filename = os.path.basename(post.url) + ".md"
        filepath = os.path.join(pelicanroot, "content", filename)
        print(f"Generating {filepath}")
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, "w") as f:
            f.write(renderedText)

