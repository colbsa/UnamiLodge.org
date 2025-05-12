---
title: Lodge Calendar
layout: page
permalink: /calendar/
---
<div class="table-responsive">
  <table class="table table-responsive table-striped mt-3" id="lodge-calendar">
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
          {% if event.post-url %}
            <td class="align-middle"><a href="{{event.post-url}}">{{event.title}}</a></td>
          {% else %}
            <td class="align-middle">{{event.title}}</td>
          {% endif %}
          <td class="align-middle">
          {% if event.date-end %}
            {% assign m = event.date | date: "%-m" %}
            {% assign n = event.date-end | date: "%-m" %}
            {% if m == n %}
              {{event.date | date: "%B %-d"}}-{{ event.date-end | date: "%-d, %Y"}}
            {% else %}
              {{event.date | date: "%B %-d"}} - {{ event.date-end | date: "%B %-d, %Y"}}
            {% endif %}
          {% else %}
            {{event.date | date: "%B %-d, %Y"}}
          {% endif %}
          </td>
          {% if event.location-url %}
            <td class="align-middle"><a href="{{event.location-url}}" target="_blank">{{event.location}}</a></td>
          {% else %}
            <td class="align-middle">{{event.location}}</td>
          {% endif %}
          {% if event.link-url %}
            <td class="align-middle"><a href="{{event.link-url}}" class="btn btn-primary" target="_blank">{{event.link-text}}</a></td>
          {% else %}
            <td class="align-middle">{% if event.link-text %}{{event.link-text}}{% else %}Coming Soon{% endif %}</td>
          {% endif %}
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

Unami Lodge also makes available a [long range calendar](/files/UnamiLodgeCalendar_2025-2028.pdf){:target="_blank"} [*Updated: May 12, 2025*]. Please note that dates and locations listed in the long range calendar are subject to change.
