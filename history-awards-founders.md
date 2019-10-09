---
title: The Founder&#39;s Award
layout: page
permalink: /history/awards/founders
---
Introduced at the 1981 National Order of the Arrow Conference, the Founder&#39;s Award recognizes Arrowmen who have given outstanding service to their lodge. The award is reserved for an Arrowman who demonstrates that he or she personifies the spirit of selfless service, as advocated by founder E. Urner Goodman and cofounder Carroll A. Edson.

While the Vigil Honor is a high mark of distinction, the Founders Award is used to recognize those Arrowmen, youth and adult, who have impacted the lodge in a positive and lasting way. This is a rare and distinguished honor, to recognize the spirit of our Founders in another. Lodges may petition the national Order of the Arrow committee to present between two and four awards annually, depending on the number of members in the lodge. If the lodge presents more than one award, at least one must be awarded to a youth under the age of 21.

The award is a handsome bronze medallion bearing the likenesses of E. Urner Goodman and Carroll A. Edson, with a wooden base and a brass plate suitable for engraving. Available for uniform wear is a gold-colored arrow suspended from a red ribbon.

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
    {% for person in site.data.awards-founders reversed %}
      <tr>
        <td>{{person.year}}</td>
        <td>{{person.name}}</td>
        <td>{{person.lodge}}</td>
        <td>{{person.age}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
