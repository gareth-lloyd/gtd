---
area: null
contexts: []
created: &id001 2020-04-08 00:00:00
defer_until: null
due: null
energy: null
id: 2020-04-08T0000-investigate-hasura
project: 2021-05-10T0000-pariti
tags: []
time_minutes: null
title: Investigate hasura
updated: *id001
waiting_on: null
waiting_since: null
---

https://hasura.io/
with graphql generator: https://graphql-code-generator.com/

Hasura by far, lets you point-and-click build your database and table relationships with a web dashboard and autogenerates a full GraphQL CRUD API with permissions you can configure and JWT/webhook auth baked-in.
https://hasura.io/

I've been able to build in a weekend no-code what would've taken my team weeks or months to build by hand, even with something as productive as Rails. It automates the boring stuff and you just have to write single endpoints for custom business logic, like "send a welcome email on sign-up" or "process a payment".

It has a database viewer, but it's not the core of the product, so I use Forest Admin to autogenerate an Admin Dashboard that non-technical team members can use:

https://www.forestadmin.com/

With these two, you can point-and-click make 80% of a SaaS product in almost no time.

I wrote a tutorial on how to integrate Hasura + Forest Admin, for anyone interested:

http://hasura-forest-admin.surge.sh

For interacting with Hasura from a client, you can autogenerate fully-typed & documented query components in your framework of choice using GraphQL Code Generator:

https://graphql-code-generator.com/

Then I usually throw Metabase in there as a self-hosted Business Intelligence platform for non-technical people to use as well, and PostHog for analytics:

https://www.metabase.com/

https://posthog.com/

All of these all Docker Containers, so you can have them running locally or deployed in minutes.

This stack is absurdly powerful and productive.