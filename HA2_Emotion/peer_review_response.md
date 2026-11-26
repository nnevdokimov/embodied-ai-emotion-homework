# Response to peer review

The [received review](HA2_Emotion_Peer_Review.pdf) examined [a6e39ac](https://github.com/nnevdokimov/embodied-ai-emotion-homework/tree/a6e39acc28a10dabbe310e5567b94f9058d1a40c/HA2_Emotion) and accepted the numerical results with minor revisions. Both review PDFs are preserved unchanged.

| Comment | Response |
| --- | --- |
| Distinguish source evidence from authored examples. | The figure legend now identifies WordNet ancestry and generated examples. Research links have a separate `motivating_literature_url` field. Both freeze edges state that the selected sense is a general interruption or pause. |
| Identify the panic edit as a redundant ancestor shortcut. | The methods, multiple-parent table and perturbation explanation use this label. An assertion checks that panic's ancestor set is unchanged; both paths still span seven WordNet steps. |
| Explain disconnection and score units. | The write-up and CSV distinguish the branch cut from deleting both incoming panic edges. A check confirms that restoring the emotion branch alone leaves panic isolated. Mood's increase is stated as 0.333 score points. Figures label scar's withheld baseline link separately from nodes detached from entity. |
| Carry sense uncertainty into HA2. | Node tables retain the HA0 `uncertain` and `uncertainty_note` fields. Warmth is explicitly thermal; freeze denotes a general interruption or pause. |
| Report breadth coverage. | `results/coverage_summary.csv` reports 15/24 leaves among reachable nodes and 15/19 among reachable inventory concepts. The existing flood expansion remains a separate coverage test. |
| Provide regression checks and a manifest. | `verify_submission.py` independently enumerates root paths and descendants, checks the 75 comparisons, fixed-root coverage, association invariance and exact edit sequence. `manifest.json` records SHA-256 hashes of inputs, outputs and notebook source cells. |
| Document headless execution. | The README gives the kernel-registration and nbconvert commands. The runner is pinned in requirements; this revision is checked on Python 3.12.13. The independent review reports Python 3.12.14. |

The baseline retains 25 nodes and the same three additions and removals. Compact-depth and hop-weighted comparisons remain separate. Independent multiple inheritance and expansion of several leaves across branches are useful follow-up experiments; the present experiment tests an ancestor shortcut. The hierarchical fallback follows the instructor notebook. A full transitive dependency lock would be appropriate if identical bytes across environments become a requirement.

Our [outgoing review](HA2_Peer_Review_Team_10_Detailed.pdf) covers the Space and Movement submission at e501db9.
