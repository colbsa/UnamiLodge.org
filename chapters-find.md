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

<span id="alert-response"></span>

<iframe src="https://www.google.com/maps/d/embed?mid=1cEJd5Fv4sfaouJ9mOJ66Hwj2l80&hl=en" width="100%" height="400" frameborder="0" class="mt-3"></iframe>

<script type="text/javascript">

chapters = {{ site.data.chapters | jsonify }};

const input = document.querySelector('input');
input.addEventListener('input', updateValue);

var chapters_matched =[];
var multiple_text = "The zipcode you entered aligns with the chapters below. Either use the map to see which chapter you are in or contact one of the leaders from your unit or chapter.";

function updateValue(e) {
  if(e.target.value.toString().length > 4)
  {
    for (var i=0; i < chapters.length; i++)
    {
      for (var j=0; j < chapters[i]["zip"].length; j++)
      {
        if (chapters[i]["zip"][j] == e.target.value)
        {
          chapters_matched.push(chapters[i]);
        }
      }
    }
    if(chapters_matched.length === 1)
      window.location.href = "/chapters/" + chapters_matched[0]["email"];
    if(chapters_matched.length > 1)
    {
      var alert_div = document.getElementById("alert-response");
      alert_div.innerHTML = "<div class=\"alert alert-info hidden\" role=\"alert\" id=\"alert-response\">"
      + multiple_text
      + "<ul><li><a href=\"/chapters/"
      + chapters_matched[0]["email"]
      + "\">"
      + chapters_matched[0]["chapter-name"]
      + "</a></li><li><a href=\"/chapters/"
      + chapters_matched[1]["email"]
      + "\">"
      + chapters_matched[1]["chapter-name"]
      + "</a></li></ul></div>";
    }
  };
}

</script>
