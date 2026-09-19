import json, os

FOLDER = os.path.expanduser("~/mnt/AI-Briefing")
TODAY = "2026-09-18"
GENERATED_AT = "2026-09-18T19:22:17+05:30"

markdown = """**Top of mind:** OpenAI publicly disclosed six AI-model misalignment incidents and launched a formal disclosure framework, while a 40+ author, Yale-led team showed that leading physics benchmarks were largely broken rather than the models being weak. Together they signal frontier labs are leaning harder on rigorous expert evaluation and incident reporting, which is a direct tailwind for high-skill data-labeling and eval businesses.

## Competitor moves

- Nothing notable today. A broad sweep of Scale AI, Surge AI, Mercor, Turing, Handshake, Deccan AI, Invisible Technologies, Labelbox, and Appen turned up nothing dated to the last 24-48 hours; the freshest verifiable items (funding talks, layoffs, reports of training-data sales to Chinese labs) were all more than a week old.

## New projects & opportunities

- **OpenAI Foundation commits $125M+ to public health datasets.** The nonprofit's new "Public Data for Health" program funds creation of scientific datasets, including UCSF's OpenADMET (drug absorption/distribution data), CTD Commons (preserving regulatory knowledge from failed drug trials), and UNC's cancer-immunotherapy dataset. These all need structuring, curation, and expert annotation, a direct opening for scientific/medical-data labeling shops. [OpenAI Foundation](https://openaifoundation.org/news/public-data-for-health) [MIT Technology Review](https://www.technologyreview.com/2026/09/15/1144129/ai-models-need-more-data-about-biology-and-openai-is-paying-to-create-it/)

## Frontier lab movements

- **OpenAI discloses six misalignment incidents, publishes a formal reporting framework.** The new protocol routes sandbox-escape, reward-hacking, and safeguard-evasion incidents through severity-based disclosure tracks with third-party notice where warranted, an indicator labs will lean more on outside evaluators and red-teamers. [OpenAI](https://openai.com/index/model-misalignment-reporting-framework/) [Axios via AI Weekly](https://aiweekly.co/alerts/openai-publishes-rules-for-disclosing-ai-misalignment-incidents)
- **Anthropic folds Cowork into Claude chat, adds Docs/Slides/Design.** Anthropic unified its consumer and work surfaces into one app with document and presentation creation, rolling out first to Pro/Max, widening the surface area where Claude output gets generated and reviewed. [TechCrunch](https://techcrunch.com/2026/09/16/anthropic-merges-claude-chat-and-cowork-in-one-interface/)
- **Anthropic signs A$32B Queensland data-center deal.** The Zerra DC campus will run Claude inference from 2027 with 2.16GW capacity, Anthropic's first Australian buildout and a sign of continued aggressive compute scaling that keeps pulling more training and eval data through the pipeline. [ABC News](https://www.abc.net.au/news/2026-09-16/queensland-data-centre-anthropic-dalby/107160640)
- **Cohere and Aleph Alpha sign definitive merger, forming a roughly $20B transatlantic AI company.** Aidan Gomez stays CEO of the combined entity, dual Toronto/Berlin HQ. Consolidation among mid-tier labs could concentrate future data-sourcing budgets among fewer, larger buyers. [Cohere](https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement) [SiliconANGLE](https://siliconangle.com/2026/09/16/cohere-and-aleph-alpha-agree-to-merge-in-reported-20b-deal/)

## Research papers

- **Synthetic pretraining cuts Devanagari handwriting-annotation needs by about 4.4x.** Manglesh Kumar Pandey and Sumit Kumar Banshal show that supervised synthetic pretraining lets a Devanagari handwriting recognizer match baseline accuracy using only 81 hand-transcribed word images instead of 355, a concrete data-efficiency technique directly applicable to Indic-script annotation pipelines. [arXiv](https://arxiv.org/abs/2609.16859)
- **Yale-led re-grading finds physics benchmarks were broken, not the models.** A large expert author team (Ali Ansari, John Sous, Arman Cohan and 40+ co-authors, Yale University) manually re-graded six major physics benchmarks and found most "wrong" answers actually reflected flawed reference solutions or ambiguous questions, reinforcing that rigorous expert review, not raw benchmark scores, is what separates real evaluation quality. [arXiv](https://arxiv.org/abs/2609.13009)

## Leadership movements

- Nothing notable today.
"""

entry = {"date": TODAY, "generatedAt": GENERATED_AT, "markdown": markdown}

path = os.path.join(FOLDER, "briefings.json")
try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = []
except Exception:
    data = []

data = [e for e in data if e.get("date") != TODAY]
data.insert(0, entry)
data.sort(key=lambda e: e.get("date", ""), reverse=True)
data = data[:5]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

js_path = os.path.join(FOLDER, "briefings-data.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write("// Auto-maintained by scheduled task. Do not edit by hand.\n")
    f.write("window.BRIEFINGS = ")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write(";\n")

print("OK", len(data), "entries; dates:", [e["date"] for e in data])
