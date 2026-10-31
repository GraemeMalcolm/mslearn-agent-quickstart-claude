---
title: Develop your first agent with Claude
permalink: index.html
layout: home
---

Welcome to the lab for *Develop your first agent with Claude*!

In this lab, you'll prototype an agent in the Claude Console, build it in Python with the Claude SDK, and then use Claude Code in Visual Studio Code to add a new feature.

## Before you start

To complete this lab, you need:

- A [Claude Console](https://platform.claude.com){:target="_blank"} account with API credits (the lab uses a small amount).
- A [Claude](https://claude.ai){:target="_blank"} account or your Console account, to sign in to Claude Code.
- [Visual Studio Code](https://code.visualstudio.com/){:target="_blank"} installed.
- [Python version **3.10** or later](https://www.python.org/downloads/){:target="_blank"} installed.
- [Git](https://git-scm.com/install/){:target="_blank"} installed.

## Exercises

<hr>

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions/Labs'" %}
{% for activity in labs  %}
{% if activity.lab.title %}

### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{% if activity.lab.level %}**Level**: {{activity.lab.level}} \| {% endif %}{% if activity.lab.duration %}**Duration**: {{activity.lab.duration}}{% endif %}

{% if activity.lab.description %}
*{{activity.lab.description}}*
{% endif %}
<hr>
{% endif %}
{% endfor %}
