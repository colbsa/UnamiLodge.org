---
---

chapters = {{ site.data.chapters | jsonify }};

form_responses = {
    multiple: {
      text: ", the zipcode you entered aligns with the chapters below. Either use the map to see which chapter you are in or contact one of the leaders from your unit or chapter.",
      alert_class: "alert-info"
    },
    error: {
      text: ", the zipcode you entered is not registered in this Council or Lodge. Please verify your zipcode and try again.",
      alert_class: "alert-warning"
    }
  }
  
  const input = document.getElementById("findchapterform-zip");
  const alert_div = document.getElementById("alert-response");
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
  
      else if(chapters_matched.length > 1)
      {
        multi_chapter_output = "<ul>";
        chapters_matched.forEach(function(match) {
          multi_chapter_output += "<li><a href=\"/chapters/" + match["email"] + "\">" + match["chapter-name"] + "</a></li>";
        });
        multi_chapter_output += "</ul>";
  
        alert_div.innerHTML = "<strong>" + zip_input.target.value.toString() + "</strong>"
                            + form_responses.multiple.text
                            + multi_chapter_output;

        alert_div.classList.remove(form_responses.error.alert_class);
        alert_div.classList.add(form_responses.multiple.alert_class);
      }

      else if(chapters_matched.length < 1)
      {
        alert_div.innerHTML = "<strong>" + zip_input.target.value.toString() + "</strong>"
                              + form_responses.error.text;
        alert_div.classList.remove(form_responses.multiple.alert_class);
        alert_div.classList.add(form_responses.error.alert_class);
      }
  
      alert_div.removeAttribute("hidden");
      chapters_matched = [];
    };
  }