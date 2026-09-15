---
area: null
completed_at: null
contexts: []
created: 2026-09-11 15:40:30.412753
defer_until: null
due: null
energy: low
id: 2026-09-11T1540-what-are-bw-custom-views-contrasted-with-the-ihg-w
order: null
output: |
  ## Agent run 2026-09-11T16:05

  **Short answer:** it's the same Canary Mobile SDK for all three (iOS / Android / React Native wrapper). The difference is which UI layer the brand renders:
  - **IHG and Wyndham use a *flavor*.** They render Canary's own default views (CheckInFlow, Tipping, Upsells, Checkout, Chat, Key…), styled by a brand "flavor" that Canary builds and maintains. A flavor is a design-token/theme pack: fonts and weights, icon library, corner radii, border styles, background colours. Hotel colours and fonts also come from the backend. The app passes `flavor:` when it creates a view, e.g. `CheckInFlow(hotelSlug:…, confirmationCode:…, flavor: .iceCream)` ([Jason, #ihg](https://canarytechnologies.slack.com/archives/C03V5P4B48P/p1770154463794889?thread_ts=1770152568.002329&cid=C03V5P4B48P)). So Canary owns the pixels. Brand-specific design asks become Canary tickets: IHG deep blue #1F4456, IHG icons, 8px sheet radius ([thread](https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1777042433441299?thread_ts=1776973186.250279&cid=C09M5GRJPL2)); Wyndham's 12→16px font fix. Wyndham's owner said they'd "follow the out of the box Canary flows and customization options (fonts, colors, etc.)" ([Wyndham SDK / Mobile App](https://app.notion.com/p/2b681468615180d8adb2c235912e8653)). Canary is also building Wyndham's In-Stay screen around the SDK ([Wyndham In-Stay + SDK Scope](https://app.notion.com/p/2cd814686151805191ddd151c2d18852)).
  - **Best Western uses *custom views*.** BWH is rebuilding its app from scratch in React Native and wants no webviews. Its old integration embedded Canary check-in and compendium URLs as webviews ([BW Mobile Integration](https://app.notion.com/p/294814686151803e8547e7fe42e06142)). Per Bree, Shipra said explicitly that BW "plan to use their own custom built UI" ([#best-western](https://canarytechnologies.slack.com/archives/C07BX379GQK/p1775271556422989?thread_ts=1775241221.798579&cid=C07BX379GQK)). Custom views are an SDK extension point. Each flow exposes a closure/container slot that takes the brand's own view, and Canary passes down a **view model**: state plus action callbacks and enumerated events. Canary keeps the logic, API calls, state persistence and events; the brand draws every screen itself. In Swift this is a result builder, `CheckInFlowView(...) { MyCustomPaymentView ... }`. Any step the brand doesn't replace falls back to `DefaultXView`. It's type-safe; "the only way they can mess it up is if they don't call the callback" ([Jason's design thread, Oct 2025](https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1761849307772949?thread_ts=1761849307772949&cid=C09M5GRJPL2); iOS PR https://github.com/canary-technologies-corp/canary-sdk-ios/pull/3).

  **Nuances:**
  - The custom-view *feature* ships in every SDK. There are no prebuilt "default custom views": each brand writes its own. For BW handoff, Eric built sample `CustomCheckOutView` / `CustomUpsellsView` / `CustomTippingView` in RN (RN 1.3.0), only to prove the JS→native view-model bridge works ([handoff thread](https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1775050380474829?thread_ts=1775050380.474829&cid=C09M5GRJPL2); [release notes](https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1775245061382919); MOB-293 https://linear.app/canary-technologies/issue/MOB-293/build-custom-views-in-reactnative-for-each-flow).
  - BW also got a flavor ("Kyoto", shipped 4/17), but as an unrequested bonus, so they can fall back to default views if they want ([Best Western Flavor](https://app.notion.com/p/361814686151811fa9f1d09270d121e8)). Bree's intended taxonomy: a generic "Canary flavor" for anyone without custom designs, bespoke flavors for IHG and Wyndham, and BW on Canary UX with its own tokens ([thread](https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1775661905237799?thread_ts=1775656059.688889&cid=C09M5GRJPL2)).
  - The RN SDK wraps the native iOS/Android SDKs rather than using JSI. So BW's custom views are RN components, bridged to native view models.

  **Trade-offs (my synthesis):**
  - **Flavor (IHG/Wyndham):** faster integration, and Canary controls UX quality and consistency. The cost is ongoing Canary design and maintenance work per brand. Upgrades are also QA-heavy for the brand: IHG is pinned and gets patches rather than new versions ([thread](https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1782491700508039?thread_ts=1782418676.499239&cid=C09M5GRJPL2)).
  - **Custom views (BW):** the brand has full UI freedom and Canary does little per-brand UI work. But the view-model/event contract becomes a public API that must stay stable. Canary can't see or fix broken UX in the brand's views. Some internals, like compendium's inner sheets, weren't customizable as of Jan ([BW SDK 1/14](https://app.notion.com/p/2e8814686151805c99b2f6fb472b41ac)).
  - **BW status:** the SDK is "done for BW" (Jason, May). BW's app rebuild (Tellus) slipped into milestones, with the wide release around January. Bree offered for Canary to build BW's custom views from their designs if timing allows ([#best-western-mobile-app-project](https://canarytechnologies.slack.com/archives/C0AQLLSLGH0/p1779917851177909?thread_ts=1779915285.225939&cid=C0AQLLSLGH0)).

  Sources are Slack #epd-mobile / #best-western / #ihg and Notion. I didn't read the SDK repos directly.

  ## Follow-up 2026-09-11T16:20: technical stack for custom views (read from the SDK repos via gh)
  - **iOS** (https://github.com/canary-technologies-corp/canary-sdk-ios): Swift 6, SwiftUI, Swift Package `CanaryKit`. Custom views plug into a result-builder block on `CheckInFlowView(...) { ... }`. Each step type (LandingView, ReviewReservationView, RegistrationView, AddPaymentView, UploadIdView, SignatureView, AddonView, SelectMobileKeyView) takes a closure that hands the brand's view an `async throws` submit/continue function. The SDK keeps orchestration: service calls and step advancement. See Examples/CanarySample-iOS/.../CustomViews/BareCheckInFlow.swift. Rough edges: `UploadIdView` takes loose primitives with a wire-string idType. `CheckInCompleteView` is `package`, not public (MOB-1207).
  - **Android** (https://github.com/canary-technologies-corp/canary-sdk-android): Kotlin, Jetpack Compose (Material3), coroutines, kotlinx.serialization, OkHttp; minSdk 24. The shape is a headless handle: `Canary.tipping(hotelSlug, conf)` returns an object with `state: StateFlow<Tipping.UiState>` (sealed class) plus action methods. The host app renders its own composables with `collectAsState()`. See sample/.../customviews/CustomTippingView.kt.
  - **React Native** (https://github.com/canary-technologies-corp/canary-sdk-js, `@canary/react-native`; RN >=0.80, React 19, Expo config plugin): a thin TypeScript layer over the native SDKs. Old-architecture bridge: `NativeModules.CanaryBridge`, `RCT_EXTERN_MODULE` + Swift on iOS, `CanaryBridgeModule.kt` on Android; promise-based methods. No TurboModules/JSI. Custom views = React hooks acting as view models (`useTipping`, `useCheckInFlow`, `useCheckOut`, `useAddons`, `useMobileKeys`, `useHotel`, `useReservation`…) returning state plus actions, rendered with plain RN components. Stock views are native SwiftUI/Compose screens embedded through ViewManagers (`ComposeHostingView`).
  - **Takeaway for BW:** their RN custom views sit on hooks → old RN bridge → native Swift/Kotlin SDK → Canary API. So BW ships Canary's native binaries even though its UI is pure JS. Every hook's state/action shape becomes a contract Canary has to keep stable.

  ## Follow-up 2026-09-11T16:35: Notion page updated (user approved "yes")
  Added a "Brand integration models: flavors vs custom views" subsection to section 2 of [Mobile Pod — Jason Flax departure impact & landscape](https://app.notion.com/p/3d78146861518160bb80ece5ac5feb64). It sits after "Current themes" and before "Also owned beyond the SDK code". Contents: a flavor-vs-custom-views table by brand, the per-platform stack (iOS / Android / RN), implications, and source links. No existing content was changed. I re-read the page after the write to confirm it.
project: 2026-09-08-mobile
source_id: null
tags: []
time_minutes: 5
title: What are BW custom views contrasted with the IHG / Wyndham SDK approach to
  mobile dev?
updated: 2026-09-14 13:03:58.137003
waiting_on: null
waiting_since: null
working_on: true
---