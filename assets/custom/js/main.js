// Adds highlight for current time of the year
// Used in about-calendar.md
var today = Date.now();
var today_row = "<tr><td class=\"align-middle text-center\" colspan=\"4\">Coming Up!</td></tr>"
$(".date-end", "#lodge-calendar").each(function() {
  var date = Date.parse($(this).text());
  if (date > today) {
    $(this).parent('tr').before(today_row);
    return false;
  }
});