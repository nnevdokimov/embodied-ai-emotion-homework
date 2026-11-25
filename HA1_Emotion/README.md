# HA1 Emotion group

The notebook contains results and plots; [interpretation.md](interpretation.md) contains the 300-word interpretation.

The verified environment uses Python 3.12. Install `requirements.txt`, then run all notebook cells from the extracted folder. All input data are included; running the analysis requires no downloads. The frequency cache also supports running without wordfreq installed.

## Inventory and method

All twenty concepts are from the instructor's list, with `angr` and `freeaze` corrected to `anger` and `freeze`. The revised HA0 uses the same terms, senses and six shared features. Physical anchors retain literal noun senses; the notebook gives separate emotional extensions.

The notebook reads the HA0 inventory, adds the proprioception annotation by concept ID and joins the source means by ID and spelling. Both primary axes use sample min–max scaling. Values at 0.5 are listed separately. The notebook compares rank and z-score scaling, tests haptic alternatives for three ambiguous senses, enumerates all four missing social scores, removes the entire social channel and tests the original held-out prediction.

## Sources and provenance

- Five channels: [Lancaster Sensorimotor Norms](https://osf.io/download/48wsc/) (Lynott et al., 2020), adapted under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Columns: Visual.mean, Auditory.mean, Haptic.mean, Max_strength.action, Interoceptive.mean. Scores 0/1/2 use cutoffs 5/3 and 10/3 on the original 0–5 scale.
- Socialness: [Diveica et al. norms](https://raw.githubusercontent.com/DiveicaV/Socialness-LexicalSemanticProcessing/0c4dccc0e62664ea1c6afa101dcab67e00401753/Study1/Data/Properties_data/SocialnessNorms_DiveicaPexmanBinney2021.csv) (2023). Scores use cutoffs 3 and 5 on the original 1–7 scale. `heaviness`, `flood`, `sting` and `scar` are absent: their scores of 0 are generated, with blank source means. The notebook tests all 81 possible replacements for these scores.
- All twenty proprioception scores are generated; rationales are stored with the data. Overall, 116 of 140 feature values are sourced and 24 generated.
- Senses and hypernyms: [WordNet 3.0](https://wordnet.princeton.edu/). `data/wordnet.zip` includes the original noun data, license and citation. Every selected entry has one direct hypernym; selected senses are fixed by noun offsets.
- Frequency: Robyn Speer, [wordfreq 3.1.1](https://pypi.org/project/wordfreq/3.1.1/), English large list. The bundled subset is under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); corpus attribution is in [wordfreq NOTICE](https://github.com/rspeer/wordfreq/blob/master/NOTICE.md). Zipf − 3 gives log10 occurrences per million words. Metadata record the cache hash and extraction settings.

Raw norm means are in `data/source_means.csv`, joined by lowercased exact word. Ratings and frequency are word-level, not specific to the selected WordNet sense. Definitions, examples and field-level provenance are in the bundled revised HA0 CSV. No random sampling is used.

## Evidence for proprioception

The weight-matching experiment of Gandevia and McCloskey measured perceived heaviness while changing sensory input during lifting. It supports a role for bodily feedback in judgments of a lifted load. Our 0–2 lexical bin remains a generated annotation. One team participant supplied a separate rating of 2 after seeing the audit. This single unblinded judgment is recorded in data/heaviness_review.csv. The notebook tests removal of this channel. [Primary experiment](https://pubmed.ncbi.nlm.nih.gov/592207/)
