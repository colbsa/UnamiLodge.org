function ContactUsAlert(alert_class, alert_headline, alert_text) {
  $("#alert-response").removeClass("alert-info");
  $("#alert-response").removeClass("alert-warning");
  $("#alert-response").removeClass("alert-danger");
  $("#alert-response").addClass(alert_class);
  $("#alert-headline").text(alert_headline);
  $("#alert-text").text(alert_text);
  $("#alert-response").removeClass("hidden")
  $("#alert-response").addClass("show")
}
$("#contact-form").validate({
  rules: {
    name: {
      required: true
    },
    email: {
      required: true,
      email: true
    },
    message: {
      required: true
    }
  },
  messages: {
    name: "Please tell us your name.",
    email: {
      required: "Please give us your email address.",
      email: "Please put your email address in the format of name@domain.com"
    },
    message: "Please let us know what you want to say."
  },
  submitHandler: function() {
    grecaptcha.execute();
  }
});
function ContactUs() {
  var alert_class = "alert-info";
  var alert_headline = "Loading...";
  var alert_text = "";
  ContactUsAlert(alert_class, alert_headline, alert_text)
  $("#forminput_name").prop('disabled', true);
  $("#forminput_email").prop('disabled', true);
  $("#forminput_message").prop('disabled', true);
  $("#forminput_send").prop('disabled', true);
  $.ajax({
    url: '_inc/ContactUs_Engine.php',
    method: 'POST',
    dataType: 'json',
    data: $("#contact-form :input"),
    success: function(data) {
      if(data['success'] == true)
      {
        alert_class = "alert-success";
        alert_headline = "Thank you!";
        alert_text = "You should be hearing from a member of our team shortly.";
      }
      else
      {
        alert_class = "alert-danger";
        alert_headline = "Uh-Oh!";
        alert_text = data['error'];
      }
      ContactUsAlert(alert_class, alert_headline, alert_text);
    },
    error: function(data) {
      alert_class = "alert-danger";
      alert_headline = "Woops!";
      alert_text = "Sorry, but it looks like something has gone wrong. Please try again later.";
      ContactUsAlert(alert_class, alert_headline, alert_text);
    }
  });
};
