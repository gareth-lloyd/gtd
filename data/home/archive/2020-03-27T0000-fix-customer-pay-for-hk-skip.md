---
area: null
contexts: []
created: &id001 2020-03-27 00:00:00
defer_until: null
due: null
energy: null
id: 2020-03-27T0000-fix-customer-pay-for-hk-skip
project: null
tags: []
time_minutes: null
title: fix customer pay for hk skip
updated: *id001
waiting_on: null
waiting_since: null
---

08:18
ERROR: test_cannot_skip_finished (work.tests.api.visits.test_skip_visit.SkipVisitRecordTests)
08:18
----------------------------------------------------------------------
08:18
Traceback (most recent call last):
08:18
  File "/home/rof/.pyenv/versions/2.7.17/lib/python2.7/unittest/case.py", line 329, in run
08:18
    testMethod()
08:18
  File "/home/rof/src/github.com/HousekeepLtd/housekeep/housekeep/work/tests/api/visits/test_skip_visit.py", line 244, in test_cannot_skip_finished
08:18
    self.visit_record, event_data=self.event_data
08:18
  File "/home/rof/.pyenv/versions/2.7.17/lib/python2.7/site-packages/django/utils/decorators.py", line 185, in inner
08:18
    return func(*args, **kwargs)
08:18
  File "/home/rof/src/github.com/HousekeepLtd/housekeep/housekeep/work/api/visits.py", line 1380, in _skip_visit_record
08:18
    if not is_conversion:
08:18
NameError: global name 'is_conversion' is not defined
08:18

08:18
======================================================================
08:18
ERROR: test_cannot_skip_skipped (work.tests.api.visits.test_skip_visit.SkipVisitRecordTests)
08:18
----------------------------------------------------------------------
08:18
Traceback (most recent call last):
08:18
  File "/home/rof/.pyenv/versions/2.7.17/lib/python2.7/unittest/case.py", line 329, in run
08:18
    testMethod()
08:18
  File "/home/rof/src/github.com/HousekeepLtd/housekeep/housekeep/work/tests/api/visits/test_skip_visit.py", line 231, in test_cannot_skip_skipped
08:18
    self.visit_record, event_data=self.event_data
08:18
  File "/home/rof/.pyenv/versions/2.7.17/lib/python2.7/site-packages/django/utils/decorators.py", line 185, in inner
08:18
    return func(*args, **kwargs)
08:18
  File "/home/rof/src/github.com/HousekeepLtd/housekeep/housekeep/work/api/visits.py", line 1380, in _skip_visit_record
08:18
    if not is_conversion:
08:18
NameError: global name 'is_conversion' is not defined