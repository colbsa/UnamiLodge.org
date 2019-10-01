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
          <td class="align-middle">{{event.title}}</td>
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

Unami Lodge also makes available a [long range calendar](/files/UnamiLodgeCalendar_2019-2022.pdf). Please note that dates and locations listed in the long range calendar are subject to change.
