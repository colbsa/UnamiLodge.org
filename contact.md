---
title: Contact Us
layout: page

---

<form>
  <div class="row">
    <div class="col-md-6 mb-3">
      <label for="name">Name</label>
      <input type="text" class="form-control" id="name" placeholder="" value="" required>
      <div class="invalid-feedback">
        Valid name is required.
      </div>
    </div>
    <div class="col-md-6 mb-3">
      <label for="email">Email</label>
      <input type="email" class="form-control" id="email" placeholder="" value="" required>
      <div class="invalid-feedback">
        Valid email is required.
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-md-6 mb-3">
      <label for="recipient">Recipient</label>
      <input type="text" class="form-control" id="recipient" placeholder="" value="" required>
      <div class="invalid-feedback">
        Please enter a recipient.
      </div>
    </div>
    <div class="col-md-6 mb-3">
      <label for="subject">Subject</label>
      <input type="text" class="form-control" id="subject" placeholder="" value="" required>
      <div class="invalid-feedback">
        Please enter a subject.
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <label for="message">Message</label>
      <textarea class="form-control" id="message" placeholder="" required></textarea>
      <div class="invalid-feedback">
        Please enter a message.
      </div>
    </div>
  </div>
</form>
