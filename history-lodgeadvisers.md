---
title: Lodge Advisers
layout: page
permalink: /history/lodge-advisers
---
<table class="table table-striped my-3">
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Term</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.lodgeadvisers reversed %}
      <tr>
        <td>{{person.name}}</td>
        <td>{{person.start-year}} - {{person.end-year}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
