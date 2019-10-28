---
title: New Members
layout: page
permalink: /newmembers/
---

<div class="alert alert-success">
  <strong>Check it out!</strong> The <a href="/news/2019-New-Members-Bash">New Members' Bash</a> is quickly approaching!
  <a class="btn btn-primary" href="https://colbsa.doubleknot.com/event/2019-new-members-bash/2584306">Register Now!</a>
</div>

Congratulations! You’ve completed your Ordeal and are now a full member in Order of the Arrow, entitled to all the rights and privileges of membership. However, your journey in the Order of the Arrow is only just beginning. A world of opportunity is now open to you as a member of Unami Lodge, One. This page will help you as take the next steps on your membership journey and explore the wonders of the Order of the Arrow.

## Join in the Fellowship – Come Out to a Lodge Activity
From the beginning, you can continue your active membership in Unami Lodge, One by attending a variety of lodge activities, including:
- Lodge Service Weekends held each April & May. Come out and perform cheerful service at our council camps, meet fellow arrowmen, and participate in some awesome evening programs!
- Lodge Fellowship Weekends held in October. Perform a half day of cheerful service, and enjoy a fun-filled afternoon and evening of exciting activities! Also, come out and vote in the yearly Lodge Officer Elections.
- Section NE-5 Conclave held in early June. Each lodge in the section – the 10 lodges from the councils surrounding us – takes turns hosting this action-packed weekend of training, fellowship, and fun! The 2019 Section NE-5 Conclave’s theme is “Major League Brotherhood” and being held at Ockanickon Scout Reservation.
- Annual Dinner held every January. The oldest standing event in the Order of the Arrow, our lodge banquet highlights the accomplishments of all the members of the lodge throughout the year, recognizes the recipients of awards for outstanding and camp service, and begins the term of the new lodge officers.
- Community Service Day held in March. Held in three distinct areas throughout the council, the Community Service Day is a way for members of our lodge to give service to our local communities. Past locations have included Pennypack Park, Mount Moriah Cemetery, and the Valley Forge Medal of Honor Grove.
- Find out when all of these great events are happening on the [Lodge Calendar](/calendar), and sign-up to join in the fun & fellowship. Also, be on the look out for information about special events for new members!

## Chapter Information
As a member of Unami Lodge, One, you are also a member of a chapter – a smaller portion of our lodge – which corresponds to your district of the council. Each chapter has a chapter chief, a chapter vice chief, and a chapter secretary, as well as a chapter adviser. Each chapter holds monthly meetings and activities for its members. Chapters also are responsible for conducting unit elections in your home unit and assisting with camp promotions. <!-- To find out which chapter you belong to, more info about their meeting, and the latest news & updates, click [here](/chapters). -->

## Get Involved & Join a Committee
There are 15 operating committees of Unami Lodge, One, all eager for you to become a part of and help with. Read a brief description of the work that each committee does and click on the committee name to contact them and get involved!

{% for committee in site.data.committees %}
**{{committee.committee-name}}** - {{committee.responsibilities}}
{% endfor %}

### Seal the Bonds of Brotherhood
As an Ordeal member, your focus should be on providing leadership to your home unit. After 6 months as an Ordeal member, you have the opportunity to take the next step in your membership journey and become a Brotherhood member. As a Brotherhood member, your focus should shift to now serve the lodge as well, and providing leadership on the chapter or lodge level. You can become a Brotherhood member at any of our three lodge weekends, as well as at Resica Fall Scout Reservation during the summer. To sign-up and seal the bond, head over to the [Lodge Calendar](/calendar).

### Key Contacts
Questions? Head over to the [contact form](/contact) and ask one of our lodge committees, or contact one of the leaders of the lodge listed below.

{% assign key3_person = site.data.lec.officers | where:"key3", "true" %}
{% for person in key3_person %}
{{person.name}} - {{person.title}} - [{{person.email}}@unamilodge.org](/contact?recipient={{person.email}})
{% endfor %}
