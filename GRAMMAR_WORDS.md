# Grammar-Related Words in Database

This document lists all words in the database that have grammar implications (articles, pronouns, verbs, prepositions, conjunctions, etc.).

## Words Currently in High-Frequency List

Based on `seeds/seed_high_frequency_words.py`, the following grammar-related words are included:

### Prepositions
- **de** (rank 2) - "of, from"
- **a** (rank 4) - "to, at"
- **en** (rank 9) - "in, on"
- **por** (rank 12) - "for, by, through"
- **con** (rank 19) - "with"
- **para** (rank 20) - "for, to"
- **hasta** (rank 52) - "until, even"
- **desde** (rank 53) - "since, from"
- **entre** (rank 81) - "between, among"
- **contra** (rank 83) - "against"
- **sin** (rank 84) - "without"
- **durante** (rank 75) - "during"

### Conjunctions
- **y** (rank 8) - "and"
- **pero** (rank 25) - "but"
- **si** (rank 23) - "if"
- **porque** (rank 55) - "because"
- **mientras** (rank 92) - "while"
- **sino** (rank 95) - "but rather"
- **ni** (rank 97) - "neither, nor"
- **e** (rank 68) - "and (before i/hi)"

### Pronouns
- **yo** (rank 26) - "I"
- **ella** (rank 77) - "she"
- **usted** (rank 73) - "you (formal)"
- **mi** (rank 21) - "my"
- **tu** (rank 31) - "your (informal)"
- **su** (rank 30) - "his, her, your, their"
- **sus** (rank 79) - "their, your (plural)"
- **esto** (rank 38) - "this"
- **eso** (rank 27) - "that"
- **esta** (rank 41) - "this (feminine)"
- **ese** (rank 65) - "that (masculine)"
- **otra** (rank 70) - "other, another (feminine)"

### Question Words
- **qué** (rank 13) - "what"
- **donde** (rank 94) - "where"
- **como** (rank 35) - "like, as, how"

### Adverbs
- **muy** (rank 50) - "very"
- **más** (rank 37) - "more"
- **también** (rank 46) - "also, too"
- **bien** (rank 24) - "well, good"
- **ya** (rank 39) - "already, now"
- **ahora** (rank 66) - "now"
- **aquí** (rank 32) - "here"
- **así** (rank 60) - "like this, so"
- **después** (rank 72) - "after, later"
- **tan** (rank 93) - "so, as"
- **tanto** (rank 76) - "so much, as much"

### Indefinite/Quantifiers
- **todo** (rank 40) - "all, everything"
- **todos** (rank 59) - "all, everyone"
- **algo** (rank 62) - "something"
- **nada** (rank 89) - "nothing"
- **cada** (rank 67) - "each, every"
- **cualquier** (rank 91) - "any"
- **mismo** (rank 64) - "same"

### Verbs (Common Conjugations)
- **es** (rank 7) - "is"
- **está** (rank 22) - "is (location/state)"
- **son** (rank 45) - "they are"
- **ser** (rank 44) - "to be (permanent)"
- **estar** (rank 43) - "to be (location/state)"
- **fue** (rank 47) - "was, went"
- **era** (rank 49) - "was, used to be"
- **había** (rank 48) - "there was/were"
- **siendo** (rank 80) - "being"
- **tiene** (rank 88) - "has"
- **puede** (rank 58) - "can, may"
- **veo** (rank 61) - "I see"
- **ver** (rank 54) - "to see"
- **lleva** (rank 100) - "carries, takes"
- **partir** (rank 98) - "to leave, to start from"
- **estado** (rank 82) - "state, been"

### Phrases with Grammar
- **del** (rank 33) - "of the, from the" (de + el)
- **al** (rank 34) - "to the" (a + el)
- **porque** (rank 55) - "because"

### Negation
- **no** (rank 3) - "no, not"

### Affirmation
- **sí** (rank 29, 74) - "yes"

## Words EXCLUDED from High-Frequency List (Too Confusing Standalone)

These grammar words are intentionally excluded because they're too confusing for learners on their own. They're only included when part of phrases:

### Articles (Excluded)
- **el** - "the (masculine)"
- **la** - "the (feminine)"
- **los** - "the (masculine plural)"
- **las** - "the (feminine plural)"
- **un** - "a, an (masculine)"
- **una** - "a, an (feminine)"

### Pronouns (Excluded)
- **lo** - "it, the"
- **me** - "me"
- **te** - "you (informal)"
- **le** - "him, her, you (formal)"
- **se** - "oneself, itself"
- **nos** - "us"
- **os** - "you (plural, informal)"

## Encounter Words with Grammar Implications

From `seeds/generate_50_encounters.py`, encounter words that are grammar-related:

### Phrases (Multi-word)
- **mucho gusto** - "nice to meet you"
- **me gusta** - "I like"
- **hasta luego** - "see you later"
- **nos vemos** - "see you"

### Question Words in Encounters
- **cómo** - "how"
- **qué** - "what"
- **dónde** - "where"
- **cuándo** - "when"
- **cuál** - "which"

### Common Verbs in Encounters
- **soy** - "I am"
- **me llamo** - "my name is"
- **vivo** - "I live"
- **quiero** - "I want"
- **necesito** - "I need"
- **busco** - "I'm looking for"
- **tengo** - "I have"
- **puedo** - "I can"
- **hablo** - "I speak"
- **voy** - "I go"
- **pago** - "I pay"
- **traigo** - "I bring"
- **hago** - "I do/make"
- **uso** - "I use"
- **trabajo** - "I work"

### Time/Connector Words
- **ayer** - "yesterday"
- **hoy** - "today"
- **mañana** - "tomorrow"
- **aquí** - "here"
- **allí** - "there"
- **cerca** - "near"
- **porque** - "because"
- **entonces** - "then"
- **pero** - "but"
- **primero** - "first"
- **después** - "after"
- **ahora** - "now"
- **siempre** - "always"
- **nunca** - "never"
- **a veces** - "sometimes"
- **más** - "more"
- **menos** - "less"
- **suficiente** - "enough"
- **conmigo** - "with me"
- **contigo** - "with you"
- **solo** - "alone, only"
- **antes** - "before"
- **tarde** - "late"
- **temprano** - "early"
- **también** - "also"
- **todavía** - "still"
- **tampoco** - "neither"

### Adjectives with Grammar Implications
- **fácil** - "easy"
- **difícil** - "difficult"
- **importante** - "important"
- **diferente** - "different"
- **igual** - "same"
- **nuevo** - "new"
- **mejor** - "better, best"
- **peor** - "worse, worst"
- **listo** - "ready"

## Summary

**Total Grammar Words in High-Frequency List:** ~50-60 words
**Grammar Words Excluded (Standalone):** ~13 words (articles and pronouns)
**Grammar Words in Phrases:** ~10+ phrases

The database prioritizes teaching grammar words in context (phrases) rather than standalone, as standalone grammar words are too abstract for learners.




This document lists all words in the database that have grammar implications (articles, pronouns, verbs, prepositions, conjunctions, etc.).

## Words Currently in High-Frequency List

Based on `seeds/seed_high_frequency_words.py`, the following grammar-related words are included:

### Prepositions
- **de** (rank 2) - "of, from"
- **a** (rank 4) - "to, at"
- **en** (rank 9) - "in, on"
- **por** (rank 12) - "for, by, through"
- **con** (rank 19) - "with"
- **para** (rank 20) - "for, to"
- **hasta** (rank 52) - "until, even"
- **desde** (rank 53) - "since, from"
- **entre** (rank 81) - "between, among"
- **contra** (rank 83) - "against"
- **sin** (rank 84) - "without"
- **durante** (rank 75) - "during"

### Conjunctions
- **y** (rank 8) - "and"
- **pero** (rank 25) - "but"
- **si** (rank 23) - "if"
- **porque** (rank 55) - "because"
- **mientras** (rank 92) - "while"
- **sino** (rank 95) - "but rather"
- **ni** (rank 97) - "neither, nor"
- **e** (rank 68) - "and (before i/hi)"

### Pronouns
- **yo** (rank 26) - "I"
- **ella** (rank 77) - "she"
- **usted** (rank 73) - "you (formal)"
- **mi** (rank 21) - "my"
- **tu** (rank 31) - "your (informal)"
- **su** (rank 30) - "his, her, your, their"
- **sus** (rank 79) - "their, your (plural)"
- **esto** (rank 38) - "this"
- **eso** (rank 27) - "that"
- **esta** (rank 41) - "this (feminine)"
- **ese** (rank 65) - "that (masculine)"
- **otra** (rank 70) - "other, another (feminine)"

### Question Words
- **qué** (rank 13) - "what"
- **donde** (rank 94) - "where"
- **como** (rank 35) - "like, as, how"

### Adverbs
- **muy** (rank 50) - "very"
- **más** (rank 37) - "more"
- **también** (rank 46) - "also, too"
- **bien** (rank 24) - "well, good"
- **ya** (rank 39) - "already, now"
- **ahora** (rank 66) - "now"
- **aquí** (rank 32) - "here"
- **así** (rank 60) - "like this, so"
- **después** (rank 72) - "after, later"
- **tan** (rank 93) - "so, as"
- **tanto** (rank 76) - "so much, as much"

### Indefinite/Quantifiers
- **todo** (rank 40) - "all, everything"
- **todos** (rank 59) - "all, everyone"
- **algo** (rank 62) - "something"
- **nada** (rank 89) - "nothing"
- **cada** (rank 67) - "each, every"
- **cualquier** (rank 91) - "any"
- **mismo** (rank 64) - "same"

### Verbs (Common Conjugations)
- **es** (rank 7) - "is"
- **está** (rank 22) - "is (location/state)"
- **son** (rank 45) - "they are"
- **ser** (rank 44) - "to be (permanent)"
- **estar** (rank 43) - "to be (location/state)"
- **fue** (rank 47) - "was, went"
- **era** (rank 49) - "was, used to be"
- **había** (rank 48) - "there was/were"
- **siendo** (rank 80) - "being"
- **tiene** (rank 88) - "has"
- **puede** (rank 58) - "can, may"
- **veo** (rank 61) - "I see"
- **ver** (rank 54) - "to see"
- **lleva** (rank 100) - "carries, takes"
- **partir** (rank 98) - "to leave, to start from"
- **estado** (rank 82) - "state, been"

### Phrases with Grammar
- **del** (rank 33) - "of the, from the" (de + el)
- **al** (rank 34) - "to the" (a + el)
- **porque** (rank 55) - "because"

### Negation
- **no** (rank 3) - "no, not"

### Affirmation
- **sí** (rank 29, 74) - "yes"

## Words EXCLUDED from High-Frequency List (Too Confusing Standalone)

These grammar words are intentionally excluded because they're too confusing for learners on their own. They're only included when part of phrases:

### Articles (Excluded)
- **el** - "the (masculine)"
- **la** - "the (feminine)"
- **los** - "the (masculine plural)"
- **las** - "the (feminine plural)"
- **un** - "a, an (masculine)"
- **una** - "a, an (feminine)"

### Pronouns (Excluded)
- **lo** - "it, the"
- **me** - "me"
- **te** - "you (informal)"
- **le** - "him, her, you (formal)"
- **se** - "oneself, itself"
- **nos** - "us"
- **os** - "you (plural, informal)"

## Encounter Words with Grammar Implications

From `seeds/generate_50_encounters.py`, encounter words that are grammar-related:

### Phrases (Multi-word)
- **mucho gusto** - "nice to meet you"
- **me gusta** - "I like"
- **hasta luego** - "see you later"
- **nos vemos** - "see you"

### Question Words in Encounters
- **cómo** - "how"
- **qué** - "what"
- **dónde** - "where"
- **cuándo** - "when"
- **cuál** - "which"

### Common Verbs in Encounters
- **soy** - "I am"
- **me llamo** - "my name is"
- **vivo** - "I live"
- **quiero** - "I want"
- **necesito** - "I need"
- **busco** - "I'm looking for"
- **tengo** - "I have"
- **puedo** - "I can"
- **hablo** - "I speak"
- **voy** - "I go"
- **pago** - "I pay"
- **traigo** - "I bring"
- **hago** - "I do/make"
- **uso** - "I use"
- **trabajo** - "I work"

### Time/Connector Words
- **ayer** - "yesterday"
- **hoy** - "today"
- **mañana** - "tomorrow"
- **aquí** - "here"
- **allí** - "there"
- **cerca** - "near"
- **porque** - "because"
- **entonces** - "then"
- **pero** - "but"
- **primero** - "first"
- **después** - "after"
- **ahora** - "now"
- **siempre** - "always"
- **nunca** - "never"
- **a veces** - "sometimes"
- **más** - "more"
- **menos** - "less"
- **suficiente** - "enough"
- **conmigo** - "with me"
- **contigo** - "with you"
- **solo** - "alone, only"
- **antes** - "before"
- **tarde** - "late"
- **temprano** - "early"
- **también** - "also"
- **todavía** - "still"
- **tampoco** - "neither"

### Adjectives with Grammar Implications
- **fácil** - "easy"
- **difícil** - "difficult"
- **importante** - "important"
- **diferente** - "different"
- **igual** - "same"
- **nuevo** - "new"
- **mejor** - "better, best"
- **peor** - "worse, worst"
- **listo** - "ready"

## Summary

**Total Grammar Words in High-Frequency List:** ~50-60 words
**Grammar Words Excluded (Standalone):** ~13 words (articles and pronouns)
**Grammar Words in Phrases:** ~10+ phrases

The database prioritizes teaching grammar words in context (phrases) rather than standalone, as standalone grammar words are too abstract for learners.




This document lists all words in the database that have grammar implications (articles, pronouns, verbs, prepositions, conjunctions, etc.).

## Words Currently in High-Frequency List

Based on `seeds/seed_high_frequency_words.py`, the following grammar-related words are included:

### Prepositions
- **de** (rank 2) - "of, from"
- **a** (rank 4) - "to, at"
- **en** (rank 9) - "in, on"
- **por** (rank 12) - "for, by, through"
- **con** (rank 19) - "with"
- **para** (rank 20) - "for, to"
- **hasta** (rank 52) - "until, even"
- **desde** (rank 53) - "since, from"
- **entre** (rank 81) - "between, among"
- **contra** (rank 83) - "against"
- **sin** (rank 84) - "without"
- **durante** (rank 75) - "during"

### Conjunctions
- **y** (rank 8) - "and"
- **pero** (rank 25) - "but"
- **si** (rank 23) - "if"
- **porque** (rank 55) - "because"
- **mientras** (rank 92) - "while"
- **sino** (rank 95) - "but rather"
- **ni** (rank 97) - "neither, nor"
- **e** (rank 68) - "and (before i/hi)"

### Pronouns
- **yo** (rank 26) - "I"
- **ella** (rank 77) - "she"
- **usted** (rank 73) - "you (formal)"
- **mi** (rank 21) - "my"
- **tu** (rank 31) - "your (informal)"
- **su** (rank 30) - "his, her, your, their"
- **sus** (rank 79) - "their, your (plural)"
- **esto** (rank 38) - "this"
- **eso** (rank 27) - "that"
- **esta** (rank 41) - "this (feminine)"
- **ese** (rank 65) - "that (masculine)"
- **otra** (rank 70) - "other, another (feminine)"

### Question Words
- **qué** (rank 13) - "what"
- **donde** (rank 94) - "where"
- **como** (rank 35) - "like, as, how"

### Adverbs
- **muy** (rank 50) - "very"
- **más** (rank 37) - "more"
- **también** (rank 46) - "also, too"
- **bien** (rank 24) - "well, good"
- **ya** (rank 39) - "already, now"
- **ahora** (rank 66) - "now"
- **aquí** (rank 32) - "here"
- **así** (rank 60) - "like this, so"
- **después** (rank 72) - "after, later"
- **tan** (rank 93) - "so, as"
- **tanto** (rank 76) - "so much, as much"

### Indefinite/Quantifiers
- **todo** (rank 40) - "all, everything"
- **todos** (rank 59) - "all, everyone"
- **algo** (rank 62) - "something"
- **nada** (rank 89) - "nothing"
- **cada** (rank 67) - "each, every"
- **cualquier** (rank 91) - "any"
- **mismo** (rank 64) - "same"

### Verbs (Common Conjugations)
- **es** (rank 7) - "is"
- **está** (rank 22) - "is (location/state)"
- **son** (rank 45) - "they are"
- **ser** (rank 44) - "to be (permanent)"
- **estar** (rank 43) - "to be (location/state)"
- **fue** (rank 47) - "was, went"
- **era** (rank 49) - "was, used to be"
- **había** (rank 48) - "there was/were"
- **siendo** (rank 80) - "being"
- **tiene** (rank 88) - "has"
- **puede** (rank 58) - "can, may"
- **veo** (rank 61) - "I see"
- **ver** (rank 54) - "to see"
- **lleva** (rank 100) - "carries, takes"
- **partir** (rank 98) - "to leave, to start from"
- **estado** (rank 82) - "state, been"

### Phrases with Grammar
- **del** (rank 33) - "of the, from the" (de + el)
- **al** (rank 34) - "to the" (a + el)
- **porque** (rank 55) - "because"

### Negation
- **no** (rank 3) - "no, not"

### Affirmation
- **sí** (rank 29, 74) - "yes"

## Words EXCLUDED from High-Frequency List (Too Confusing Standalone)

These grammar words are intentionally excluded because they're too confusing for learners on their own. They're only included when part of phrases:

### Articles (Excluded)
- **el** - "the (masculine)"
- **la** - "the (feminine)"
- **los** - "the (masculine plural)"
- **las** - "the (feminine plural)"
- **un** - "a, an (masculine)"
- **una** - "a, an (feminine)"

### Pronouns (Excluded)
- **lo** - "it, the"
- **me** - "me"
- **te** - "you (informal)"
- **le** - "him, her, you (formal)"
- **se** - "oneself, itself"
- **nos** - "us"
- **os** - "you (plural, informal)"

## Encounter Words with Grammar Implications

From `seeds/generate_50_encounters.py`, encounter words that are grammar-related:

### Phrases (Multi-word)
- **mucho gusto** - "nice to meet you"
- **me gusta** - "I like"
- **hasta luego** - "see you later"
- **nos vemos** - "see you"

### Question Words in Encounters
- **cómo** - "how"
- **qué** - "what"
- **dónde** - "where"
- **cuándo** - "when"
- **cuál** - "which"

### Common Verbs in Encounters
- **soy** - "I am"
- **me llamo** - "my name is"
- **vivo** - "I live"
- **quiero** - "I want"
- **necesito** - "I need"
- **busco** - "I'm looking for"
- **tengo** - "I have"
- **puedo** - "I can"
- **hablo** - "I speak"
- **voy** - "I go"
- **pago** - "I pay"
- **traigo** - "I bring"
- **hago** - "I do/make"
- **uso** - "I use"
- **trabajo** - "I work"

### Time/Connector Words
- **ayer** - "yesterday"
- **hoy** - "today"
- **mañana** - "tomorrow"
- **aquí** - "here"
- **allí** - "there"
- **cerca** - "near"
- **porque** - "because"
- **entonces** - "then"
- **pero** - "but"
- **primero** - "first"
- **después** - "after"
- **ahora** - "now"
- **siempre** - "always"
- **nunca** - "never"
- **a veces** - "sometimes"
- **más** - "more"
- **menos** - "less"
- **suficiente** - "enough"
- **conmigo** - "with me"
- **contigo** - "with you"
- **solo** - "alone, only"
- **antes** - "before"
- **tarde** - "late"
- **temprano** - "early"
- **también** - "also"
- **todavía** - "still"
- **tampoco** - "neither"

### Adjectives with Grammar Implications
- **fácil** - "easy"
- **difícil** - "difficult"
- **importante** - "important"
- **diferente** - "different"
- **igual** - "same"
- **nuevo** - "new"
- **mejor** - "better, best"
- **peor** - "worse, worst"
- **listo** - "ready"

## Summary

**Total Grammar Words in High-Frequency List:** ~50-60 words
**Grammar Words Excluded (Standalone):** ~13 words (articles and pronouns)
**Grammar Words in Phrases:** ~10+ phrases

The database prioritizes teaching grammar words in context (phrases) rather than standalone, as standalone grammar words are too abstract for learners.



