---
title: The Dave Fortunato Outstanding Service Award     
layout: page
permalink: /history/awards/adult-osa
---
The Dave Fortunato Outstanding Service Award was established by the Lodge Executive Committee in the fall of 1996. Dave was a long-time Scouter in the Valley Forge Council, an active campmaster, chapter adviser, and lodge adviser of Delmont Lodge #43. Following the merger of Unami 1 with Delmont Lodge, Dave was chosen as the first lodge adviser of the new lodge. Unfortunately, this Vigil Honor member and Founder’s Award recipient passed away on September 27, 1996. As someone who believed firmly in living by the Scout Oath and Law, and who abided by the Obligation in his daily life, Dave saw great promise in the new Unami Lodge, One.

Originally presented to youth and adult arrowmen alike, beginning in 2010 the Fortunato Award is presented to solely adult arrowmen. These individuals serve their lodge, Unami, One, to an outstanding degree. Unselfish service and an exemplary performance of one’s role in the lodge are the main factors considered by the selection committee.

<table class="table table-striped my-3 ">
  <thead>
    <tr>
      <th scope="col">Year</th>
      <th scope="col">Name</th>
      <th scope="col">Age</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.awards-adult-osa reversed %}
      <tr>
        <td>{{person.year}}</td>
        <td>{{person.name}}</td>
        <td>{{person.age}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
