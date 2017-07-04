# Generates pages for Pelican static site generator.

import os
import os.path
from pelicanconfig import pelicanroot
from jinja2 import Template

postTemplate = """Title: {{ post.title }}
Date: {{ post.created }}
Category: Blog
Slug: {{ post.slug() }}
{% if post.tags %}Tags: {{ ", ".join(post.tags) }}
{% endif %}

{{ post.body }}

"""

def pelican_generate(posts):
    template = Template(postTemplate)
    for post in posts:
        renderedText = template.render(post=post)
        filepath = os.path.join(pelicanroot, "content", post.url + ".md")
        print(f"Generating {filepath}")
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, "w") as f:
            f.write(renderedText)

