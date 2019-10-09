---
title: The Thomas J. Richards Outstanding Service Award
layout: page
permalink: /history/awards/youth-osa
---
The Thomas J. Richards Outstanding Service Award was established by the Lodge Executive Committee in October of 2010. Tom — a past lodge committee chairman, officer, and section chief who had been recognized with the Vigil Honor and Founder’s Award — passed away in the early morning hours of August 17th of that year. Only nineteen years old at the time of his passing, Tom was about to enter his sophomore year at Penn State University, studying political science and history. An amazing friend, brother, and Scout, Tom will always be remembered by his friends as the one and only “Super Chief.”

The Thomas J. Richards Award for Outstanding Service is used to recognize those youth Arrowmen who do exactly that: serve their lodge, Unami, One, to an outstanding degree. Unselfish service and an exemplary performance of one's role in the lodge are the main factors considered by the selection committee.

<table class="table table-striped my-3 ">
  <thead>
    <tr>
      <th scope="col">Year</th>
      <th scope="col">Name</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.awards-youth-osa reversed %}
      <tr>
        <td>{{person.year}}</td>
        <td>{{person.name}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
