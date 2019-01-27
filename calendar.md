---
title: Lodge Calendar
layout: page

---

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
				<td>{{event.title}}</td>
				<td>{{event.dates}}</td>
				<td>{{event.location}}</td>
				<td>{{event.link-text}}</td>
			</tr>
		{% endfor %}
	</tbody>
</table>