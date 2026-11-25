HA0: EMOTION
Revised: 2026-11-25
Language: English
Team: Nikolay Evdokimov; Aleksandr Mandrov; Ivan Tsarikov; Egor Antonov

FILES AND SCOPE
HA0_Emotion.csv: 20 concepts; semicolon-delimited CSV, UTF-8 with BOM.
README.txt: feature schema, sources and reproduction rules.
Exit_Ticket.txt: modelling question, computational claim and weakening result.
One member submits the group's four-file package.

The inventory is the instructor's Emotion list. Two spelling corrections were applied: angr -> anger and freeaze -> freeze. No concepts were added or removed. The family includes emotion categories and bodily/physical anchors for emotional expressions, not only taxonomic subclasses of emotion. All selected WordNet senses are nouns. For example, warmth denotes heat sensation and flood denotes rising water; their emotional extensions are considered separately in HW1.

SCHEMA AND PROVENANCE
The CSV preserves the original column order. EM01-EM20 identify the concepts; wordnet_synset and category_parent_synset fix WordNet 3.0 noun offsets. Each definition has at most 20 words and excludes its own term or a morphological variant. category_parent is one direct hypernym. Example sentences use the selected sense.

The provenance JSON maps every other field to status (sourced/manual/generated), source_id, source_url, locator and method. Of the 120 feature values, 116 are converted published human ratings and 4 social scores (heaviness, flood, sting, scar) are generated low-confidence estimates because these words are absent from the Socialness Norms. Their source means remain unavailable; no published ratings are imputed. Seventeen definitions are verbatim WordNet definitions; emotion, fear and sting are paraphrased and marked generated. All 20 examples are generated.

FEATURES
visual: visual experience, Lancaster Visual.mean.
auditory: auditory experience, Lancaster Auditory.mean; not pronunciation of the word.
tactile: touch experience, approximated by Lancaster Haptic.mean.
motor: strongest action-effector association, Lancaster Max_strength.action; maximum of Foot_leg, Hand_arm, Head, Mouth and Torso means.
interoceptive: internal bodily experience, Lancaster Interoceptive.mean; not emotional valence.
social: broad social relevance, Socialness Norms Mean; not restricted to direct interpersonal interaction.

Published Lancaster means (0-5) are converted to 0 for [0,5/3), 1 for [5/3,10/3), and 2 for [10/3,5]. Published socialness means (1-7) are converted to 0 for [1,3), 1 for [3,5), and 2 for [5,7]. A cutoff enters the higher bin; the published decimal values are used without extra rounding. Zero denotes the low interval, not absence. These cutoffs are our explicit scale conversion, not values published by the norm authors.

For the four generated social scores, the rubric is 0 = low/incidental, 1 = context-dependent, 2 = central social relevance. The provisional low bin considers social roles, settings, values and interactions for each literal referent. Word-level associations remain uncertain. These estimates are separate from the norm-based conversion; each rationale is recorded in provenance.

UNCERTAINTY
The rows feeling, warmth and freeze carry uncertainty flags. The freeze noun synset covers a general interruption of movement or progress, not a specifically fear-induced response. All norm ratings describe words, not selected senses. Feeling can invoke touch; warmth can invoke affection; freeze can invoke cold. The ratings must not be presented as sense-specific measurements. This small, instructor-selected inventory is not a representative sample of emotions.

EXIT TICKET
Question: Does adding interoceptive strength improve prediction of independent socialness ratings for held-out Emotion concepts compared with visual, auditory, tactile and motor features alone?
Claim: For the Emotion concepts with published socialness ratings, adding interoceptive strength to visual, auditory, tactile and motor features will reduce leave-one-concept-out MAE for predicting socialness by at least 10%, compared with the same model without interoceptive strength.
Weakening result: An improvement below 10% would not support the prespecified effect-size claim; no improvement or worse performance would also weaken the directional claim.
Evaluate only the 16 concepts with published socialness ratings; exclude the four generated social targets. Use original continuous means, leave-one-concept-out ridge regression (alpha=1), training-fold standardization and a training-mean baseline. The 10% threshold is a prespecified practical criterion. HA1 tests this prediction using the protocol above.

REPRODUCIBILITY
1. Obtain the sources below and verify the two norm-file hashes and the WordNet data.noun hash.
2. Match lowercased Word to term exactly. Do not replace missing words with synonyms or inflections.
3. Apply the stated bins to five Lancaster columns and the 16 available socialness means. Retain the four explicitly generated social scores and their rationales.
4. Retrieve each WordNet noun record by offset; verify the stored direct hypernym. Preserve the fixed paraphrases, examples and selected senses from the CSV.
5. Check 20 unique terms and senses, six scores in {0,1,2}, definitions of at most 20 words, one parent, provenance for every field and the three sense-uncertainty notes.
No random computation is used. Fixed generated text and annotations are stored in the CSV; a new model run is not needed to reproduce this submission. The source hashes, 116 sourced feature values and all parent links were checked during preparation.

SOURCES
LANC: Lynott et al. (2020), The Lancaster Sensorimotor Norms.
Publication: https://doi.org/10.3758/s13428-019-01316-z
Data: https://osf.io/download/48wsc/
SHA256: 445d363fb1f9f3e50b86d88e2f46cdc9a22b5dd8a713ce4e7be2a773d57f43c5
License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
Modifications: selecting 20 words and converting five feature means to 0-2.

SOCIAL: Diveica, Pexman and Binney (2023), Quantifying social semantics.
Publication: https://doi.org/10.3758/s13428-022-01810-x
Data: https://raw.githubusercontent.com/DiveicaV/Socialness-LexicalSemanticProcessing/0c4dccc0e62664ea1c6afa101dcab67e00401753/Study1/Data/Properties_data/SocialnessNorms_DiveicaPexmanBinney2021.csv
SHA256: 59d15e0f57a96395e0ae2ecb0ed5eeab64ec77aa5c1438f7905ce50a1eb0cbb1
The article is CC BY 4.0; data are from the first author's public repository. Sixteen ratings were selected and converted to 0-2; four missing-word estimates are separately labelled generated.

WN30: Princeton University (2006), WordNet 3.0; Fellbaum (ed., 1998), WordNet: An Electronic Lexical Database.
Data: https://wordnetcode.princeton.edu/3.0/WNdb-3.0.tar.gz
data.noun SHA256: 489f145e0f68877c0be5bd0eb4117adaaac52f38f6204eb8d85dbe2158b614cc
Modifications: selecting noun senses and parents, paraphrasing three definitions, and adding examples and metadata. WordNet's required license follows.

FULL WORDNET 3.0 LICENSE
WordNet Release 3.0

This software and database is being provided to you, the LICENSEE, by  
Princeton University under the following license.  By obtaining, using  
and/or copying this software and database, you agree that you have  
read, understood, and will comply with these terms and conditions.:  
  
Permission to use, copy, modify and distribute this software and  
database and its documentation for any purpose and without fee or  
royalty is hereby granted, provided that you agree to comply with  
the following copyright notice and statements, including the disclaimer,  
and that the same appear on ALL copies of the software, database and  
documentation, including modifications that you make for internal  
use or for distribution.  
  
WordNet 3.0 Copyright 2006 by Princeton University.  All rights reserved.  
  
THIS SOFTWARE AND DATABASE IS PROVIDED "AS IS" AND PRINCETON  
UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR  
IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, PRINCETON  
UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT-  
ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE  
OF THE LICENSED SOFTWARE, DATABASE OR DOCUMENTATION WILL NOT  
INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR  
OTHER RIGHTS.  
  
The name of Princeton University or Princeton may not be used in  
advertising or publicity pertaining to distribution of the software  
and/or database.  Title to copyright in this software, database and  
any associated documentation shall at all times remain with  
Princeton University and LICENSEE agrees to preserve same.

SOURCE EXTRACT
source_means.csv contains the original continuous means for these twenty words. Columns follow the source mappings above. Empty social means indicate missing observations. HA1 checks all 81 possible replacements and a model restricted to six features shared by every row. The definition of emotion is an AI-authored paraphrase informed by WordNet and the APA Dictionary of Psychology (https://dictionary.apa.org/emotion).
