# AVATAR-Twin

Submission to the **NASA BPS Digital AVATAR Challenge**
Author: Nanthakumar R, New Way Concepts Research

AVATAR-Twin is a proposed digital twin of the astronaut bone marrow chip. It combines an exposure model, a mechanistic model of blood-cell production, a single-cell state layer, and a hierarchical Bayesian layer that separates crew-shared effects from donor-specific effects. New data updates the model through sequential Bayesian updating, behind a validation gate.

## What is in this repository

| Folder | Contents |
|---|---|
| `whitepaper/` | 8-page white paper (PDF, Word, Markdown source) |
| `slides/` | 7-slide presentation (PPTX, PDF) and the script that builds it |
| `video/` | 2 min 49 s narrated pitch video, subtitles (SRT), narration script |
| `code/` | Design-sensitivity simulation, partial-pooling demonstration, figure scripts |
| `figures/` | Figures used in the paper and slides |

## Run the code

```
pip install -r code/requirements.txt
cd code
python design_simulation.py      # how well can individual-response spread be estimated, by design
python twin_demo.py 0.5          # partial pooling on synthetic donors (noise level 0.5)
python make_architecture_figure.py
```

## Important notes

- **No AVATAR data were used.** The public AVATAR pages do not give chip counts, replicates or sensor details. Everything numeric in `code/` is synthetic and only shows how the method behaves.
- The twin design relies on published work; the paper lists 28 references.
- The video narration uses a synthetic (text-to-speech) voice.
- Claims about astronaut outcomes are hypotheses until the validation plan in the paper is carried out.
