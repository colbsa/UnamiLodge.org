---
title: The Charles J. &quot;Chuck&quot; Benshetler Spirit of Camp Leadership Award
layout: page
permalink: /history/awards/camp-leadership
---
Charles J. &quot;Chuck&quot; Benshetler was a Vigil Honor member of Unami Lodge, One, serving for decades on the staffs of Philadelphia and Cradle of Liberty Council camps. Chuck served in a multitude of positions during that time, including as both camp director and camp ranger at Treasure Island Scout Reservation. Chuck always set an example to the staff and tried to improve the camp in any way that he could. It is in his memory and legacy that Unami Lodge, One recognizes members of the Order of the Arrow and camp staff which exemplify the same spirit of camp leadership.

The Charles J. &quot;Chuck&quot; Benshetler Spirit of Camp Leadership Award is used to recognize those members of the Cradle of Liberty Council summer camp staff who exemplify the best qualities that a camp staff member should possess. Like Chuck, these individuals are always thinking about what is best for each Scout camper, and are always trying to improve camp through their selfless actions; it is through their words and actions that these individuals are seen by their fellow staff members and put in a position for recognition. Whether it is promoting the proper uniform, leading a song at meals, helping a Scout learn a new skill, or keeping morale high among the staff, the individuals honored with this award are always there to cheerfully take on such tasks, just as Chuck would have done.

<table class="table table-responsive table-striped my-3 ">
  <thead>
    <tr>
      <th scope="col">Year</th>
      <th scope="col">Name</th>
      <th scope="col">Camp</th>
      <th scope="col">Lodge</th>
      <th scope="col">Youth/Adult</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.awards-benshetler reversed %}
      <tr>
        <td>{{person.year}}</td>
        <td>{{person.name}}</td>
        <td>{{person.camp}}</td>
        <td>{{person.lodge}}</td>
        <td>{{person.age}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
