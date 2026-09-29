---
area: null
completed_at: 2026-09-29 11:03:57.147787
contexts: []
created: 2026-09-29 04:32:39.632285
defer_until: null
due: null
energy: low
id: 2026-09-29T0432-reorganize-quote-builder-form
order: null
output: ''
project: 2026-05-25-villa-collective
source_id: null
tags: []
time_minutes: 5
title: reorganize quote builder form
updated: 2026-09-29 11:03:57.147774
waiting_on: null
waiting_since: null
working_on: false
---

* Reorganize the builder form
  * Form field UX
    * Follow flexibility ranges from enquiry. Displayed first as radio button block. 
    * Specific dates, +/- 3, +/-7, flexible
    * If specific dates selected, same behavior as “Search these exact dates”
    * Otherwise use arrival date range. 
    * Adults and children: use best UX practices for picking numeric values - radio buttons for reasonable values? 
    * Similarly, refine the country and region pickers. Ideally they wouldn’t require so many clicks to use, but most important to follow UX best practices. 
    * Min bedrooms, max bedrooms can re-use adults and children picker UX. 
    * Features can re-use picker improvements from country/region
  * Page state flow
    * arrive - form expanded, all controls available
    * Hit search: animated collapse of form to summary of inputs (readonly)
    * Simple UI to reopen the form to edit search (or cancel and go back to same results)
    *