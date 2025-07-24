### EvolAgent

Agent framework with
- Multi Agents
- Hierarchical Cross-Task Memory
- Meta Tool Learning
- RAG Knowledge Update
- Multi Paths Sampling for Self-Consistency

Command for running experiments.

Rename `.env.example` to `.env` and set environment variables.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
crawl4ai-setup
crawl4ai-doctor

export TOKENIZERS_PARALLELISM=true
mkdir -p "workspace"
python main.py
rm -rf workspace/*

pip freeze > requirements.txt
```

`Cognitive Architectures for Language Agents`.

Building on psychological theories, Soar uses several types of memory to track the agent’s state (Atkinson and Shiffrin, 1968). 

**Working memory** (Baddeley and Hitch, 1974) reflects the agent’s current circumstances: it stores the agent’s recent perceptual input, goals, and results from intermediate, internal reasoning. And that is the agent's current history.

**Long term memory** is divided into three distinct types. 

*Procedural memory* stores the production system itself: the set of rules that can be applied to working memory to determine the agent’s behavior. 

*Semantic memory* stores facts about the world (Lindes and Laird, 2016), while *episodic memory* stores sequences of the agent’s past behaviors (Nuxoll and Laird, 2007).

Priorities are:
`Procedual (System) > Semantic (Fewshots) > Episodic (Experiments)`