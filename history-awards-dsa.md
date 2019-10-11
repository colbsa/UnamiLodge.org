---
title: The Distinguished Service Award
layout: page
permalink: /history/awards/dsa
---
The Distinguished Service Award (DSA) was created in 1940 to honor those who rendered service to the Order beyond the lodge level. The award is presented to Arrowmen, youth and adult, who have rendered distinguished and outstanding service to the Order on a sectional, regional, or national basis. The award is presented at National Order of the Arrow Conferences. Since the time the first awards were presented, 1019 Distinguished Service Awards have been awarded.

The award is a sterling silver arrowhead bearing an arrow pointing up and to the wearer&#39;s right suspended from a white neck-ribbon on which red arrows are embroidered. A white square knot embroidered on red cloth is available for uniform wear, and a silver arrowhead lapel pin is available for civilian wear.

<table class="table table-responsive table-striped my-3 ">
  <thead>
    <tr>
      <th scope="col">Year</th>
      <th scope="col">Name</th>
      <th scope="col">Lodge</th>
      <th scope="col">Youth/Adult</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.awards-dsa reversed %}
      <tr>
        <td>{{person.year}}</td>
        <td>{{person.name}}</td>
        <td>{{person.lodge}}</td>
        <td>{{person.age}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
