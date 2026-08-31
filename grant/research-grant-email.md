# Research Grant Email Draft

**To:** grants@fal.ai  
**Subject:** fal Research Grant application — ContinuityForge, open-source multi-shot AI animation research

Hello fal team,

I’m [NAME], a [ROLE / SHORT CREDIBLE DESCRIPTION] based in [LOCATION]. I’m applying for a fal Research Grant for ContinuityForge:

Repository: https://github.com/aexlpeng/continuityforge  
Demo: [DEMO URL]

ContinuityForge is an Apache-2.0 orchestration and evaluation toolkit for turning 5- and 10-second generative-video shots into coherent one-to-five-minute animated stories. It addresses character and prop drift, dialogue/shot-duration mismatch, model routing, retry cost, and reproducibility through explicit start/end state contracts and generation manifests.

The initial codebase already includes a tested shot planner, continuity propagation, configuration-driven routing, a queue-backed fal adapter, dry-run manifests, an original episode fixture, and a human/automatic evaluation protocol. With grant compute, I plan to run controlled ablations across [NUMBER] original or permissively licensed episodes, comparing fixed-duration baselines, duration-aware planning, text and visual state propagation, and capability/cost routing.

I am requesting [AMOUNT] in fal credits for a pre-registered matrix of [BRIEF MATRIX]. The resulting prompts, configurations, manifests, aggregate results, failure taxonomy, and technical report will be published openly. A detailed proposal and budget are included in the repository under `grant/research-grant-application.md`.

fal is especially relevant because its common model API and queue infrastructure let the project compare multiple generative-video endpoints under the same reproducible pipeline—not simply because it provides compute.

Thank you for considering the project. I would be glad to share the experiment plan or answer technical questions.

Best,  
[NAME]  
[GITHUB / WEBSITE]  
[EMAIL]
