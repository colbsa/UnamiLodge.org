---
title: The Green Turtle Award
layout: page
permalink: /history/awards/green-turtle
---
The Green Turtle Award was created by the Lodge Executive Committee in the spring of 2016 to recognize and thank those individuals who, and corporations and organizations which, have contributed significantly to the mission and goals of Unami Lodge, One and the Cradle of Liberty Council, whether by service or donation. Recipients of this award must not be members of Unami Lodge, One or the Order of the Arrow, but may be members of the Boy Scouts of America. Only those nominees whose accomplishments are of the highest order are recognized with the Green Turtle Award, and the lodge will present no more than two Green Turtle Awards a year.

<table class="table table-striped my-3 ">
  <thead>
    <tr>
      <th scope="col">Year</th>
      <th scope="col">Name</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.awards-green-turtle reversed %}
      <tr>
        <td>{{person.year}}</td>
        <td>{{person.name}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
