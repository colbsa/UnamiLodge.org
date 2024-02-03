---
title: Lodge Executive Committee
layout: page
permalink: /contactlist/
---
<h3 class="mt-5">Officers</h3>
<table class="table table-responsive table-striped mt-3">
  <thead>
    <tr>
      <th scope="col">Positon</th>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.lec.officers %}
      <tr>
        <td>{{person.title}}</td>
        <td>{{person.name}}</td>
        <td><a href="/contact?recipient={{person.email}}">{{person.email}}@unamilodge.org</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>
<h3 class="mt-5">Advisory Board</h3>
<table class="table table-responsive table-striped mt-3">
  <thead>
    <tr>
      <th scope="col">Positon</th>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    {% for person in site.data.lec.advisoryboard %}
      <tr>
        <td>{{person.title}}</td>
        <td>{{person.name}}</td>
        <td><a href="/contact?recipient={{person.email}}">{{person.email}}@unamilodge.org</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>
<h3 class="mt-5">Committees</h3>
<table class="table table-responsive table-striped mt-3">
  <thead>
    <tr>
      <th scope="col">Positon</th>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    {% for committee in site.data.lec.committees %}
      <tr class="table-active"><td colspan="3">{{committee.committee-name}}</td></tr>
      {% for member in committee.members %}
        <tr>
          <td>{{member.title}}</td>
          <td>{{member.name}}</td>
          <td><a href="/contact?recipient={{committee.email}}">{{committee.email}}@unamilodge.org</a></td>
        </tr>
      {% endfor %}
    {% endfor %}
  </tbody>
</table>
<h3 class="mt-5">Chapters</h3>
<table class="table table-responsive mt-3">
  <thead>
    <tr>
      <th scope="col">Positon</th>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    {% for chapter in site.data.chapters %}
      <tr class="table-active"><td colspan="3">{{chapter.chapter-name}}</td></tr>
      {% for officer in chapter.officers %}
        <tr>
          <td>{{officer.title}}</td>
          <td>{{officer.name}}</td>
          <td><a href="mailto:{{chapter.email}}@unamilodge.org">{{chapter.email}}@unamilodge.org</a></td>
        </tr>
      {% endfor %}
    {% endfor %}
  </tbody>
</table>
