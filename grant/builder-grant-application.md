# fal Builder Grant Application Draft

> **Use only after ContinuityForge has a direct, user-facing generative-media experience and you have an approved partner/referral path.** As checked on 2026-08-31, fal describes Builder Grant eligibility as bootstrapped/indie teams in Europe or Asia building a direct generative-media app; applications are currently available through approved partners.

**Product name:** ContinuityForge  
**Applicant / team:** [NAME]  
**Country:** [COUNTRY IN EUROPE OR ASIA]  
**Website:** [URL]  
**Public repository:** https://github.com/aexlpeng/continuityforge  
**Product demo:** [REQUIRED DEMO URL]  
**fal account email:** [EMAIL]  
**Approved partner / referral code:** [CODE]

## What are you building?

ContinuityForge is a direct generative-video workflow that lets a creator turn an original script and character bible into a planned sequence of 5- and 10-second animated shots. It preserves explicit character, prop, location, and end-frame state across shots; routes each shot to a compatible fal endpoint; and records a reproducible production manifest. The user reviews the storyboard before any paid generation and can regenerate or repair only the failed shot.

## Who is it for?

Independent animators, educators, and small creative teams who want to produce original one-to-five-minute animated stories but cannot manually manage dozens of disconnected model calls and continuity notes.

## Why is generation the core experience?

The product's primary output is newly generated visual media. Script parsing and planning exist to control the video-generation process; they are not an internal-only AI feature. Users select or approve shots, generate media through fal, compare attempts, and assemble approved clips.

## How will you use fal?

- Image/keyframe generation for locked character and location references
- Image-to-video and text-to-video generation for 5s/10s shots
- Queue-backed retries and request tracking
- Model routing based on shot duration and capability
- Controlled A/B evaluation of cost, latency, and continuity

The server-side Python adapter uses the official `fal-client`; API keys are never exposed to the browser.

## Current stage

[CHOOSE ONLY WHAT IS TRUE: prototype / private alpha / public beta]. The open-source orchestration scaffold is complete. Current evidence: [USERS], [GENERATIONS], [WAITLIST], [REPOSITORY STARS], [DEMO].

## What will the credits unlock?

[Starter / Plus / Launch] credits will fund [FIRST END-TO-END TESTS / PRIVATE BETA / LAUNCH TRAFFIC]. The immediate target is [NUMBER] users producing [NUMBER] shots across [PERIOD]. We will cap retries, cache successful shots, and track per-user generation cost.

## Bootstrapping status

The project is [SELF-FUNDED / PRE-REVENUE / REVENUE DETAILS]. The team has [NUMBER] people and has raised [NONE / ACCURATE DETAILS]. Credits will be used only for this product's generative-media calls and will not be resold or transferred.

## Next milestone

Within [NUMBER] weeks of approval, we will ship [SPECIFIC USER-FACING MILESTONE], onboard [NUMBER] testers, and publish [WHAT WILL BE PUBLIC].
