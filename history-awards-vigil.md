---
title: The Vigil Honor
layout: page
permalink: /history/awards/vigil/
---

<table class="table table-responsive table-striped my-3 ">
  <thead>
    <tr>
      <th scope="col">Year</th>
      <th scope="col">Name</th>
      <th scope="col">Lodge</th>
      <th scope="col">Location</th>
      <th scope="col">Name Interpretation</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.awards-vigil reversed %}
      <tr>
        <td>{{ person.year }}</td>
        <td>{{ person.fname }} {{ person.lname }}</td>
        <td>{{ person.lodge }}</td>
        <td>{{ person.location }}</td>
        <td>{{ person.interpretation }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
