---
title: Search
layout: page
permalink: /search/
excerpt: Find what you are looking for at Musser Scout Reservation. We are bound to have it.
dependencies:
- src: https://cdnjs.cloudflare.com/ajax/libs/lunr.js/2.3.6/lunr.min.js
  integrity: sha256-M/Awbb/BYh+Rh0aGjpQid26p1b2OBsrk2k9yAvQxPV0=
scripts: 
- src: assets/custom/js/search.js

---

<form action="/search" method="get">
  <div class="form-row align-items-center">
    <div class="col-10">
      <label class="sr-only" for="query">Search</label>
      <input type="text" id="search-box" name="query" class="form-control mb-2">
    </div>
    <div class="col-auto">
      <input type="submit" value="search" class="btn btn-primary mb-2">
    </div>
  </div>
</form>

<div class="list-group" id="search-results"></div>

{% assign searchable_pages = site.pages | where_exp: "page", "page.layout == 'page' or page.layout == 'portal'" %}
<script>
  window.store = {
    {% for page in searchable_pages %}
      "{{ page.url | slugify }}": {
        "title": "{{ page.title | xml_escape }}",
        "author": "",
        "date": "{{ page.date | date: "%B %d, %Y" }}",
        "category": "{{ page.category | xml_escape }}",
        "content": {{ page.content | strip_html | strip_newlines | jsonify }},
        "url": "{{ page.url | xml_escape }}"
      },
    {%- endfor -%}
    {% for post in site.posts %}
      "{{ post.url | slugify }}": {
        "title": "{{ post.title | xml_escape }}",
        "author": "{{ post.author | xml_escape }}",
        "date": "{{ post.date | date: "%B %d, %Y" }}",
        "category": "{{ post.category | xml_escape }}",
        "content": {{ post.content | strip_html | strip_newlines | jsonify }},
        "url": "{{ post.url | xml_escape }}"
      }
      {% unless forloop.last %},{% endunless %}
    {%- endfor -%}
  };
</script>
