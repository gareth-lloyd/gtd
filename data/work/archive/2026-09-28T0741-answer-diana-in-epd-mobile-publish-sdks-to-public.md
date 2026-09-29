---
area: null
completed_at: 2026-09-28 14:48:51.202209
contexts:
- react
created: 2026-09-28 07:41:13.722821
defer_until: null
due: 2026-09-28
energy: medium
id: 2026-09-28T0741-answer-diana-in-epd-mobile-publish-sdks-to-public
order: null
output: |
  ## Agent run 2026-09-28T14:12:47+03:00

  Nothing was sent or posted. Research was read-only. A draft Slack reply is at the bottom.

  Thread: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790328396587869?thread_ts=1790328396.587869&cid=C09M5GRJPL2

  ### Bottom line

  Diana's core argument holds: gating the download protects little, because the SDK already ships inside every
  customer's App Store / Play Store build. The proposal is sound in direction. It is not ready to execute: there
  are five concrete blockers (licence, changelog content, npm naming, Android obfuscation decision, registry
  ownership), all fixable. Two cheap steps are worth doing now regardless of the decision: claim an npm scope
  and verify the Maven Central namespace.

  ### The repos Blake asked for

  Source repos (GitHub visibility: internal):
  - https://github.com/canary-technologies-corp/canary-sdk-ios (latest v1.3.12)
  - https://github.com/canary-technologies-corp/canary-sdk-android (latest 1.7.2)
  - https://github.com/canary-technologies-corp/canary-sdk-js (latest v1.3.14, package `@canary/react-native`)
  - https://github.com/canary-technologies-corp/canary-sdk-core (C++ core, untouched since 2025-11-21, no releases)

  Distribution repos, which are what customers are meant to consume and what would become public:
  - https://github.com/canary-technologies-corp-dist/canary-sdk-ios-dist
  - https://github.com/canary-technologies-corp-dist/canary-sdk-android-dist
  - https://github.com/canary-technologies-corp-dist/canary-sdk-js-dist

  NOT VERIFIED: I could not open the dist repos. They return 404 to my GitHub token and anonymously, so they are
  private and I am not a member of that org. Blake may hit the same wall. Contents below are inferred from the
  publish workflows in the source repos, not from the dist repos themselves.

  ### What each artifact would expose

  | SDK | What ships | Readability |
  | --- | --- | --- |
  | iOS | Compiled XCFramework (built with BUILD_LIBRARY_FOR_DISTRIBUTION, so it includes .swiftinterface files listing the public API), plus Package.swift, COPYRIGHT, CHANGELOG.md | Low. Compiled binary. |
  | Android | AAR + POM in Maven layout | High. `isMinifyEnabled = false` in `canary/build.gradle.kts`, so no R8 obfuscation. Decompiles to readable Kotlin with original names. |
  | React Native | tsup JS bundle with `sourcemap: true`, plus the Swift/ObjC and Android bridge code as source, podspec, README, CHANGELOG | High, but it is a thin bridge over the native SDKs. |

  No third-party lock-vendor binaries are vendored in any of the three, so I found no third-party
  redistribution problem. No hardcoded secrets turned up in a hostname/credential grep. Shipped source does
  reference staging.canarytechnologies.com and test.canarytechnologies.com. `secretKey` is deprecated on both
  platforms ("authentication now uses device attestation"); I found a device keystore identity
  (`AndroidKeystoreDeviceIdentityStore`, iOS `SecureKeyStore`) but no App Attest / Play Integrity calls, so
  "attestation" here means a device keypair, not platform attestation. Worth confirming with the mobile team
  since the whole security argument rests on runtime auth.

  ### Blake's question: public but unlisted?

  - npm: no. Every public package is searchable.
  - Maven Central: no. Everything is indexed.
  - SPM: there is no central registry. "Publishing" means making the dist git repo public. It is not listed
    anywhere unless someone submits it to Swift Package Index, but a public GitHub repo is findable by search.
    Francisco's answer in the thread is right.

  ### Issues found

  1. Licence contradiction (blocker). `COPYRIGHT` in all three repos says "proprietary and confidential",
     distribution prohibited, subject to the "Canary Technologies SDK License Agreement". The Android POM
     declares Apache License 2.0 (`canary/build.gradle.kts`, `pom { licenses {...} }`). On Maven Central the POM
     is the public licence statement. Legal needs to supply wording that allows public download but restricts
     use to customers. I found no Slack mention of the SDK License Agreement, so whether it exists is an open
     question.
  2. Changelogs leak internal detail (blocker). CHANGELOG.md is copied wholesale into each dist repo. Counts:
     iOS 193 Linear ticket IDs and 35 "Internal" sections; Android 106 and 25; JS 85 and 10. They also name
     flavor codenames (Aspen, Monaco, Kyoto). If a flavor maps to a customer, that is customer information.
     Needs a scrub or a public/internal split before anything goes public.
  3. npm naming (blocker, and the live risk Diana mentioned).
     - `@canary` scope: appears to be owned by someone else (npm org endpoint returns 200; our other candidate
       scopes return 404). So the source package name `@canary/react-native` is not available to us.
     - Unscoped `canary-sdk` is taken by an unrelated company (Canary QA, LLM monitoring, published 2026-03).
     - `@canary-technologies-corp-dist`, the scope customers configure today, is unclaimed on public npm. A
       customer whose scope-to-registry mapping is missing falls through to public npm, so anyone who registers
       that org could serve them a package. Claiming it closes this regardless of the publish decision.
     - `@canarytechnologies` and `@canary-technologies` are both unclaimed as of today.
  4. Android obfuscation is a decision, not a bug. Shipping unminified is normal for libraries, but it means
     the public artifact is the most readable of the three. Decide whether that is acceptable or whether to
     obfuscate internals and keep the public API.
  5. Permanence. Maven Central releases cannot be deleted or changed. npm unpublish is restricted after 72
     hours. A bad or leaky release gets superseded, never retracted. This is the main real difference from
     today, where we control every copy we hand out.
  6. Maven Central entry requirements not met yet: verified namespace for `com.canarytechnologies` (DNS TXT
     record), GPG-signed artifacts, sources and javadoc jars (placeholders are allowed for closed source),
     complete POM. The current build applies `maven-publish` only, no signing. The POM's SCM URLs point at
     `canary-technologies-corp/canary-android`, which is not the repo name.
  7. The three are coupled. The RN package depends on the native SDKs: the Android bridge pulls
     `com.canarytechnologies:canary-sdk:1.7.2`, and `CanaryReactNative.podspec` resolves CanaryKit from the
     internal source repo `canary-technologies-corp/canary-sdk-ios.git`, pinned to 1.3.11 while iOS latest is
     1.3.12. Public npm only helps if both native artifacts are publicly resolvable too. NOT VERIFIED: whether
     the podspec is rewritten anywhere before publish; the workflow only copies it.
  8. Supply-chain ownership. Public registries make us a supply-chain dependency for hotel-brand apps. Needs a
     named owner for the npm org and Sonatype account, enforced 2FA, GPG key custody, and OIDC trusted
     publishing from GitHub Actions instead of long-lived tokens.
  9. Docs mismatch. Diana says the iOS zip is at an open URL. Today
     `https://docs.canarytechnologies.com/android/sdk/1.7.2/canary-sdk-1.7.2.aar` and
     `https://docs.canarytechnologies.com/releases` both return 401 (Basic auth). The iOS path uses an obscured
     segment and returned 403 rather than 401 on a directory probe, which is consistent with it being exempt
     from auth, but I could not confirm a real file URL without the checksum. The iOS README install
     instructions still say `https://github.com/your-org/CanaryKit`, and the Android README shows version 1.0.0.

  ### Alternatives

  | Option | Credentials needed | Indexed publicly | Upgrade = version bump | Notes |
  | --- | --- | --- | --- | --- |
  | A. Status quo (GitHub Packages + hand vendoring) | Yes | No | No | What Wyndham and Best Western reject today. |
  | B. Full public: Maven Central + npm + public SPM dist repo | No | Yes | Yes | Diana's proposal. Best tooling support. Permanent. |
  | C. Self-hosted open repos on our domain | No | No | Yes for Maven and SPM | Open Maven repo on S3/CloudFront, which we already populate, plus public SPM dist repo. Closest to Blake's "unlisted". npm has no good equivalent: a tarball URL works but loses semver ranges and update tooling. |
  | D. Hybrid: C for iOS and Android, public npm for RN | No | npm only | Yes | Exposes only the thin bridge in a public index. |
  | E. Per-customer tokens on a private registry | Yes | No | Yes | Does not fix the token clash customers complain about. |

  Recommendation: B is the right end state if legal signs off, since secrecy is not what protects us. If Blake
  wants lower visibility, D gets nearly all the customer benefit. Either way, do these first:
  claim the npm scope(s), verify the Maven namespace, get licence wording from legal, scrub the changelogs.

  ### Draft Slack reply (NOT sent; needs your explicit OK)

  Destination: thread in #epd-mobile, link above.

  > Sorry for the slow reply. I went through the three repos and publish workflows. I'm in favour of the goal, with a few things to sort out before we publish.
  >
  > 1. Secrecy isn't what protects us. The SDK already ships inside every customer's App Store and Play Store build, so anyone motivated can pull it out. Runtime auth is the real control. Agree with Diana.
  > 2. @Blake on unlisted: npm and Maven Central have no unlisted mode. SPM has no central index, so a public dist repo is only findable by search. If we want "no credentials but not in a public index", we can host an open Maven repo on our own domain plus a public SPM dist repo. npm has no good equivalent.
  > 3. What would be exposed: iOS is a compiled XCFramework. Android is an AAR with minify off, so it decompiles to readable Kotlin. RN is a JS bundle with source maps plus bridge source. The dist repos are canary-sdk-ios-dist, canary-sdk-android-dist and canary-sdk-js-dist in the canary-technologies-corp-dist org.
  > 4. To fix first:
  > • The Android POM declares Apache 2.0 while our COPYRIGHT says proprietary and confidential. Legal needs to give us wording that fits public distribution.
  > • Changelogs are copied wholesale to the dist repos, including Internal sections, Linear ticket IDs and flavor codenames.
  > • npm naming: `@canary` looks taken and unscoped `canary-sdk` belongs to another company. We need to pick and claim a scope.
  > • Maven Central and npm releases are effectively permanent, so we need a named owner for the accounts, 2FA and signing keys.
  > • The RN package only helps if the native artifacts it depends on are public too, so it's all three or none.
  >
  > Suggestion: claim the npm scope and Maven namespace this week, since that closes the squatting risk whatever we decide, and make the publish call once legal has looked at the licence.

  ### Caveats on this research

  - Dist repo contents inferred from workflows, not inspected (no access).
  - `@canary` scope ownership inferred from an npm API status code. Confirm by attempting to create the org
    on npmjs.com.
  - The repo's secret-read hook blocked reading `canary-sdk-js/.npmrc`. I left it unread; registry config was
    taken from the publish workflow and install docs instead.
  - Source repos were shallow-cloned into the session scratchpad for reading. Nothing was modified or pushed.

  ## Agent run 2026-09-28T14:16:30+03:00 (correction)

  The first run overstated one point. "The SDK already ships inside customer apps, so gating protects
  little" is too strong. Extraction from a shipped app is possible but clearly harder than reading the raw
  SDK. This supersedes the "Bottom line" wording and point 1 of the draft reply above.

  | Platform | From a customer's store app | From the raw SDK artifact |
  | --- | --- | --- |
  | Android | Our code is mixed into the host app. If the customer builds with R8 (normal for release builds), our internals are renamed, shrunk and inlined. Our `consumer-rules.pro` keeps only `CanaryInitializer`, so nothing else is protected from renaming. | Isolated AAR, unminified, original class, method and parameter names. Readable Kotlin in minutes with free tools. |
  | iOS | Store binaries are FairPlay-encrypted. Dumping one needs a jailbroken device. Symbols are usually stripped. | Unencrypted, includes `.swiftinterface` files with the full public API signatures. Still compiled code, so internals stay hard to read. |
  | React Native | JS is usually Hermes bytecode, minified, no source maps. | Bundle plus source maps (`sourcemap: true`), which normally carry the original TypeScript. |

  What still holds:
  - Download gating is not a security boundary. Every customer and their contractors already hold the raw
    artifacts, and a determined party can recover the code from a store app.
  - API endpoints and request shapes are visible to anyone who proxies a customer app's traffic.
  - Runtime auth is the control that matters.

  What changes with public publishing:
  - Effort drops from skilled reverse engineering to a casual download.
  - The audience widens from customers under contract to anyone, including competitors.
  - Android is where the gap is largest, so issue 4 (obfuscation decision) carries more weight than the
    first run gave it.

  NOT VERIFIED: whether Wyndham's and Best Western's apps actually build with R8 enabled, and whether
  CanaryKit is linked statically or dynamically (`build-xcframework.sh` sets no explicit Mach-O type or
  strip flags).

  Revised point 1 for the draft reply:

  > 1. Gating the download isn't a real security boundary: customers already hold the raw artifacts and runtime auth is the actual control. It does raise the effort, though. Pulling our code out of a store app is much harder than reading the raw SDK, especially on Android where our AAR ships unobfuscated. So going public is a real change in who can read our internals, and we should decide on Android obfuscation before we publish.
project: 2026-09-08-mobile
source_id: https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790328396587869?thread_ts=1790328396.587869&cid=C09M5GRJPL2
tags:
- morning-gtd
- slack
time_minutes: 15
title: 'Answer Diana in #epd-mobile: publish SDKs to public registries (SPM, Maven
  Central, npm)'
updated: 2026-09-28 14:48:51.202200
waiting_on: null
waiting_since: null
working_on: false
---

Agent work: examine the issues and alternatives

Diana tagged Blake and me. Wyndham and Best Western both vendor our binaries by hand today; public registries would make upgrades a version bump. Blake asked whether unlisted is possible and wants to see the external repos.
Open 2 days, no reply from me.
https://canarytechnologies.slack.com/archives/C09M5GRJPL2/p1790328396587869?thread_ts=1790328396.587869&cid=C09M5GRJPL2