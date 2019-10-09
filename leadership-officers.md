---
title: Lodge Officers
layout: page
permalink: /officers/
---
<table class="table table-responsive table-striped my-3">
  <thead>
    <tr>
      <th scope="col">Positon</th>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.lec.officers %}
      <tr>
        <td>{{person.title}}</td>
        <td>{{person.name}}</td>
        <td><a href="/contact?recipient={{person.email}}">{{person.email}}@unamilodge.org</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>
