---
area: null
contexts: []
created: &id001 2018-09-10 00:00:00
defer_until: null
due: null
energy: null
id: 2018-09-10T0000-fix-mailchimp-unsubscribe
project: null
tags: []
time_minutes: null
title: fix mailchimp unsubscribe
updated: *id001
waiting_on: null
waiting_since: null
---

Catch and ignore
EventResponseProcessingError: Event update by None in marketingsite on verity.stroud@googlemail.com wants to receive marketing emails at 2018-09-01 18:33:55.311140+00:00 failed: respond_to_contact_preference_created_or_updated() call failed due to Mailchimp to make call to https://us3.api.mailchimp.com/3.0/lists/774d52726a/members/66787ff5e00ee6ffe8c56652f4ac3739 with payload {u'instance': u'd8661a2e-eee8-4b99-9778-0a646ddd3e3c', u'status': 400, u'detail': u'verity.stroud@googlemail.com is in a compliance state due to unsubscribe, bounce, or compliance review and cannot be subscribed.', u'type': u'http://developer.mailchimp.com/documentation/mailchimp/guides/error-glossary/', u'title': u'Member In Compliance State'} failed with status 400: verity.stroud@googlemail.com is in a compliance state due to unsubscribe, bounce, or compliance review and cannot be subscribed.