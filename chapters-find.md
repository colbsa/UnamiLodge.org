---
title: Find My Chapter
layout: page
permalink: /chapters/find
---

A chapter is a smaller organizational unit of the lodge, much like a patrol is a smaller part of a troop. There are 11 chapters in Unami Lodge, One, that currently align with the different Scouting districts of the Cradle of Liberty Council. Each chapter has their own officers and adviser who look to support units in their implementation of lodge programming, and who represent those units at larger meetings of the lodge. Chapters meet monthly to discuss the happenings of the lodge and for members to join in fellowship.

The best way to find what chapter you belong to is learning from your troop. You can also try to learn by submitting the zipcode of your troop's meeting place below or by locating it on the map.

<form id="findchapterform" onsubmit="event.preventDefault();">
  <div class="form-group">
    <label for="zip">Zipcode</label>
    <input type="number" class="form-control col-3" name="zip" id="findchapterform-zip" placeholder="" value="" maxlength="5" required>
  </div>
</form>

<div class="alert alert-info fade" role="alert" id="alert-response" hidden>
  The zipcode you entered aligns with the chapters below. Either use the map to see which chapter you are in or contact one of the leaders from your unit or chapter.
  <ul id="findchapter-chapters"></ul>
</div>

<iframe src="https://www.google.com/maps/d/embed?mid=1cEJd5Fv4sfaouJ9mOJ66Hwj2l80&hl=en" width="100%" height="400" frameborder="0" class="mt-3"></iframe>

<script type="text/javascript">

chapters = {{ site.data.chapters | jsonify }};

const input = document.getElementById("findchapterform-zip");
const multiple_div = document.getElementById("alert-response");
const chapters_ul = document.getElementById("findchapter-chapters");
input.addEventListener('input', updateZip);

var chapters_matched =[];
var multi_chapter_output = "";

function updateZip(zip_input) {
  if(zip_input.target.value.toString().length > 4)
  {
    chapters.forEach(function(chapter) {
      chapter.zip.forEach(function(chapter_zip) {
        if (chapter_zip == zip_input.target.value)
          chapters_matched.push(chapter);
      });
    });

    if(chapters_matched.length === 1)
      window.location.href = "/chapters/" + chapters_matched[0]["email"];

    if(chapters_matched.length > 1)
    {
      chapters_matched.forEach(function(match) {
        multi_chapter_output += "<li><a href=\"/chapters/" + match["email"] + "\">" + match["chapter-name"] + "</a></li>";
      });

      chapters_ul.innerHTML = multi_chapter_output;
      multiple_div.removeAttribute("hidden");
      multiple_div.classList.add("show");
    }

    chapters_matched = [];
  };
}

</script>
