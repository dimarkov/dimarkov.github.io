---
layout: default
title: Projects
permalink: /projects/
description: "Open-source projects: active-inference bandits, probabilistic inference, Bayesian model reduction, JAX libraries."
---

<p class="prompt">ls -la projects/</p>

<ul class="proj-list">
{% for p in site.data.projects %}
  <li class="proj">
    <p>
      <span class="proj-name">{{ p.name }}/</span>
      <span class="proj-meta">{{ p.stars }}★ · {{ p.language }} · last commit {{ p.last_commit }}</span>
    </p>
    <p class="proj-desc">{{ p.description }}</p>
    <p class="pub-links">
      <a href="https://github.com/{{ p.repo }}" rel="noopener">github.com/{{ p.repo }}</a>
    </p>
  </li>
{% endfor %}
</ul>

<p>→ full list on <a href="https://github.com/{{ site.links.github }}" rel="noopener">github.com/{{ site.links.github }}</a></p>
