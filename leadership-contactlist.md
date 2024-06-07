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
        <td>{{person.email}}@unamilodge.org</td>
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
        <td>{{person.email}}@unamilodge.org</td>
      </tr>
    {% endfor %}
  </tbody>
</table>
<h3 class="mt-5">Committees</h3>
<table class="table table-responsive mt-3">
  <thead>
    <tr>
      <th scope="col">Positon</th>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
    </tr>
  </thead>
  <tbody>
    {% for committee in site.data.lec.committees %}
      <tr class="table-active"><td colspan="3"><h5 class="my-0">{{committee.committee-name}}</h5></td></tr>
      {% for member in committee.members %}
        <tr>
          <td>{{member.title}}</td>
          <td>{{member.name}}</td>
          <td>{{committee.email}}@unamilodge.org</td>
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
      <tr class="table-active"><td colspan="3"><h5 class="my-0">{{chapter.chapter-name}}</h5></td></tr>
      {% for officer in chapter.officers %}
        <tr>
          <td>{{officer.title}}</td>
          <td>{{officer.name}}</td>
          <td>{{chapter.email}}@unamilodge.org</td>
        </tr>
      {% endfor %}
    {% endfor %}
  </tbody>
</table>
