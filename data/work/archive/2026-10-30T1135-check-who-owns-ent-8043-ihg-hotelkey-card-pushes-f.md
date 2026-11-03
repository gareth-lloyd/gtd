---
area: null
completed_at: 2026-10-30 14:13:25.300407
contexts:
- react
created: 2026-10-30 11:35:30.503819
defer_until: null
due: null
energy: medium
id: 2026-10-30T1135-check-who-owns-ent-8043-ihg-hotelkey-card-pushes-f
order: null
output: |
  ## Agent run 2026-10-30T13:09:30+02:00

  **Nobody owns ENT-8043 (https://linear.app/canary-technologies/issue/ENT-8043/ihg-hotelkey-card-push-returns-401-not-authorized-at-11-hotels).** It is In Progress in the Enterprise team, with no assignee and no priority. The test fix also failed, and nobody has noted that on the ticket.

  **Who has touched it**
  - Andrea Bradshaw filed it on 10-28 and said she would verify the test fix. Her last comment was 10-28 21:26 UTC.
  - rcuadra is the only person who has changed config (their Linear account shows only that handle). They found all the listed hotels have the username set to the Property ID instead of canary-<hotel code>, and changed ihg-nycpv only, as a test, on 10-28 21:05 UTC. They have not commented since.
  - Martin Mineo declined it on 10-29: he tracks HotelKey for BW only and has no list of IHG issues. He also listed 7 other IHG hotels with rejected webhooks, which may need the same cleanup.
  - Taylor Kirchwehm is not on the ticket but says the master credentials sheet is the source of truth, and that errors with those credentials should go to HotelKey (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793285908878999?thread_ts=1793285908.878999&cid=C03V5P4B48P).
  - Boybit Ruiz added another failed sync from ihg-dabhi on 10-29 22:41 UTC (Zendesk https://canarysupport.zendesk.com/tickets/214603).
  - The ticket moved to Configuration on 10-29 12:21 UTC and In Progress at 13:57 UTC. Linear's history doesn't show who moved it.

  **Test fix failed (not on the ticket)**
  ihg-nycpv got NOT_AUTHORIZED on add-source after the username change: once between 14:00 and 17:00 UTC on 10-29, and again at 23:00:37 UTC. Either the username was not the cause, or the change did not stick. I did not check the current config value, so a revert is not ruled out.

  **Still failing, 10-29 11:00 to 10-30 11:00 UTC (Groundcover, NOT_AUTHORIZED on add-source, attempts not unique cards)**
  - 64 failures at 10 of the 11 hotels: voco Folkestone 14, Daytona 12, Chester 10, Garner Norman 10, Calgary 6, Lexington 4, Denver 3, Plainview 2, Edmond 2, Oklahoma City 1. Dodge City had none.
  - No hotel outside the ticket's list had this failure, so it does not appear to be spreading.
  - The latest failure was voco Folkestone at 10:26 UTC today.
  - I did not count successes in this window, so "every push fails" is confirmed only from the ticket's own table (24h to 10-28 20:00 UTC).

  **Link to Sharon's report: raised, not proven**
  - Sharon Hales posted ENT-8043 herself in the #ihg thread when Taylor asked for an example of migrations being overwritten (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793292085167699?thread_ts=1793285908.878999&cid=C03V5P4B48P). So she does treat it as a case of that.
  - Nobody has shown an overwrite. Her follow-up is a question: are existing integrations being given new credentials from the sheet? It has no reply in what I read.
  - The ticket conflicts with rcuadra's finding: its description says Canary config was correct at 7 hotels, while rcuadra says the usernames are wrong at all of them.

  **Recommendation**
  Assign it to rcuadra, as the only person who has worked the config, with Taylor taking the HotelKey escalation. Compare the 11 hotels against the master sheet and check the ihg-nycpv username is still the changed value. If it is, send the list to HotelKey to confirm the accounts are active, which is the ticket's own fallback. Do not roll the username change out to the other 10 until then. Set a priority: cards are not reaching HotelKey, and a hotel has already raised a support ticket.

  **Draft Linear comment on ENT-8043 (not posted, needs your yes):**
  > The ihg-nycpv username change hasn't fixed it. Add-source still returned 401 NOT_AUTHORIZED after the change, most recently on 10-29 at 23:00 UTC. Across the list there were 64 failures at 10 of the 11 hotels in the 24h to 10-30 11:00 UTC, and none at hotels outside the list. Can someone check the ihg-nycpv username is still the changed value and compare the list against the master credentials sheet? If they match, this needs to go to HotelKey. This ticket also has no assignee: @rcuadra, can you take it, with Taylor on the HotelKey side?

  Nothing was changed in Linear, Slack or any config.

  ## Agent run 2026-10-30T13:31:44+02:00 (MCP investigation)

  **Conclusion: this is a long-running credential or account problem at a small set of hotels, not a recent overwrite and not a code regression.** The exact cause is still open because the production config read was blocked.

  **Evidence (Groundcover, add-source requests to HotelKey; counts are attempts, not unique cards)**
  - Isolated: in the 7 days to 10-30 11:00 UTC, IHG hosts returned 4,672 200s across 417 hotels and 468 401s across 15 hotels.
  - No successes: the 11 hotels on the ticket had zero 200s from 10-09 to 10-30. Earlier history is unknown, because the 10-02 to 10-09 query timed out.
  - Long-running: 9 of the 11 were already failing between 10-09 and 10-15. Plainview's first logged failure is 10-20 and Daytona's is 10-19.
  - Not PMS-11184: the encrypted-password cutover (fd238b7c42a, 10-21) came after failures had started, and 417 hotels still succeed.

  **Overwrite theory: weakened, not ruled out**
  - Sharon Hales said the migration credentials were added "last week", but 9 of these hotels were failing by 10-15, and none shows a working period since 10-09. An overwrite before 10-09 would not show up here.
  - Admin saves to HotelKey configs from 10-26 to 10-30 were only Hollister and Plainview (below). Scripts don't go through admin, so this says nothing about them.

  **Plainview vs Hollister (the most useful lead)**
  - Hollister (config 16561): admin save by user 1513 at 10-28 14:22:44 UTC. Last 401 was 14:21:53, first 200 was 14:22:53. Its username fix worked at once.
  - Plainview (config 14616): admin save by user 61 at 10-28 20:58:19 UTC, about 7 minutes before rcuadra's comment. The same admin path triggered follow-on Celery work, and there were no later admin saves, so an admin revert is unlikely. It still returned 401 on 10-29.
  - So the username alone was not enough at Plainview. Hypotheses, neither tested: the password also doesn't match, or the HotelKey account is not active. The 401 itself can't tell these apart.
  - User 61 also used the HotelKey admin reveal-secret at 10-29 13:07 UTC. That may mean someone was still working this on 10-29. I did not map user 61 to a person or see which config it was for.

  **Why these hotels otherwise look healthy (from code)**
  add-source uses the username and password in HotelKeyThirdPartyClient (backend/pms-gateway/vendors/integrations/hotelkey/clients/thirdparty/client.py). Inbound webhooks check the separate webhook_username (services/event.py). That fits Martin's finding of no webhook rejections at these hotels. A bad API credential can therefore go unnoticed until a card push fails.

  **Corrections to my earlier run**
  - "No hotel outside the list" held for the last 24h only. Over 7 days, 4 more hotels had 401s: Panama City-Tyndall (18, last 10-29 00:51 UTC), Spring-The Woodlands (12, last 10-27), Lincoln North East (4, last 10-26), and Hollister (18, now fixed). From 10-16 to 10-30 the first three had zero 200s, so they probably belong on the ticket.
  - Dodge City's absence from the last 24h does not mean it recovered. It had zero 200s, and its last push was a 401 on 10-28.
  - "Every push fails" is now confirmed for the 11 hotels from 10-09, not just from the ticket's table.

  **Not done**
  - Production config check: canary prod-db was denied by the auto-mode classifier as a production read, and I did not re-route it through another tool. The read-only queries classify the username shape without returning usernames or passwords: /private/tmp/claude-501/-Users-garethlloyd-projects-canary/f9d58053-af9c-4d9a-922f-9692cdacdc6d/scratchpad/hk.sql (affected hotels) and /private/tmp/claude-501/-Users-garethlloyd-projects-canary/f9d58053-af9c-4d9a-922f-9692cdacdc6d/scratchpad/hk2.sql (all hotels). hk2 would show whether working IHG hotels use the canary-<code> username, which is the fastest test of rcuadra's finding.
  - Master sheet comparison: I don't have access to the sheet.

  **Updated next step**
  Don't bulk-apply the username change. Have the owner compare both username and password for Plainview against the master sheet. If they match, or if correcting them still gives a 401, send the 14 hotels still affected to HotelKey to confirm the accounts are active. The owner recommendation is unchanged.

  **Updated draft Linear comment on ENT-8043 (replaces the earlier draft; not posted, needs your yes):**
  > Update from the logs. The ihg-nycpv username change saved on 10-28 at 20:58 UTC, but add-source still returned 401 on 10-29, so the username alone didn't fix it. Hollister's username fix worked within a minute, so please check the ihg-nycpv password and account status too before applying this to the others.
  > None of the 11 hotels has had a successful add-source since at least 10-09, and 9 were already failing by 10-15, so this predates last week's migration credentials and the 10-21 password change. It is isolated: 15 hotels had 401s in the last 7 days, against 417 with successes.
  > Three more hotels had 401s and no successes from 10-16: Panama City-Tyndall, Spring-The Woodlands and Lincoln North East.
  > This still has no assignee: @rcuadra, can you take it, with Taylor on the HotelKey side?

  Nothing was changed in Linear, Slack or any config.

  ## Agent run 2026-10-30T14:11:58+02:00 (Sharon's theory)

  **Verdict: the mechanism is real, but it doesn't explain these 11 hotels as described. Not proven either way.**
  - Mechanism exists: HotelKeyConfigurationService.upsert_configuration (backend/pms-gateway/vendors/integrations/hotelkey/services/configuration.py) copies username and password onto an existing config. The onboarding HotelKey schema (backend/canary/onboarding/configuration_providers/integrations_schemas/hotelkey.py) carries HotelKey credential fields. I did not trace the full call path from onboarding to this upsert. These writes would not appear in the admin-save logs I checked.
  - Against, for these hotels: no 200s from 10-09 to 10-30, so they show no working period to be overwritten since 10-09, and 9 were failing by 10-15, before the credentials she says were added "last week".
  - Gaps: an overwrite before 10-09 is not excluded. Admin saves were checked for 10-26 to 10-30 only. Plainview and Daytona have no logged pushes before 10-20 and 10-19, so their timing is not informative. She may have other hotels in mind, as she gave this ticket as her only example.
  - Possible support, inference only: rcuadra found the same wrong username pattern at all the listed hotels, which looks like one bulk source rather than hand entry. That source could equally be the original setup, not an overwrite.
  - What would settle it: gateway config created_at and updated_at for the 11 hotels (in hk.sql, blocked), and any earlier successful pushes in Snowflake or older logs. updated_at after a hotel's last success would support her. No success ever would rule it out for that hotel.

  ## Agent run 2026-10-30T14:34:25+02:00 (OnboardingScriptBatch evidence)

  **Verdict: no evidence that a script overwrote these hotels' credentials, and good evidence against it since at least 10-05. The opposite may be true: scripts may have left old credentials in place. That is a hypothesis until the shell output is back.**

  **Sources:** Snowflake is unavailable (role has no access to CANARY_RAW or the gateway HotelKey table). Canary MCP run_sql needs a Workup run ID, which I don't have, and the MCP returned "session not found". Evidence is from code and Groundcover.

  **Code (backend/canary/onboarding/plans)**
  - create_pms_configuration skips a HotelKey config that already exists: configure_pms_integration_create_configuration_plan.py upserts only when existing_config is None.
  - update_pms_configuration does overwrite: configure_pms_integration_update_configuration_plan.py upserts when a config exists. Each write hits PUT /api/accounts/hotelkey, and the gateway logs upsert_configuration.diff.
  - So a standard Configure PMS batch cannot replace credentials. Only an Update PMS batch, a direct API call or an admin save can.

  **Logs**
  - No upsert_configuration.diff for any of the 15 affected hotels (11 on the ticket, Hollister, Panama City-Tyndall, Spring-The Woodlands, Lincoln North East) from 09-20 to 10-30.
  - The control passed: the same event shows IHG-named hotels being written on 10-28 by the IHG GMS Core Configure PMS batches, with matching PUTs. In 09-20 to 10-09 it shows 5 such writes, but none before 10-05, so coverage before 10-05 is weaker. I did not separately confirm the event for EU hotels such as voco Folkestone.
  - Batches do touch these hotels without changing credentials: Panama City-Tyndall got PATCH /api/accounts/me and hotelkey/validate on 10-28 from 21:30 UTC, with no diff. The timing lines up with IHG GMS Core batches 99702 and 99712, but that link is inferred, and its 401s continued afterwards.
  - Other writes seen: an admin account save at voco Folkestone on 10-27 and at Panama City-Tyndall on 10-28, on /canary-admin/gateway/account/. Those are account pages; I don't know what they changed.
  - The admin HotelKey saves checked earlier cover 10-26 to 10-30 only. Admin history before that is in the gateway snippet below.

  **New hypothesis**
  These configs existed before the master sheet credentials and were never updated, because Configure PMS skips existing configs. That would fit rcuadra's finding of a Property ID username, the absence of writes, and failures with no working period. It would also mean the fix is an Update PMS batch or corrected values, not a one-off username edit, but Plainview still has to be explained, since its username edit did not clear the 401.

  **Shell snippets (read-only, print shapes and dates, never credential values; not yet run)**
  - /private/tmp/claude-501/-Users-garethlloyd-projects-canary/f9d58053-af9c-4d9a-922f-9692cdacdc6d/scratchpad/ent8043_canary_shell.py: batches and runs per hotel, who ran them, vendor_config_upserted, sheet value dates and username shape.
  - /private/tmp/claude-501/-Users-garethlloyd-projects-canary/f9d58053-af9c-4d9a-922f-9692cdacdc6d/scratchpad/ent8043_gateway_shell.py: config created and updated dates, username shape, admin change history including who.
  Reading the result: a config updated after a hotel's Update PMS run, or with an admin change to credentials, supports Sharon. A sheet shape of canary-code with a gateway shape of property_id, and vendor_config_upserted false, supports the hypothesis above. These were syntax-checked only, because I can't run them here. Slugs and property codes assume the code is the slug's uppercase suffix.

  The draft Linear comment is still unposted. Hold it until the shell output is back, because its diagnosis may change.

  ## Agent run 2026-10-30T14:44:14+02:00 (Canary shell output, US)

  **Verdict: Sharon's overwrite theory is not supported for the 8 hotels with batch history. Leading explanation: the 10-16 sheet refresh never reached configs that already existed, because Configure PMS skips them. Likely but not proven; the gateway output is still needed.**

  **What the output shows**
  - 8 of 10 US hotels have batches, and all are create_pms_configuration, run by tkirchwehm. None has an update_pms_configuration batch. Some hotels ran Configure PMS two or three times (Garner Norman 3; Daytona, Edmond, Plainview, Calgary 2; plus a pending batch at Daytona).
  - All 8 hotels' sheet values have username shape canary-code and were last updated 2026-10-16 15:05, which looks like a bulk import. rcuadra found Property ID usernames in the gateway, so the sheet and gateway appear to differ. I don't know what the 10-16 import changed.
  - Dodge City and Chester have no PMS batches, so those configs came some other way, possibly by hand. My snippet could not look up their sheet values, because it finds them through batch identifiers.
  - Not in this run: ihg-lyxcf (needs the EU shell) and ihg-hlisr (slug not found, and not needed).

  **Bug in my snippet**
  vendor_config_upserted=None means not found, not false. Run results store plan_results as a list, and the first version did not search lists. Fixed in ent8043_canary_shell.py; a re-run will show true or false.

  **Why this looks like an overwrite but may not be**
  First logged 401s follow Configure PMS runs: Plainview run 10-20 12:56, first 401 13:11; Edmond run 10-13 14:13, first 401 14:38; Daytona run 10-19 11:56, first 401 21:53. Each run sets is_tokenizing_with_hotel_payment_gateway on the check-in config (onboarding/configuration_providers/hotel_key_tokenization.py) if a payment gateway exists. That may be what starts card pushes, which would expose bad credentials rather than cause them. I did not trace that flag to add-source, and these first 401s may just be the first pushes after go-live. Calgary already had 401s between 10-09 and 10-14, so it does not fit this pattern neatly.

  **It would also explain Plainview**
  rcuadra's comment says they changed the username. If the password is also stale, a username-only change would still return 401. Hollister differed because only its username was wrong. Untested.

  **Recommended test (a production write, for the owner, not done by me)**
  At Plainview only, set the password from the master sheet, then check the next add-source result. If it returns 200, apply both username and password across the list.
  Caution: AccountService.__upsert_configuration in the gateway disables the config after every upsert, and invalidates validations when fields change. I found no re-enable in the Update PMS plan. So a bare Update PMS batch could take a hotel's integration offline until it is validated and re-enabled. Confirm the batch's plan list before using it for this.

  **Limits**
  The snippet only covers create, update and switch batch types with a linked hotel, so custom batches, rows with no hotel and direct shell writes would not appear. Log evidence before 10-05 is weak: the new Groundcover retention note says about 31 days, although my July query did return rows. The September runs that probably created these configs are outside that coverage.

  **Still needed**
  - ent8043_gateway_shell.py in the US and EU gateway shells: created and updated dates, gateway username shape, and admin history including who. A created date near the September runs, an updated date before 10-16 and a property_id shape would confirm the explanation.
  - ent8043_canary_shell.py re-run for vendor_config_upserted, plus an EU run for voco Folkestone.

  Draft Linear comment still unposted, and still on hold until the gateway output is back.

  ## Agent run 2026-10-30T14:45:39+02:00 (gateway shell output, US)

  **Verdict: Sharon's overwrite theory is not supported at the 10 US hotels. Calgary has one unexplained update, but it was already failing before it. Username alone is not the fix: 3 hotels with the canary-code username still got 401s. Next suspects are the password or the HotelKey account.**

  **Overwrite check**
  - 7 configs were created in the same minute as their first Configure PMS run, on 09-04, 09-09 or 09-28: Daytona, Denver, Plainview, Edmond, Lexington, Garner Norman, Oklahoma City.
  - Later Configure PMS runs did not touch them. Daytona, Edmond, Garner and Plainview have no update at their October run times.
  - Chester (created 05-05) and Dodge City (created 06-10) predate the sheet and have no batches. Their last updates were 05-05 and 07-10.
  - Admin history shows only two credential edits on these configs, both username-only: Plainview by rcuadra on 10-28 and Hollister by Lei Ferretti (lferretti) on 10-28. These also identify user 61 and user 1513.
  - Exception: Calgary was updated on 10-19 at 12:02 UTC, about 6 minutes after a Configure PMS run, with no admin entry and no upsert_configuration.diff, so I can't say what changed. It was already failing from 10-09 to 10-14, so this did not break a working hotel.
  - updated_at changes on any save, so the unexplained September updates (Edmond and Lexington 09-14, Oklahoma City 09-28, Garner 09-29) may be enabling steps. All predate the logged failures. Garner has an admin enable on 09-25, but not at its last update time.

  **Username shape**
  - property_id (7): Daytona, Denver, Edmond, Chester, Lexington, Oklahoma City, Garner Norman.
  - canary-code (4): Dodge City, Calgary, Plainview (after the edit), Hollister (after the edit).
  - rcuadra's finding that all listed hotels have the Property ID username is not correct for Dodge City and Calgary. Both have canary-code and still had 401s.
  - Hollister works and Plainview doesn't, with the same username shape. Hollister's config was created on 10-22, after the 10-16 sheet refresh, and Plainview's on 09-04. That fits a stale password at Plainview, but does not prove it, and an inactive account would look the same.

  **Likely sequence (inferred)**
  September Configure PMS runs created configs from the sheet as it was then, which probably held Property ID usernames. The sheet shows canary-code now, and its last update was 10-16. Configure PMS skips existing configs, so the refresh never reached them. Failures predate 10-16, so the refresh did not cause them.

  **Corrections**
  - The 10-29 13:07 reveal-secret by user 61 does not appear on any of these 11 configs, so it does not show rcuadra was working this ticket then. Disregard my earlier reading.
  - Connor Swords (cswords) exported password and webhook_password to a file for all 11 on 10-27 at 18:49 UTC. It is logged as an export and did not change updated_at. I don't know the purpose.

  **Next steps**
  1. Run /private/tmp/claude-501/-Users-garethlloyd-projects-canary/f9d58053-af9c-4d9a-922f-9692cdacdc6d/scratchpad/ent8043_gateway_shapes.py in the gateway shell. Nothing yet shows whether working IHG hotels also use property_id usernames. If they do, the username shape is not the problem. The 40 account UUIDs can be checked for 200s in Groundcover.
  2. Owner tests at Plainview: set the password from the master sheet, and watch the next add-source. Calgary is a second candidate. Dodge City has had no push since 10-28, so it would be slow to confirm.
  3. If a 200 follows, apply username and password together across the list. If 401 continues, send the list to HotelKey to check the accounts.
  Still not checked: voco Folkestone (EU).

  **Updated draft Linear comment on ENT-8043 (replaces earlier drafts; not posted, needs your yes):**
  > Findings from logs and config history. Changing the username won't be enough on its own: ihg-yycba, ihg-ddcsx and ihg-nycpv (since 10-28) already use canary-<code> and still got 401s. Hollister works with that format, but its config was created on 10-22, after the 10-16 sheet refresh. ihg-nycpv's was created on 09-04, and only its username has been edited.
  > So please check the ihg-nycpv password against the master sheet next. If it differs, set it and watch the next card push. If it matches, or the 401 continues, this list needs to go to HotelKey to confirm the accounts are active.
  > I found no sign that these credentials were overwritten by a script. None of the 10 US hotels has an Update PMS batch, Configure PMS skips existing configs, and the logs show no script writes to them since at least 10-05. ihg-yycba has one unexplained update on 10-19, but it was already failing before that. A few configs also have unexplained September updates, before the logged failures. ihg-lyxcf is not checked yet.
  > Three hotels not on this ticket also had 401s and no successes from 10-16: Panama City-Tyndall, Spring-The Woodlands and Lincoln North East.
  > This still has no assignee: @rcuadra, can you take it, with Taylor on the HotelKey side?

  ## Agent run 2026-10-30T14:51:14+02:00 (username shape counts and the admin history caveat)

  **Verdict: a Property ID username reliably marks failure, but correcting it is not enough. Overwrite is ruled out from about 10-05 onwards. Before that it is not ruled out, because API writes don't appear in admin history and the September logs are gone. This supersedes the "only two credential edits" and "not supported" wording in the previous run.**

  **Username shape counts (enabled configs, IHG - PRODUCTION 2-WAY, US gateway)**
  - canary-code 255 (197 created before the 10-16 refresh, 58 after), property_id 8, other 1.
  - All 8 property_id hotels are failing with no successes: 7 are on the ticket, with 468 401s and no 200s from 10-16 to 10-30, the latest today at 12:46 UTC. The eighth is Staybridge Suites Miamisburg (not on the ticket), with 13 401s from 10-02 to 10-12, no successes and no pushes since. Its 200s under that name filter belong to a different hotel, Extended Stay Miamisburg.
  - Plainview, now canary-code, had another 401 today at 12:43 UTC.
  - 197 canary-code configs predate the refresh, so being created before it is not a problem in itself. My stale-password reasoning from "Plainview is older than Hollister" is weaker. The fault looks specific to certain sheet rows or accounts, not the whole September load. I did not count successes per shape across the 255.

  **Effect of the admin history caveat (raised by Gareth)**
  API writes through the gateway do not appear in Django admin history.
  - Still holds, from about 10-05: updated_at moves on any save, including API writes. upsert_configuration.diff and PUT /api/accounts/hotelkey cover API credential writes, and show none for these hotels. No config except Plainview and Hollister (admin edits) and Calgary changed after 09-29.
  - Calgary explained: POST /api/accounts/me/hotelkey/validate ran at 10-19 12:02:02 UTC, matching its updated_at, with update_validation.diff. That points to a validation step, not a credential write. The 11:56 PATCH was on the account. The result list was cut off at 25 rows, but the earlier diff query also found no upsert.
  - Withdrawn: "only two credential edits" holds for admin edits only. No admin entries exist for the September updates (Daytona and Denver 09-04, Edmond and Lexington 09-14 14:04, Oklahoma City 09-28, Garner 09-29), so they were probably API writes. Edmond and Lexington updating in the same minute suggests a script. The logs for those windows returned nothing at all, so they cannot show what changed.
  - Also weaker: my claim that the September sheet held Property ID usernames. A later September API write could have set them, and I don't know the username at creation. My batch query also omitted validate and custom batches, so a custom batch running the update plan would not have appeared.
  - Sharon's specific claim still fits poorly: she says migration credentials were added last week, but no failing config has a credential write after 09-29 other than the Plainview edit. An overwrite in September is possible, though.

  **Next check**
  /private/tmp/claude-501/-Users-garethlloyd-projects-canary/f9d58053-af9c-4d9a-922f-9692cdacdc6d/scratchpad/ent8043_all_pms_runs.py (Canary shell, read-only, on the clipboard) lists every PMS-related batch run for these hotels. If validate batches match the September update times, those were not credential writes. If an update plan matches, that supports an overwrite in September.
  The next action is unchanged whichever way that goes: test the Plainview password against the master sheet, then fix username and password together on the 8 property_id hotels if it works, otherwise escalate to HotelKey. Calgary and Dodge City may be a separate case, as they already had canary-code.

  **Updated draft Linear comment on ENT-8043 (replaces earlier drafts; not posted, needs your yes):**
  > Findings from logs and config history. Eight enabled US IHG configs have the Property ID as the username, against 255 using canary-<code>, and all eight are failing with no successes. Seven are on this ticket. The eighth is Staybridge Suites Miamisburg, which should be added.
  > Correcting the username isn't enough on its own: ihg-nycpv has used canary-<code> since 10-28 and got another 401 today. ihg-yycba and ihg-ddcsx also have canary-<code> and got 401s.
  > So please check the ihg-nycpv password against the master sheet next. If it differs, set it and watch the next card push. If it matches, or the 401 continues, this list needs to go to HotelKey to confirm the accounts are active.
  > On overwrites: I found no credential writes by script since about 10-05. September is still open, because several configs have updates from then that aren't in admin history and those logs have expired. ihg-lyxcf is not checked yet.
  > Three more hotels had 401s and no successes from 10-16: Panama City-Tyndall, Spring-The Woodlands and Lincoln North East.
  > This still has no assignee: @rcuadra, can you take it, with Taylor on the HotelKey side?

  ## Agent run 2026-10-30T14:54:17+02:00 (all PMS batch runs, validate plan)

  **Verdict: no overwrite at the 8 US hotels with batch history. Every config update on them matches a batch run, an admin edit or a config that never changed. Dodge City and Chester have no batches and predate the sheet. Sharon's mechanism does exist in code since 10-14, but I found no sign it fired, and her real cases may be other hotels. Separately, onboarding validation cannot catch these bad credentials, which is why this went unnoticed.**

  **September question closed**
  Each unexplained update falls within a minute of a validate run: Denver 13:20:50 and Daytona 13:20:52 on 09-04, Lexington 14:03:59 and Edmond 14:04:00 on 09-14, Oklahoma City 20:34:37 on 09-28, Garner 14:41:21 on 09-29 (by jbalian). Calgary's 10-19 update matches its validate run at 12:02:01. No custom batches or update plans appear. The validate plan had no config-writing path until 52ed7f3e84f (ENT-7814, 10-14), so the September runs could not have written credentials. Later validate runs do not always move updated_at (Daytona on 10-19 did not), which fits a save only when a config changes state; I did not confirm that.
  This restores the earlier reading: the 6 property_id configs created by Configure PMS have kept the username from creation, so the sheet rows of that time probably held Property ID usernames. That is inferred, because I did not see the old sheet values.

  **Sharon's mechanism**
  - Since 10-14, ConfigurePMSIntegrationValidatePlan calls upsert_configuration with the full onboarding config, including username and password, when a gateway config is disabled and its brand or environment differs from expected. An enabled config raises an error instead.
  - Update PMS batches also overwrite. They ran on other hotels in October, for example 97874 (label PTWLP, 10-22), 98489 (GTYOM, 10-26) and 100137 (10-29). I did not check whether these are IHG HotelKey hotels.
  - configure_pms_integration_validate.gateway_configuration_updated returned no rows from 10-14 to 10-30, but I have no positive control for that event, so this is weaker than the upsert_configuration.diff result.
  - So this ticket is probably the wrong example for her report. Ask Sharon for the hotels she means, and check them against those batches.

  **Why validation passes with bad credentials (from code, not yet raised anywhere)**
  - HotelKeyValidationService.authenticate (backend/pms-gateway/vendors/integrations/hotelkey/services/validation.py) tests the JWT client, which does not use the config's username and password.
  - The only check using those credentials is _check_room_status_access, and a 401 there deliberately does not fail validation (ENT-6486, June). It only turns off room refresh.
  - So wrong credentials can show a completed Validate batch, and the first sign is a failed card push. All 8 hotels with batches have completed validate runs.
  - That code's comment says HotelKey grants /data-ingestion access per property. add-source is under the same path. So a third explanation for Plainview, Calgary and Dodge City is that HotelKey has not granted access at those properties, which is not a credential problem. That moves the HotelKey check up in priority for those three.

  **Next steps**
  1. Test the Plainview password against the master sheet, and ask HotelKey about data-ingestion access for Plainview, Calgary and Dodge City at the same time.
  2. Treat the sheet with care: Hollister's config was created on 10-22 and still needed a username correction, so sheet rows may still contain errors. I did not confirm that the wrong value came from the sheet.
  3. Consider a validation check for the add-source credentials, so failures show up at onboarding. Whether a safe test call exists needs checking.
  Not checked: voco Folkestone (EU). Also not visible: shell writes using QuerySet.update(), which skip updated_at.

  **Updated draft Linear comment on ENT-8043 (replaces earlier drafts; not posted, needs your yes):**
  > Findings from logs, batch history and config history. Eight enabled US IHG configs have the Property ID as the username, against 255 using canary-<code>, and all eight are failing with no successes. Seven are on this ticket. The eighth is Staybridge Suites Miamisburg, which should be added.
  > Correcting the username isn't enough on its own: ihg-nycpv has used canary-<code> since 10-28 and got another 401 today. ihg-yycba and ihg-ddcsx also have canary-<code> and got 401s.
  > Two checks next: compare the ihg-nycpv password with the master sheet, and ask HotelKey whether ihg-nycpv, ihg-yycba and ihg-ddcsx have data-ingestion access and active accounts. add-source sits under that path, and our code notes HotelKey grants it per property.
  > On overwrites: I don't see one at these US hotels. All their batch runs are Configure PMS and Validate, and each config update lines up with a validate run or an admin edit. @Sharon, can you share the hotels you had in mind? Update PMS batches and, since 10-14, Validate on a disabled config can both overwrite credentials, so those cases may be elsewhere. ihg-lyxcf is not checked yet.
  > Why this wasn't caught: HotelKey validation treats a 401 on these credentials as non-fatal, so wrong credentials can still pass a Validate batch.
  > Three more hotels had 401s and no successes from 10-16: Panama City-Tyndall, Spring-The Woodlands and Lincoln North East.
  > This still has no assignee: @rcuadra, can you take it, with Taylor on the HotelKey side?

  ## Agent run 2026-10-30T15:39:23+02:00 (where to report)

  **Recommendation: three posts. ENT-8043 for the case, the #ihg thread to answer Sharon, and the #epd-pms-gateway thread for the validation gap. Nothing posted. These drafts replace all earlier drafts.**

  **What changed in the reading**
  - Andrea Bradshaw commented on ENT-8043 today at 12:47 UTC (https://linear.app/canary-technologies/issue/ENT-8043/ihg-hotelkey-card-push-returns-401-not-authorized-at-11-hotels). She already found that the nycpv username change failed, that /v4 calls return 200 while /thirdparty calls fail, and proposed asking HotelKey and holding the other 10. So my "last comment 10-28" is out of date, and she is effectively driving this. I now recommend asking her to take the assignee slot, or name who should. Our post should add to her comment, not repeat it.
  - Her /v4 versus /thirdparty result fits the credential or access explanations. It also adds guest-details to the affected calls.
  - Validation: Connor Swords asked for a HotelKey validate check on 10-01, Yauheni Danchanka said validation already covers /data-ingestion and offered to investigate gaps (https://canarytechnologies.slack.com/archives/C023K54M812/p1790864242396879?thread_ts=1790863563.509959&cid=C023K54M812). That is the right place for the non-fatal 401 finding.
  - voco Folkestone: Taylor says HotelKey is blocking all properties outside the US (https://canarytechnologies.slack.com/archives/C0BLY521L2V/p1793281149346969?thread_ts=1793274401.963629&cid=C0BLY521L2V), so it may be a separate known issue. Taylor describes 403s at a different EU hotel, while voco's logs show 401, so this is not confirmed.

  **Not recommended:** #tmp-hotelkey-performance-degradation (Andrea and Martin's thread there has moved on to monitoring; a link at most), #hotelkey (quiet since 10-05 and mostly Best Western), #eng-alerts-groundcover-enterprise (Andrea already marked that alert as a known issue; its "since 10-26" start date is too late, but correcting it adds nothing).

  **Draft 1: ENT-8043, reply under Andrea's comment**
  > Adding config and batch history to Andrea's finding that only the /thirdparty login fails. US hotels only.
  > - Eight enabled IHG 2-way configs have the Property ID as the username, against 255 with canary-<code>. None of the eight has a successful card push in our logs since at least 10-09. Seven are on this ticket. The eighth is Staybridge Suites Miamisburg, which should be added.
  > - canary-<code> alone isn't enough: ihg-nycpv, ihg-yycba and ihg-ddcsx all have it and got 401s.
  > - Panama City-Tyndall, Spring-The Woodlands and Lincoln North East also had 401s and no successes from 10-16.
  > - I don't see a script overwrite at these hotels. They only had Configure PMS and Validate batches or none, Configure PMS skips existing configs, and each config update lines up with a validate run or an admin edit.
  > - Validate can't catch this: a 401 on these credentials is non-fatal in HotelKey validation. Raising that with PMS Engineering separately.
  > Next: compare the ihg-nycpv password with the master sheet, and @Taylor, can you ask HotelKey whether these third-party accounts are active and have data-ingestion access? @Andrea, this still has no assignee. Are you the right owner, or who should be?

  **Draft 2: #ihg, reply in Sharon's thread** (https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793285908878999?thread_ts=1793285908.878999&cid=C03V5P4B48P)
  > @Sharon we looked at ENT-8043 for this. At the US hotels on that ticket I don't see credentials being overwritten: they only had Configure PMS and Validate batches or none, and Configure PMS skips configs that already exist. The wrong usernames look like they've been there since each config was created. It's still possible elsewhere, because Update PMS batches can replace credentials, and so can Validate on a disabled config since 10-14. Can you share the hotels where you saw it happen? We can check those directly. Details are on ENT-8043.

  **Draft 3: #epd-pms-gateway, reply in Connor's 10-01 validation thread**
  > @Yauheni following up on the gap you offered to look at, with a real example. HotelKeyValidationService.authenticate proves the v4 JWT login. The only check using the config's username and password is _check_room_status_access, and that treats a 401 as missing access and just turns off room refresh (ENT-6486). So wrong third-party credentials can pass Validate. On ENT-8043, every hotel with batch history completed Validate, but card pushes all return 401.
  > A plain fix isn't obvious, because the code says most properties don't have room-status access, so that 401 can't simply become fatal. Do we have a safe way to tell bad credentials from missing access, or is this one for HotelKey? Could PMS Engineering pick this up? cc @Connor @Andrea

  ## Agent run 2026-10-30T15:52:24+02:00 (is it new? drafts revised)
  Checked each draft claim against ENT-8043, ENT-7708, ENT-7923, ENT-7812 (keyword scan, first page), ENT-8050, ENT-8056, INT-11128, INCIHG-4, PMS-11489, ENT-6486 and Slack. These drafts replace Drafts 1-3 above. Nothing posted.

  Already known, removed: only /thirdparty fails (Andrea 10-30, Ryan 10-09 on ENT-7708 https://linear.app/canary-technologies/issue/ENT-7708, SRE Agent 10-07 https://canarytechnologies.slack.com/archives/C0AQG7N3RPE/p1791368062336249); ask HotelKey (Andrea, Taylor); Property ID usernames (rcuadra); reads-only validation concern (Andrea 10-17 on ENT-7708).

  New: card push uses username/password, guest-details uses the v4 JWT (clients/thirdparty/client.py:38, clients/pms_core/client.py:86 and :386); yycba and ddcsx contradict rcuadra; 8 vs 255 counts; Miamisburg and 3 extra hotels; no credential overwrite at these hotels.

  Changed by this search: Sharon is right that scripts overwrite live settings: ENT-8050, 53 live hotels on 10-28. The non-fatal 401 came from Gareth's own June suggestion on ENT-6486, whose claim that the same username/password works for PMS core is wrong. Sharon already gave ENT-8043 as her example. Room status gave 401 at 111 accounts and 403 at 48 from 10-10 to 10-30, so it is not a credential test.

  Not checked: whether the 10-28 cohort included ENT-8043 hotels or a Configure PMS step. The 401s predate it. Whether the 74 guest-details hotels push cards fine: guest-details calls did not appear under the log event I queried.

  Draft 1, ENT-8043:
  > Adding what isn't in this thread yet. US hotels only.
  > - Card push and guest-details use different logins. add-source sends the config's username and password. guest-details sends the v4 JWT, even though its path is under /thirdparty. So nycpv's guest-details 401 says nothing about these credentials. It looks like the separate issue on INC7665889. These should be two separate asks to HotelKey.
  > - ihg-yycba and ihg-ddcsx already had canary-<code> and still get 401s, so not every hotel here has the Property ID username.
  > - Across enabled IHG 2-way configs, 8 have the Property ID as the username and 255 have canary-<code>. None of the 8 has a successful card push in our logs since at least 10-09. Seven are on this ticket. The eighth is Staybridge Suites Miamisburg, with 13 401s from 10-02 to 10-12.
  > - Also 401s and no successes from 10-16: Panama City-Tyndall, Spring-The Woodlands and Lincoln North East.
  > - I don't see a script overwriting credentials at these hotels. They only had Configure PMS and Validate batches or none, and each config update lines up with a validate run or an admin edit. The sheet values for hotels with batch history are canary-<code>, so most of these configs never took the sheet's username.
  > The ihg-nycpv password still hasn't been compared with the master sheet, as far as I can see. @Andrea, this has no assignee. Are you the right owner, or who should be?

  Draft 2, #ihg, Sharon's thread:
  > @Sharon two answers, because I think two things are mixed together. Scripts do overwrite settings on live hotels: the 10-28 "HK Onboarding Values" run reset checkout and add-on times at 53 live hotels (ENT-8050, with the decision on ENT-8056). For credentials on ENT-8043, I see the reverse of what you asked. These hotels weren't given new credentials from the sheet: most still have the older Property ID username, because Configure PMS skips configs that already exist, and their 401s started before that run. Credentials can still be replaced elsewhere, by Update PMS batches or by Validate on a disabled config since 10-14. If you have a ticket other than ENT-8043 where the credentials changed, send it over and we'll check it.

  Draft 3, #epd-pms-gateway, Connor's 10-01 thread:
  > @Yauheni following up on the gap you offered to look at, with a real example. The /data-ingestion check you mentioned doesn't stop onboarding: a 401 or 403 there only turns off room refresh. That came from my suggestion on ENT-6486 in June, and I got one thing wrong there: I said the same username and password work for the PMS-core login, but v4 uses the JWT. So nothing in Validate tests the username and password that card pushes use. On ENT-8043, every hotel with batch history passed Validate, and card pushes return 401.
  >
  > Room status can't be the test, because it returned 401 at 111 accounts and 403 at 48 from 10-10 to 10-30. Validate could compare the config username with the onboarding value, since it only compares brand and environment today. That would flag most of these hotels but not Plainview, whose username now has the sheet's format and still fails. Is there a harmless call that tests this login, or should we ask HotelKey for one? Could PMS Engineering pick this up? cc @Connor @Andrea

  ## Agent run 2026-10-30T16:30:00+02:00 (where to post)
  Re-read ENT-8043, Sharon's thread and Connor's thread; nothing new since the drafts. Nothing posted.
  Recommendation: post to ENT-8043 now, because Andrea's 10-30 comment cites guest-details as evidence about the card push login and suggests asking HotelKey. Correction: no evidence that anything has gone to HotelKey or that Andrea did anything wrong; the suggested ask is still sound for card push. Reply to Sharon's unanswered credentials question in #ihg, credentials part only. Hold the #epd-pms-gateway draft until HotelKey answers, then raise it as a ticket or in that thread.
  ENT-8043: https://linear.app/canary-technologies/issue/ENT-8043/ihg-hotelkey-card-push-returns-401-not-authorized-at-11-hotels
  Sharon's thread: https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1793285908878999?thread_ts=1793285908.878999&cid=C03V5P4B48P
  Connor's thread: https://canarytechnologies.slack.com/archives/C023K54M812/p1790864242396879?thread_ts=1790863563.509959&cid=C023K54M812

  ## Agent run 2026-10-30T16:37:12+02:00 (correction: sheet timing)
  Correction to the Sharon draft and earlier conclusions: "most never took the sheet's username" is unsupported. It compared configs with today's sheet values, last updated 10-16 15:05, so the sheet's earlier contents are unknown. The Property ID config created dates (09-04 x2, 09-09 x3, 09-28) match the Configure PMS run dates at the six ticket hotels with batch history, matched by date only, not config ID. Those configs may have taken the Property ID username from the sheet as it was then, with Create plan re-runs skipping them after the refresh. That would be stale values from a script, not an overwrite. Same could apply to passwords, which could explain ihg-nycpv still failing after a username-only edit; unverified. To settle: ask Taylor what the sheet held before 10-16 and whether passwords changed. Do not send the earlier Sharon draft.
project: null
source_id: https://linear.app/canary-technologies/issue/ENT-8043/ihg-hotelkey-card-push-returns-401-not-authorized-at-11-hotels
tags:
- morning-gtd
- linear
time_minutes: 15
title: 'Check who owns ENT-8043: IHG HotelKey card pushes failing with 401 at 11 hotels'
updated: 2026-10-30 16:37:12.000000
waiting_on: null
waiting_since: null
working_on: false
---

Every card push fails at these 11 IHG hotels, so cards never reach HotelKey. Ticket is In Progress with no assignee and no priority. Possibly related to Sharon Hales' report that completed HotelKey migrations are being overwritten with different credentials (unverified); I did not read the ticket's comments.
https://linear.app/canary-technologies/issue/ENT-8043/ihg-hotelkey-card-push-returns-401-not-authorized-at-11-hotels