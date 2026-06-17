---
area: engineering
contexts:
- craft
created: 2026-06-16 16:40:46.803505
defer_until: null
due: 2026-06-17
energy: low
id: 2026-06-16T1640-add-context-from-andrea-sync-to-ent-6145
order: 5
output: ''
project: 2026-04-16T1210-unblock-team
source_id: null
tags: []
time_minutes: 5
title: Add context from andrea sync to ENT-6145
updated: 2026-06-17 13:51:53.485091
waiting_on: null
waiting_since: null
working_on: true
---

https://linear.app/canary-technologies/issue/ENT-6145/onboarding-scripts-conditional-add-to-child

call transcript. 

Meeting Title: Andrea Bradshaw
Date: Jun 16
Meeting participants: Gareth Lloyd

Transcript:
 
Them: Hey, good afternoon. How's it going?  
Me: Pretty good. Kind of busy on some of the stuff but yeah generally good how about yourself?  
Them: Good. How was your weekend?  
Me: I was actually in the UK for a wedding. So.  
Them: Oh, fun.  
Me: Back Sunday night. Yeah it was really nice just a lot of work. With the kids but worth it.  
Them: Is the travel easier now from Athens?  
Me: Easier yes. Not easy but easier.  
Them: Yeah. That's awesome.  
Me: Cool. How was your weekend?  
Them: It was good. We had, I'm sure you're aware the next one on Saturday night. So that was just perfect night out in the city. Lots of happy people and things like that. So that was good. And then I went fishing on Sunday, which was kind of random. Oh, and I went to the sewing fishing from sheepshead bay.  
Me: Whereabouts?  
Them: And I expected it the boat to kind of go out near the rockaways, but we ended up fishing under one of the uprights for the verizono bridge. There were a lot of boats, but apparently that's where like the fluke hang out.  
Me: Oh wow.  
Them: So that was interesting.  
Me: Did you catch anything?  
Them: I caught four, but none of them were big enough to keep. Which I will admit I was a little relieved about actually.  
Me: It's all about the sport.  
Them: Yeah. Then, yeah, the other thing is I went to the Hansen like puppet shop, like the sesame street.  
Me: Oh Jim Henson right cool cool that's that's fun.  
Them: And. Yeah. Yeah, it was really interesting. There's no muppets there anymore because they sold them muppets to Disney. But there's fraggle rock and then sesame street and they do the polar bears for Coca-Cola too, which I didn't realize.  
Me: That's pretty cool.  
Them: So yeah, a ran weekend. Yeah.  
Me: Awesome. I know you put a lot of things in the dark and I've added a couple more so why don't you start off.  
Them: The first one, it's probably a lower priority, but this is kind of circling back to the PR that you reviewed last week and then came up again early this week. Just some of the comments you made. I'm not sure there are things I would have picked up on. So I was just wondering if we have time, if you could walk me through kind of like what you noticed, what patterns you're always looking for, especially in like these onboarding type PRS.  
Me: Yeah. So let me refresh my memory first I love.  
Them: Yeah, I think specifically here you're kind of calling out how it's not necessarily item potent and like maybe something tipping right into also like there was too much logic originally within onboarding. So you asked him to refactor it out. To move a lot of things to like services on the voice side.  
Me: Like. Yeah so. The onboarding app shouldn't be the place where teams write their own validation I think that should be. Fairly straightforward to enforce. And I think. What we're coming up against here is like a bit of. Maybe path dependence like we've done onboarding with onboarding scripts it's still used very actively for wind and plus so we need to sort of defend the existing behavior of wind and connect plus but the voice team have got some other requirements. And they. Re still using the onboarding scripts. In fact one of the earlier versions of this was actually there was an admin interface that was creating an onboarding script badge and like running that which was like. You might you're probably familiar with that but it's really not the right way to think about it like if you've got an admin API it should just be calling a voice service. So I think. Gaston who's implementing these. Like maybe was a bit confused just about general onboarding concepts so I. Pushed on that but then I'm opening the audio referencing just to remind myself of my comments. Now. So one of them is just a general call out about enforcing both on the client and the server. And the UI. Yeah the other thing. That's really important to remember with onboarding scripts is that. Everything happens in a database transaction and our rollback method is just to. Unwind the transaction. So anything. That makes a change on an external service. We might lose our record of that change. If we unwind the transaction and like we're not even. The only record we would have would be the results of the failure on the onboarding script run. Yeah that's something that just we have to be really aware of. I don't know if there's a way to maybe. Rise that above the level of documentation and into like a. Something that's actually enforced like we could mark plans according to whether they do change things in third party services. But yeah. Just generally keep in mind that everything's in a transaction that can be unwound.  
Them: I think I'm also struggling a little bit with. This PR feels very large and I feel like.  
Me: Yeah.  
Them: Like I, especially being like newer to the details of the domain prefer smaller. And I'm not sure how much to push and ask for small pr is, which we're also like leaning into AI and one shotting everything.  
Me: I mean. I don't have full context for what's going on here. Like gaston has been working on this for feels like over a month at this point. And it's come through like three different versions. The first couple were. Like. Just had to really push back because. They weren't using any of the onboarding and concepts in the way that we want to enforce. Let me just overview what this one's doing. So we've got. A few onboarding changes. Moving some stuff out to a service. Yeah this is I think this has changed quite significantly since I last looked at it. I might need to do another review.  
Them: Yeah, if you don't mind that big, I reviewed and I. Worked with Claude to review also a little bit. So I did approve, but yeah, I think you don't mind doing another pass and be good. Also.  
Me: I'm just saying he so I reviewed. And then he's got three more commits since then. So I don't even recognize these changes. All right I'll make a name. Both side.  
Them: I just want, yeah, I just wanted to make you aware of kind of like project staffing changes so you know who's working on what.  
Me: S.  
Them: Things are shifting a bit because I didn't have full, a full picture until after we talked last week on Andres's holidays. So he's only in this week and two days next week. So instead we're having team show pick up the work on the drift detection. And then using that to roll into the Wyndham segmentation as well. With labta.  
Me: So just on that point. Do you think the drift detection will be directly useful for the segmentation? I think. We've scoped the drift detection. What I propose to scope which was just surface in Django admin. But that leaves open. Anything around using it for onboarding scripts. Which. Would be a separate. Piece.  
Them: Il. Yeah, that's something I saw in the edge design. So I think we'll want to talk through because I think this would be great if we could use.  
Me: Okay is. That.  
Them: For this configuration run the like locked or free. Values. When we run configuration. So I'm going to talk through that with team show this afternoon.  
Me: Cool. Let me just be very specific on that.  
Them: And if the context is helpful. Like we keep your, I'm sure you're aware, you keep running into this when we run a configuration script on a second or third time. Not knowing if we should totally rewrite everything back to factory settings or not.  
Me: So. This was my notion proposal for one one approach to that. Does tincho have any documentation for what he wants to do on the segmentation or is there any documentation on that?  
Them: The segmentation work? Not yet.  
Me: Yeah.  
Them: No no we are kind of having them look at this first and spend maybe like a week on this. To then try to have that base set up so that we can start the segmentation. Work.  
Me: Awesome. Slack plus the one. Sent last Thursday which I marked as for Andres but it'll be good introduction those are those two are the relevant ones.  
Them: I'll make sure to add this. And share this with teacher then. Just thought as we're talking I'm wondering if we should rebrand from onboarding to just configuration scripts.  
Me: I think that's a fabulous idea and I think it would resolve a lot of confusion amongst other teams across the company. Can you talk to Stephanie about that? Because. She's also dealing with the non enterprise side of this. So I'm trying to figure out how, you know, adding a product to an existing hotel should really work. And I think. Encouraging. Onboarding scripts but maybe courting them something else to make that clear would be pretty good.  
Them: Well you can just call it initial configuration.  
Me: Yeah. Maybe. Go through a naming process with the team get everyone on board. There must be a good name out. Then.  
Them: We've got Ryan finishing pre-production hotels and then doing the Adobe integration for Windham compendium. LAUTA is finishing like a spike into the explo omni. But then we're also having him do an edge design for the SCIM protocol, which is the. Deleting users. So I think we'll probably move on the execution of that one. But Connor wanted to know how much work. Are there any things we need to worry about for the migration?  
Me: Blake briefly floated in Angela the other day. Was using work OS to do our SSO integration. I think the idea there would be we integrate with one thing and then it can talk to all the other protocols. I don't know if it's. A slam dunk obvious thing to do but maybe keep it at the back of your mind in case. It does sound good. Like wasn't proposing it he just asked me like did you ever think about this?  
Them: Yeah.  
Me: Cool is Ryan doing all right on pre-prod?  
Them: He's doing okay. There's a bit of confusion. I think maybe we mentioned it last week or the week before because he had told me he would be done in a few days and then in the like support meeting he said a few weeks. Which I was yeah surprised about. And so I think.  
Me: Uct.  
Them: We've leveled out that when he tells me it's a few days even if it's a few days of edge work. Like we're trying to set expectations externally. Yeah, but he's doing well and jumping on things. Um I'm sure as you know everyone gets kind of feels a little bogged down when they're on the triage rotation.  
Me: Ion. Are you concerned about that?  
Them: Yes I am. I think right now we're kind of. One planning around it. I'm just like noting when folks are on triage rotation and then to like. Trying to find the patterns on things. I think it kind of lausa keeps pushing on like if SSO is self serve that will fix a bunch of these things. But there's a lot of other like permissions create above property and create loyalty. So like it doesn't feel like a fire but it does feel like something we need to keep like prioritizing chipping away. At.  
Me: Agreed? Cool. What's next? Has the above property call list going I haven't really checked it in on that.  
Them: I think Andres was kind of just waiting for one or two final PR reviews. And he had talked with Lorena. So I think originally he wanted the team to test stuff while he was out, but I don't think the pr got merged. So I'm hoping we'll have a bug bash on Wednesday or Thursday when he's back.  
Me: Cool sounds good. You generally happy with the way the team's working?  
Them: Yeah, I think one thing I added at the bottom want to talk about is like we've had teen shadow two inch designs recently and they're pretty rough. I'm trying to figure out how to coach that. So that in a little. I think. I think teacher needs help on that side of things. I think Ryan, it feels like needs. Slightly needs to keep getting pushed or keep getting given deadlines to kind of stay focused. Andres I don't have a lot of visibility because voice is doing all of the PR reviews but it seems good in the couple I've checked in on seeing. Okay. And I think Lola is good and just needs to work on being more communicative. Proactively.  
Me: Yeah. I think these are all. Very valid pieces of feedback and stuff that they would have heard in some form but yeah I think. Using your. You know the transition to really reinforce those is a good idea.  
Them: Yeah we started. Like we had an eng only meeting yesterday. I don't know if you remember from a couple years ago that like. When we were supposed to look at our dashboards and our like API endpoint. Kind of continue those just as like monthly end meetings. So yesterday we went through. Our dashboards and we went through like the engineering backlog tickets that we have and kind of groomed things. And it's so.  
Me: That's awesome. That's the kind of thing that. I would always find really hard to fit in when everyone could be there so I'm really glad that's happening.  
Them: Yeah I think it'll be good and then yeah just the other thing I'm pushing is. Pushing everyone to read everyone's edge designs. I'm going to try to have folks do kind of like post project brown bags for the ones that we haven't read. So like Brian's project and Andres's project. I'd like them to like. Walk through the edge design and walk through the code changes with everyone just to do that knowledge share. Post project.  
Me: Cool listen. All right. Those all sound. Reasonable feels like you're on top of the team dynamics so I'm glad to hear that. That kind of leads into the the product team stuff what have you heard and because I don't I don't think I've heard like. A formal announcement in any form has kind of maybe talked through stuff with you?  
Them: Yeah Connor just has I talked to him last Wednesday in the office right before product was having their meeting and he sort of showed me the like proposed organization of product teams. It sounded like the product meeting wasn't actually that great because SJ showed up very late and wasn't very like on task. But I'm just curious since. It looks like that's not going to mirror engineering exactly if you know if there's going to be any shuffling on our side.  
Me: I don't think so like I said I haven't seen anything final but. If if what kind of has sort of. Well he's heard and communicated that goes through then I don't find any of it very concerning directly. I think. My understanding is the main point is just for SJ to have a more sustainable. Management structure and also for it does come from actual like frustration on the product team where reporting through SJ was quite frustrating for a lot of people trying to do that. Because you know he just had an unfeasible portfolio. So from that point of view I only see positives it feels like an overdue and needed change. I don't think. Much will change. At the individual pod level. I think. The dynamics will be mainly like. Who we're working with across pods so you might see some changes at that level the other change is there's an open position for someone to work under conno directly on the enterprise side. So I think that can only be positive as well you know Connor's overstretched and getting someone good in to be more focused on just your product domain would be awesome. So I'm not I'm optimistic is the honest answer.  
Them: Yeah I'm just curious since like you know the guest journey area was trying to have like area meetings and stuff like that. So it's like. Pod shifting of that impacts anything.  
Me: I feel like. For enterprise there's no like natural group of. Sibling parts. It tends to vary you know we're doing gas journey messages this month so we need to have a lot of contact with that pod or something. Internal tools we have a lot of crossover. But I think you've already got good lines of communication with Stephanie and Laura and stuff. But I'm open to it like if you if you want to think of defining more. Above part kind of formal communication and stuff but I think it's worth exploring for sure.  
Them: I'm not sure. If our group needs it or not I think I just saw like me a pod got pulled in to guest journey. So.  
Me: There are a few like pretty weird. Fits in the in the structure I've seen. Again I haven't seen that it's finalized in any way and it might change. So let's cross that bridge. When we come to it.  
Them: Okay yeah just figured I'd ask if you'd heard anything on our side.  
Me: Cool. What's I can't see the preview of this linear tick. Et.  
Them: Is just onboarding scripts that add to child conditional. We were going through this in 2000. No one had much more context on it.  
Me: Fair. Enough. I. What I'm saying here and I think it's directly relevant to work you've just been looking out for. The idea of foreign vendors that need to be removed basically. We had this new problem when we started doing IHG hotel keyboarding where the normal process was run the configuration and then go straight to go live. The problem here is that. Now that process goes from. Initial configuration PMS creation PMS validation then go live but unlike window or vs western when where every hotel needs to go through PMS. Creation. Now we're putting a bunch of hotels which which are not hotel key they're oh hip or whatever and they don't need that they still have to go through those stages. So the idea was like at the end of a batch run. Or at the end of a hotel run. On the hotel level you could look at the hotel and say is this hotel key? If so configure PMS else go straight to go live. And have like a branching. Like a flow chart through the stages of an onboarding. It feels low value like nice to have kind of work. I will make a note to add that context to the ticket.  
Them: Okay and that would basically try to remove the logic out of the plan which makes the plan a no op and rather just not include the plan in the list.  
Me: Wants to take a number 6145. I'll update you it will be what I just said to make that really clear. And the IHG example. Oh. Yeah I put in a couple things here. Lots of shared a doc thinking about ID concepts above the level of. Like the current hotel staff maybe having multiple links between. Users of different accounts I put a comment on the doc just saying this really needs to be considered in the light of the wider identity work the stuff that you saw when you were doing the OAuth piece and the global users table and all of that stuff. Which I only. Sort of. I didn't go line by line through his dog but I didn't see much evidence the huge fully read those things he might just not be aware so I have had a comment to that effect. That's just for general awareness I think he put that dot together on his own initiative as an idea which is great. I just wanted you to be generally aware that I stayed in that direction.  
Them: Okay yeah I think that dog came out of having. I think at least two tickets where users are members of multiple SSO orgs. Them all in one dashboard and even one above property view.  
Me: Yeah I don't know if we should support that but it's good to think about it either way. Cool. Just wondering if you have any thoughts about the next block which we're going to start planning in a week or so. Oh yeah the other thing I wanted to reflag was. The draft PR I sent you last week on enterprise portfolio reconciliation using the sources of truth that we have to. Keep those portfolios up to date I know you. Had. Correct thoughts about just this should be automated which I fully agree with except that. I know from having like done the manual version of this before using. Like scripts that I wrote rather than trying to formalize it. You hit so many special cases. And the process of going through the special cases kind of forces you to. Deal with. The kinds of things we should be dealing with before automating it. I think at least one more round of that would probably be good. To give us the information like of whether or not it can be automated so that was long-winded but hopefully came across.  
Them: Um re sharing the PR that has like somehow dropped off of my notice so I didn't mean to ignore it.  
Me: No worries. Okay it's my DM on Thursday. At 4 p.m but so that'll be 9am.  
Them: Okay. Sorry I think I missed the link in there. So I will give that a read today.  
Me: Cool. Awesome. What. Else. Oh. Yeah chinchos and edge designs let me know what you're thinking.  
Them: He's had done two in the last couple of days and the first one was. A lot of AI word salad. And so. I went through with plodge and had that do a terse one and I had it use like the in stage template just because it had some sections and some things. But then I found even the one that he just did for. This like drift. It felt like a lot of words and not a lot of actual like details or like.  
Me: Yeah.  
Them: Direction. I don't know if he has done edge design before if you've worked through them with him.  
Me: It was actually a specific review feedback to him that he should look for opportunities to do edge design because he hadn't done done one up until the review last couple of weeks so it's good that this is coming up. As in the opportunity for him. I gave really similar feedback to Andres when he turned in the first version of our property call lists it was like literally twice as long as it needed to be and it was obviously. AI. And not not slot but like I think he. He was able to he'd reviewed it and stood behind it and I didn't have that many. Factual or technical like objections it was just too long and I think. He responded well to me saying look you know just covers it off like respect the reader's time and I think. I would be quite strong about doing that feedback because it's important. It's really important. I think. I can't remember in which stack thread it was but I think now they've posted something basically saying if you want effort from readers show effort yourself like literally no one wants to read. Output. Did you have concerns about. Accuracy of content or do you just feel it didn't represent hard like a. Proper attempt at the task.  
Them: I think especially on the one for the drifts I have concerns because it didn't feel like there was actually a lot of engineering detail. There was a lot of words. And there was like add these two fields to a model but there wasn't a lot else specifically engineering. And so. Like yeah I. Want to. My plan is to go and it like try to get him to go. Super detailed engineering wise on these. Like plan this as like an onboarding project that someone else will have to do based off of this. I was curious if yeah, if you had seen this and if you had any other like thoughts on feedback.  
Me: I think. I haven't seen it because he hasn't done much engineering design up to this point so it's good that he's doing it. I think the only directive I give is that this stuff's really important like as an organization we're going towards something like spec driven development. So really. Accurate test technical communication is like. One of the vital skills we need to work towards so you you're we're not doing anyone any favors by soft pedaling feedback on bad dogs.  
Them: Sounds good just wanted to yeah. Find out if you had seen this before or if this was a first first go for him.  
Me: Now. Do you want me to look at those or hold back or what's what's your preference?  
Them: Why don't you wait until I'll have him do another pass on them and then take a look.  
Me: Cool yeah the only other thing is just a general question about. Whether you want to push particular things into the next planning block and whether I can support that.  
Them: I mean I think the things. That we're thinking about I think if we can continue making progress on these I think we these kind of clean up things I think we might really want to push if there's bandwidth starting to go through each of the onboarding plans and assigning like the drift values to them like once we prove that out because I think that will be really helpful. I think. I think the other question is if we push like the self serve SSO. There were some I think I think those are the only things I don't think I have. Any other context of like engineering specific projects right now.  
Me: Cool and probably omni migration will be in this next block or is that following quarter?  
Them: I think that'll be this block because connor thinks it'll be late September or October that it needs to be done. My sort of plan. Depending on what it looks like with lauta thinks is if we could kind of distribute that among the team rather than have it as like someone's focus for a couple of weeks.  
Me: So that's the SCIM work and that would mean that. An external identity provider could effectively deactivate. A user. Which they can already stop them from logging in but we're saying they could also. Remove them from what admins see so there's no confusion. And stop username password login as well by deactivating user.  
Them: Exactly.  
Me: Yeah that feels like a big gap in what we're offering to proper enterprise level SSL orgs at the moment so yeah I agree with that.  
Them: Yeah, so I think there's that and then there's. Taking that like above property work that Lalta did and making it. Self serve as well so they can start inputting values and things. I think there's some thought. We have to put in specifically on the like role mapping. Part of things which I think to make that user friendly to not canary engineer person. I think that will be the interesting ux part of things.  
Me: Cool. I'm aligned on those. Feeding anything else I can think of. Do you mind sorry.  
Them: That I.  
Me: You guys are sorry.  
Them: Was just wondering that identity work that Jordan's been doing does that have a home and an owner for next block?  
Me: Yes it will oh that's a good point I heard about this yesterday it's not going to be. Under me it's going to stay under Jordan as like a mini identity pod so sort of what had been discussed but I think. This makes total sense like Jordan has all the context he should keep running it. And I think that was recognized. So nothing for us there. Had a quick thought what was it? Oh yeah. Do you want me to take a high level like not an engineering design run. At a PID for. Onboarding scripts using rules based just to set out like goals and parameters rather than. Design.  
Them: Yeah, I think that would be great.  
Me: Awesome. All right I'll take a go at that and let you know when it's done. Anything else on your mind?  
Them: No that was all I had this week.  
Me: Good canary energy level.  
Them: Yeah doing good.  
Me: Good to hear it thanks for everything Andrea it's it's really amazing that how you're running the team at the moment I really appreciate it.  
Them: Have a good week.  
Me: Cheers. By.