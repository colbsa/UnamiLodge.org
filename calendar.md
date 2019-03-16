---
title: Lodge Calendar
layout: page

---
<div class="table-responsive">
  <table class="table table-striped mt-3">
    <thead>
      <tr>
        <th scope="col">Event</th>
        <th scope="col">Dates</th>
        <th scope="col">Location</th>
        <th scope="col">Registration</th>
      </tr>
    </thead>
    <tbody>
      {% for event in site.data.events %}
        <tr>
          <td class="align-middle">{{event.title}}</td>
          <td class="align-middle">{{event.dates}}</td>
          {% if event.location-url %}
            <td class="align-middle"><a href="{{event.location-url}}">{{event.location}}</a></td>
          {% else %}
            <td class="align-middle">{{event.location}}</td>
          {% endif %}
          {% if event.link-url %}
            <td class="align-middle"><a href="{{event.link-url}}" class="btn btn-primary">{{event.link-text}}</a></td>
          {% else %}
            <td class="align-middle">{{event.link-text}}</td>
          {% endif %}
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
