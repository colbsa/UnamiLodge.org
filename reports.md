---
title: Lodge Reports & Minutes
layout: page

---

Each meeting of the Lodge Executive Committee is recorded through detailed minutes by the lodge secretary. Once approved by the LEC at the following meeting, a copy of the approved minutes will be uploaded to this page for all members to view.  Additionally, annual reports submitted to the Cradle of Liberty council board can also be found below.

<div class="card">
	<div class="card-header">
		Lodge Executive Committee Minutes
	</div>
	<div class="card-body">
		<ul>
			{% for report in site.data.reports.minutes %}
				<li><a href="{{report.url}}">{{report.title}}</a></li>
			{% endfor %}
		</ul>
	</div>
</div>
<div class="card my-3">
	<div class="card-header">
		Annual Reports
	</div>
	<div class="card-body">
		<ul>
			{% for report in site.data.reports.annual %}
				<li><a href="{{report.url}}">{{report.title}}</a></li>
			{% endfor %}
		</ul>
	</div>
</div>