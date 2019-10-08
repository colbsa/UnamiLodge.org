/**
 * JavaScript Get URL Parameter
 * 
 * @param String prop The specific URL parameter you want to retreive the value for
 * @return String|Object If prop is provided a string value is returned, otherwise an object of all properties is returned
 */
function getUrlParams( prop ) {
  var params = {};
  var search = decodeURIComponent( window.location.href.slice( window.location.href.indexOf( '?' ) + 1 ) );
  var definitions = search.split( '&' );

  definitions.forEach( function( val, key ) {
      var parts = val.split( '=', 2 );
      params[ parts[ 0 ] ] = parts[ 1 ];
  } );

  return ( prop && prop in params ) ? params[ prop ] : params;
}

$(function() {
  var recipient = getUrlParams('recipient');
  var message = getUrlParams('message');
  if (recipient.length > 1){
    $("#contactform-recipient").replaceWith("<input type=\"text\" class=\"form-control\" name=\"recipient\" id=\"requested_email\" placeholder=\"\" value=\"" + recipient + "\" disabled required>")
    $("#contactform-card").remove();
    if (message.length > 1)
      $("#contactform-message").text(message);
  }
});

$("#contactform-recipient").change(function () {
  $("#recipient-name").text(this.value);
});

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
$("#contactform").validate({
  rules: {
    name: {
      required: true,
      minlength: 2
    },
    email: {
      required: true,
      email: true
    },
    recipient: {
      required: true,
    },
    message: {
      required: true,
      minlength: 5
    }
  },
  messages: {
    name: "Please tell us your name.",
    recipient: "Please select a recipient.",
    email: {
      required: "Please give us your email address.",
      email: "Please put your email address in the format of name@example.com"
    },
    message: "Please let us know what you want to say."
  },
  errorClass: "invalid",
  validClass: "valid",
  invalidHandler: function() {
    $("#contactform").addClass("was-validated");
  },
  submitHandler: function() {
    $("#contactform").addClass("was-validated");
    grecaptcha.execute();
  }
});
function ContactUs() {
  var alert_class = "alert-info";
  var alert_headline = "Loading...";
  var alert_text = "";
  ContactUsAlert(alert_class, alert_headline, alert_text)
  $("#contactform-name").prop('disabled', true);
  $("#contactform-email").prop('disabled', true);
  $("#contactform-recipient").prop('disabled', true);
  $("#contactform-message").prop('disabled', true);
  $("#contactform-send").prop('disabled', true);
  $.ajax({
    url: '/assets/custom/php/contact_engine.php',
    method: 'POST',
    dataType: 'json',
    data: $("#contactform :input"),
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
