---
title: Delmont Lodge Chiefs
layout: page
permalink: /history/delmont-chiefs
---
<table class="table table-striped my-3">
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Term</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.history-delmont_chiefs reversed %}
      <tr>
        <td>{{person.name}}</td>
        <td>{{person.term}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
