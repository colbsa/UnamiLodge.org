---
title: The Centurion Award
layout: page
permalink: /history/awards/centurion
---
The Centurion Award was a one-time recognition associated with the centennial anniversary of the OA that was bestowed by the national Order of the Arrow committee. It was modeled after a similar program in the BSA’s 100th anniversary celebration, the 2010 National Hall of Leadership. The Centurion Award highlighted “Hometown Heroes,” or Arrowmen who have meaningfully contributed to the forming, maturing and ongoing operational excellence of their local council’s lodge, and who, in doing so, inspired others to follow in their footsteps. These honorees will serve as exemplars of leadership, modeling to others a commitment to cheerful service as the Order of the Arrow enters its second century.

<table class="table table-striped my-3 ">
  <thead>
    <tr>
      <th scope="col">Name</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.awards-centurion reversed %}
      <tr>
        <td>{{person.name}}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
