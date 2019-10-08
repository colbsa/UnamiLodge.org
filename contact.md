---
title: Contact Us
layout: page

---

<form id="contactform" onsubmit="event.preventDefault();" novalidate>
  <div class="row">
    <div class="col-md-6">
      <div class="form-group">
        <label for="name">Name</label>
        <input type="text" class="form-control" name="name" id="contactform-name" placeholder="" value="" required>
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" class="form-control" name="email" id="contactform-email" placeholder="" value="" required>
      </div>
      <div class="form-group">
        <label for="recipient">Recipient</label>
        <div class="input-group">
          <select class="form-control" name="recipient" id="contactform-recipient" required>
            <option value="">Select One</option>
            <option value="membership">Membership</option>
            <option value="events">Events</option>
            <option value="ordeal">Ordeal</option>
            <option value="brotherhood">Brotherhood</option>
            <option value="service">Service</option>
            <option value="unitelections">Unit Elections</option>
            <option value="communications">Communications / Other</option>
          </select>
          <div class="input-group-append">
            <div class="input-group-text">@UnamiLodge.org</div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <div class="form-group">
        <label for="message">Message</label>
        <textarea class="form-control" name="message" id="contactform-message" rows="12" required></textarea>
      </div>
      <div class="g-recaptcha"
        data-sitekey="{{ site.recaptcha }}"
        data-callback="ContactUs"
        data-size="invisible">
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary btn-block" id="contactform-send">Send</button>
      </div>
      <div class="alert alert-info fade hidden" role="alert" id="alert-response">
        <strong id="alert-headline"></strong> <span id="alert-text"></span>
      </div>
    </div>
  </div>
</form>

For more options, a complete list of Unami Lodge Leadership is available on our [Contact List Page](contactlist).
