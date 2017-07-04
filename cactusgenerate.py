# Generates pages for Cactus static site generator.

import os
import os.path
from cactusconfig import cactusroot
from jinja2 import Template

postTemplate = """
title: {{ post.title }}
author: Kristopher Johnson
date: {{ post.created }}

{% raw %}
{% extends "post.html" %}
{% block body %}
{% load markup %}
{% filter markdown %}
{% endraw %}

{{ post.body }}

{% raw %}
{% endfilter %}
{% endblock %}
{% endraw %}
"""

def cactus_generate(posts):
    template = Template(postTemplate)
    for post in posts:
        renderedText = template.render(post=post)
        filepath = os.path.join(cactusroot, "pages", "posts", post.url)
        print(f"Generating {filepath}")
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, "w") as f:
            f.write(renderedText)

