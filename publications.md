---
layout: default
title: Publications
permalink: /publications/
description: "Full publication list — active inference, probabilistic ML, Bayesian inference, neuroscience, complex systems."
---

<p class="prompt">ls publications/ --sort=year --reverse</p>

<p class="pub-meta">
38 peer-reviewed and preprint publications · h-index 17 · 1,200+ citations.
Indexed on <a href="{{ site.links.scholar }}" rel="noopener">Google Scholar</a>
and <a href="{{ site.links.orcid }}" rel="noopener">ORCID</a>.
</p>

<ul class="pub-list">
{% assign all_pubs = site.data.publications | sort: "year" | reverse %}
{% for pub in all_pubs %}
  <li class="pub">
    <p>
      <span class="pub-year">{{ pub.year }}</span>
      <span class="pub-title">{{ pub.title }}</span>
    </p>
    <p class="pub-meta">{{ pub.authors }} · <em>{{ pub.venue }}</em></p>
    {% if pub.links %}
      <p class="pub-links">
        {% if pub.links.doi %}<a href="{{ pub.links.doi }}" rel="noopener">doi</a>{% endif %}
        {% if pub.links.arxiv %}<a href="{{ pub.links.arxiv }}" rel="noopener">arxiv</a>{% endif %}
        {% if pub.links.pdf %}<a href="{{ pub.links.pdf }}" rel="noopener">pdf</a>{% endif %}
        {% if pub.links.url %}<a href="{{ pub.links.url }}" rel="noopener">link</a>{% endif %}
      </p>
    {% endif %}
  </li>
{% endfor %}
</ul>

<p>→ full profile on <a href="{{ site.links.scholar }}" rel="noopener">Google Scholar</a> · <a href="{{ site.links.orcid }}" rel="noopener">ORCID</a></p>
