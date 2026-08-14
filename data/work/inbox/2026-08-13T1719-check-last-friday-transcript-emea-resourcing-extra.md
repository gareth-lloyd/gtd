---
area: null
completed_at: null
contexts: []
created: 2026-08-13 17:19:10.031817
defer_until: null
due: null
energy: low
id: 2026-08-13T1719-check-last-friday-transcript-emea-resourcing-extra
order: null
output: |
  ## Agent run 2026-08-13T17:25

  **Source:** Granola — "EMEA resourcing and prioritization with Blake", Fri 7 Aug 2026,
  16:02 GMT+3 (meeting id `08bf977e-fb06-48b5-98fd-704d7a9e2999`).
  Participants in the room (from transcript context): Blake (exec, joined from the car),
  Martin (EMEA lead), James (EMEA eng doing the coordination), you.
  Caveat: the Granola transcript is **truncated mid-sentence** right at the wrap-up
  ("Cool, concrete actions because I have to run too. I'm going to start conversations
  right away about where ticketing goes. That doesn't mean that…"). The explicit
  action list Blake was about to read out is NOT in the recording — worth checking
  with Blake or James if you want the authoritative version.

  ### Action points — yours

  1. **Monday conversation with Blake on ticketing ownership.** Blake, in-meeting:
     "that's now an active work stream move in my mind… Gareth, we should talk about
     this on Monday too." You said yes.
     STATUS: I checked Granola for Mon 10 Aug — the only captured meeting was the
     "EMEA directors call" (`bbefd219-0ed7-43f6-b51d-d5a98c4b337e`), whose notes cover
     Tommy, physical access, Ash's PMS capabilities work and internal tools. **No
     ticketing/Ian item in it.** So this looks unclosed, ~4 days late. Highest-priority
     follow-up out of this transcript.
  2. **Coordinate with Ian on where the hand-off line sits.** Blake asked you directly:
     "a lot of this seems like more coordination with Ian is necessary on some of the
     ownership of getting these things across the finish line. I don't like the sound
     of where PMS gateway is handing off responsibility… it seems like PMS gateway is
     ending done too early" (certification complete ≠ integration live in a hotel).
     Concrete framing Blake offered: PMS Gateway should be "pulled deeper, almost
     donated into EMEA for the completion of some of this work stream", rather than
     EMEA being tasked with finishing the flow-through.
  3. **Get product/market metrics behind the ticketing question before the org move.**
     Raised in-meeting as the missing input: addressable market for ticketing, size of
     the triage queue for these integrations, and whether HotelKit is a one-off or the
     start of a series. Without it the "move ticketing to Ian" decision is being made
     on pattern-smell alone.

  ### Action points — Blake

  4. **Start conversations on moving ticketing integrations to Ian's connectivity
     team.** Committed to explicitly, and to taking notes to make sure it progresses.
     This is the one hard decision that came out of the meeting.

  ### Open items / decisions NOT made

  5. **HotelKit ownership — still undecided.** James' case: ~4,000 units, one German
     customer about to be contractually committed; scaffolding similar to the work
     already done for BPMaestro; EMEA has the time-zone overlap for HotelKit's own
     certification process, the language coverage, and the scar tissue from making
     guest-request-item mapping work on prior ticketing integrations; Messaging and
     Service/Concierge roadmaps are full. Blake did NOT say no to EMEA taking this
     specific one — but framed ticketing as a category that is "graduating" and should
     migrate. Also flagged by Martin: even if headcount were approved now, hiring +
     onboarding + notice periods means nobody lands before well into next year, so
     HotelKit can't be staffed by new hires anyway.
  6. **Martin's Q4 headcount increase ask — unresolved.** Current EMEA R&D is
     2 automation + 3 engineers (incl. James). Blake's test for approving it: the
     headcount must map to a durable *ownership surface area*, not to activation
     throughput. Explicitly blessed as EMEA-owned and scale-worthy: GDPR, local
     government/regulatory connectivity, STB police reporting (Italy, Spain), and the
     equivalent bespoke regional work for APAC staying with the APAC pod. Explicitly
     NOT accepted as a scaling justification: activation volume growing linearly with
     the customer base — Blake: "if we need to linearly scale EMEA R&D staffing, we're
     not getting scale in general", and band-aiding product quality with a horizontal
     team is "the worst long-term outcome". Supporting pillar you can use: Harman has
     said EMEA activation is a top company priority.
  7. **Senior implementation manager role — supported in principle, not scoped.**
     Origin: James is effectively doing TPM + implementation-lead work and it's
     unsustainable ("I don't think James can keep handling it the way he has for the
     last two months"). James' own product-side conclusion: not a CNPM — the skill set
     needed is a senior CS/implementation lead ("imagine Albert going in and setting
     everything up") who owns config, PMS integration tracking and POC coordination
     end to end. Would sit under Nathan but below Nathan's level. Blake supportive;
     open question is whether it needs a paired TPM on the R&D side, and whether it's
     an R&D or CS role (Blake's default: push activation-coordination burden to CS
     over time).
  8. **Sharon's team enablement — recurring failure mode, no owner assigned.** Blake:
     we repeatedly fail to educate the Integrations team to take on new integrations
     (happened with PMS gateway, and consistently with mobile keys). The work that
     scales linearly with customer count belongs there, not in engineering. Centralised
     connectivity ownership makes that muscle repeatable.

  ### Framing worth reusing

  - Blake's architecture position: EMEA should only ever absorb an integration as
    *total overflow*, and that overflow should come from the integrations/connectivity
    team — never from a product pod.
  - Connectivity today = Payments + PMS Gateway under Ian; Blake thinks that layer
    should absorb more categories (ticketing, membership gateways).
  - Your R vs CAR point landed: EMEA is measured R-primary/CAR-secondary, vertical pods
    are CAR-only, which is why the vertical pods exit before the customer is actually
    live. Blake agreed ("100% true") and tied it to Canary's DNA — whoever is closest
    to the customer does the work all the way through.
  - Blake's own summary of where to be most critical: "the integration landscape is the
    place we should be most critical coming out of this conversation."

  ### Suggested next actions to capture separately

  - Chase the Blake ticketing/Ian conversation that was due Mon 10 Aug.
  - Ask Blake or James for the concrete action list the recording cut off.
  - Pull the ticketing addressable-market + triage-queue numbers before block planning.

  ## Agent run 2026-08-13T17:34 — full meeting summary (reordered, not interpreted)

  Same source meeting. Grouped by topic for clarity; content is what was said, not a
  reading of it. Granola merges all non-Gareth speakers into "Them", so speaker
  attribution below is from context. Recording cuts off mid-sentence during Blake's
  closing action list.

  ### Stated purpose of the 30 minutes
  - Decide whether EMEA picks up HotelKit — James wanted it settled before block
    planning so it wouldn't consume that session
  - Martin's standing ask: increase EMEA headcount in Q4
  - Mid-meeting Gareth reset the group back to the resourcing question, which had
    morphed into a prioritization question the previous time they spoke

  ### HotelKit — the case for EMEA (James)
  - HotelKit is a service ticketing solution, comparable to HubOS and BPMaestro
  - ~4,000 units in scope; a German-based customer about to be contractually
    committed accounts for a portion
  - BPMaestro already done; the scaffolding looks similar
  - Conversations with SJ, Kevin and Jake pointed to EMEA as best placed to talk to
    both the customer and the HotelKit point of contact
  - Service/Concierge and Messaging product owners report full roadmaps
  - Unlocks CAR for the region
  - Gareth added: HotelKit runs its own certification/approval process, so time-zone
    overlap matters; and the team already has hard-won experience mapping the
    specific guest-requested item through ticketing systems
  - James added: language coverage matters too, and EMEA is already handling the
    end-to-end vertical slice (voice and web chat)

  ### Blake's response on ownership
  - Agreed Messaging should not take it: "I think that that's wrong"
  - Has been talking to Ian; believes integrations that aren't PMS or payments are
    underserved on ownership
  - PMS and payments have natural homes; CRS sits close enough to PMS that PMS
    Gateway took it; ticketing is now the largest of the remainder, and membership
    gateways are in the same category
  - Those have been owned by product teams because product teams are the primary
    user — described as a disservice, because ownership isn't consistent
  - "A bad outcome is EMEA pod owns this ticketing gateway. Nobody wants that long
    term."
  - On overflow: EMEA picking up an integration should only ever be total overflow,
    and that overflow should come from an integrations team, not a product pod
  - Connectivity today = payments + PMS Gateway under Ian; that layer should absorb
    more, with more shared commonality — e.g. Julius thinking about scale across all
    integrations
  - Sharon's team (Integrations) is a repeated failure: they don't get educated to
    take on new work — happened with PMS Gateway and consistently with mobile keys.
    Work that scales linearly with customer base belongs there; engineering work
    should not scale with customer base. Centralised connectivity makes that
    hand-off a repeatable muscle
  - Decision stated in-meeting: "we need integrations to start thinking about this
    work needs to start moving, like now, over to Ian's world… that's now an active
    work stream move in my mind. And I'm going to take notes to make sure that that
    progresses. Gareth, we should talk about this on Monday too."
  - Caveat Blake gave: not saying HotelKit specifically is the one to say no to and
    move — but ticketing as a category "feels like it's graduating"

  ### Pushback raised on that
  - More product metrics needed first: addressable market, what the roadmap looks
    like, size of the triage queue for these integrations — it may be that after
    HotelKit there aren't many more ticketing integrations
  - Hiring timing: with Q4 approaching, hiring + onboarding + notice periods means a
    new person lands well into next year, so "I don't think we should be talking
    about HotelKit at all at this stage"
  - Martin noted he isn't arguing EMEA should own everything — he'd already agreed
    with Mati that VPN ownership moves now the client is onboarded

  ### Blake on what EMEA should be discerning about
  - The pod has to be very discerning about what it takes on; this will be a
    repeated conversation
  - Ticketing integrations: two seen so far, more expected — that category is
    "becoming a smell to me versus repeated work that we should take on"
  - EMEA's speciality is getting customers activated, which ties the work closer to
    EMEA than to a product pod, but connectivity is not EMEA's speciality either

  ### Ownership that stays with EMEA (agreed)
  - GDPR work — ownership stays with EMEA
  - Connectivity with local governments stays with EMEA; same principle applies to
    APAC for bespoke STB work
  - Local regulation integrations, STB / police reporting for Italy and Spain
  - Blake: you own the outcome, which means talking to a lot of people and enforcing
    things across upstream and downstream teams
  - Compliance integrations named as a continuing chunk, including Dubai and the
    GDPR work — not expected to be one-offs

  ### Activation and the scaling argument
  - Blake's framing: Harman is very clear that EMEA activation is a top company
    priority, and Blake is happy to stand on that as the pillar for staffing the
    team up — if the blocker is R&D resource in the EMEA pod, that's a good staffing
    argument
  - Question put to the room: does activation work scale linearly with customer
    base? Answer given: yes, currently the ask to activate fast requires it
  - Open question raised back: what is the expectation — is EMEA a forward-deployed
    engineering team owning engagements end to end, on top of every ticket any other
    team is working? That drives faster activation but takes time away from other
    engineering work. Noted as coming up from multiple sources and also raised by
    Gareth in the document
  - Pipeline growth means continued heavy activation support; the question posed was
    whether that's doable with the current two automation engineers plus James plus
    one more — three engineers
  - Blake's counter-framing: scaling EMEA R&D for activation alone should be
    questioned hard, because leverage should be coming from the vertical pods; "if
    we need to linearly scale the EMEA R&D staffing, we're not getting scale in
    general"
  - Blake: an EMEA team existing and being large would be a smell — it would mean
    Canary can't prioritise well enough for teams to own what they need to own
  - Blake: EMEA reacting to information in the morning and fixing by evening is a
    factor to keep, so some scaling to customer base is expected, but it should
    scale slowly
  - Long-term push stated: activation coordination burden goes to CS as much as
    possible
  - Blake on band-aiding: "I hate the idea that we have a shitty product and the
    only way we can fix it is by band-aiding over with a team that's horizontal…
    it's a good temporary outcome, but long term it's the worst outcome"
  - Martin's counter: right now EMEA customers are very critical of product quality
    — HSC Berlin given as the prime example — so you can't go without an EMEA pod
    today. Blake clarified he isn't arguing against having the pod, but against its
    scale and what it scales against; an acceptable answer could be to add someone
    and later have that person roll off. Martin's stated near-term focus: getting
    IC Berlin activated. Blake: "and you should be obsessed by that" — none of this
    is feedback on current delivery

  ### James's role and the role gap
  - James is currently doing coordination and fixing: everything Ulysses-side fixed
    for Lunar, plus pushing Sharon's team or sales for access, contacts and content
  - Named pattern: for new PMSes (host, clock, and others) coordination and
    throughput are what's lacking; EMEA steps in when a hotel needs to go live or is
    piloting — cited: Greg Hotel (Protel), Lunar — solving high-priority bugs to get
    them live
  - Stated as unsustainable: "I don't think James can [keep going] the way he's been
    handling it for the last two months. That's more like a project management
    role." If EMEA is responsible for knowing the status of every issue across every
    team and pushing them, that's a TPM role
  - James's separate product-side discussion: the plan had been to hire a CNPM to
    take load off, but that isn't the skill set needed. His suggestion: a senior
    implementation / CS lead — "imagine Albert just going in and setting up
    everything" — someone product-ops or TPM-shaped who can keep a host PMS
    integration on track with the POCs lined up
  - Blake: supportive of a senior implementation manager looking across; asked
    whether that differs from Nathan's role. Answer: Nathan would still manage that
    implementation manager — an equivalent level, non-kiosk. Blake's open question:
    whether that person needs pairing with a TPM on the R&D side; if it sits on the
    R&D side, it's a TPM

  ### Exchange on PMS Gateway hand-off
  - Blake to Gareth: "a lot of this seems like more coordination with Ian is
    necessary on some of the ownership of getting these things across the finish
    line. I don't like the sound of where PMS Gateway is handing off responsibility"
  - Gareth: "certification, and then done" / "without actually pushing through an
    integration with the hotel"
  - Blake: "it seems like PMS Gateway is ending done too early"
  - Established on host: EMEA hasn't done hands-on-keyboard work on it yet; James is
    working with Mal directly to push the integration and get the keys
  - James's framing of the EMEA remit: the task given is that host unlocks X amount
    of deals, so it's important for EMEA to own — and when host comes online the
    EMEA pod also carries that remit; e.g. on Greg Hotel/Protel, EMEA has been
    involved in the issues raised because of the sheer number for a new integration

  ### Gareth's R vs CAR point
  - Put as speculative: EMEA, because of how it's structured, set up and
    incentivised, thinks more sharply about financials than other pods and
    prioritises on R and CAR in a way that isn't driving decisions on other pods
  - Blake: that's natural — vertical pods think CAR much more than R; EMEA is
    R-primary, CAR-secondary, inverting the relationship
  - Gareth: so vertical pods aren't held to account for R in the same way, and might
    end their involvement earlier
  - Blake: "100% true." EMEA ends up closest to the customer, and Canary's DNA is
    that the people close to the customer do the work all the way through — there's
    no expectation of hand-off. Blake's conclusion: "it feels like the PMS Gateway
    team needs to be pulled deeper, almost donated into EMEA for the completion of
    some of this work stream, rather than the EMEA team being tasked with finishing
    the flow-through"

  ### Blake's closing summary before the cut-off
  - "The integration landscape is the place that we should be most critical coming
    out of this conversation"
  - If things look like routine-style integrations, the same pattern applies as
    never taking on a full end-to-end payment gateway or a PMS gateway — identify
    them and move them into Ian's world for better scale, ownership and
    observability
  - Stated danger: EMEA getting bogged down with these integrations breaking, which
    follows as long as EMEA built them and took them live
  - Activation side: keep the fast-reaction factor, keep the EMEA-owned ingredients
    (GDPR, local regulation integrations, STB/police reports for Italy and Spain),
    and default to CS taking the activations coordination burden
  - Headcount follows from that rigour; if headcount is added for a period, either
    the ownership surface has genuinely grown or it's a band-aid for something in
    the business that should be fixed instead
  - Recording ends here: "Cool, concrete actions, because I have to run too. I'm
    going to start conversations right away about where ticketing goes. That doesn't
    mean that—"

  ### Not resolved in the meeting
  - HotelKit ownership
  - Martin's Q4 headcount increase
project: null
source_id: null
tags: []
time_minutes: 5
title: check last friday transcript (emea resourcing ) extract action points
updated: 2026-08-13 17:34:10.000000
waiting_on: null
waiting_since: null
working_on: true
---