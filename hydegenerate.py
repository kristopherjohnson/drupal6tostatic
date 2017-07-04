"""Generates pages for Hyde static site generator."""

import os
import os.path
from hydeconfig import hyderoot
from jinja2 import Template

postTemplate = """---
title: >
    {{ post.title }}
description: >
    {{ post.title }}
created: !!timestamp '{{ post.created }}'
tags:
    - testing
---

{{ post.body }}

"""

def hyde_generate(posts):
    template = Template(postTemplate)
    for post in posts:
        renderedText = template.render(post=post)
        filename = os.path.basename(post.url) + ".html"
        filepath = os.path.join(hyderoot, "content", "blog", filename)
        print(f"Generating {filepath}")
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, "w") as f:
            f.write(renderedText)

