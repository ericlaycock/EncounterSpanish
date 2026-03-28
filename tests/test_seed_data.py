"""Data integrity tests for seed_bank.py.

Pure Python tests (no DB needed) that validate the seed data against the spec:
- 11 sub-situations total
- 3 encounter words per encounter
- First 5 encounters per sub-situation are free
- No duplicate Spanish words within the same sub-situation
- Sequential encounter numbering within each sub-situation
- All word_ids in SITUATION_WORDS exist in ENCOUNTER_WORDS
"""

import pytest
from collections import Counter

from app.data.seed_bank import (
    ENCOUNTER_WORDS,
    SITUATIONS,
    SITUATION_WORDS,
    ANIMATION_NAMES,
    _SUB_SITUATIONS,
    HIGH_FREQUENCY_WORDS,
)

# Expected sub-situations with their encounter counts
EXPECTED_SUB_SITUATIONS = {
    ("airport", "Checking In"): 50,
    ("banking", "Banking"): 50,
    ("clothing", "Clothing Shopping"): 50,
    ("contractor", "Hiring a Contractor"): 50,
    ("core", "Core"): 47,
    ("groceries", "At the Supermarket"): 50,
    ("internet", "Setting Up WiFi"): 50,
    ("mechanic", "At the Mechanic"): 50,
    ("police", "Traffic Stop"): 50,
    ("restaurant", "Eating Out"): 50,
    ("small_talk", "Meeting a Neighbor"): 50,
}

NUM_SUB_SITUATIONS = 11
NUM_ENCOUNTERS = 547
NUM_SITUATION_WORDS = 1641


class TestSubSituationCounts:
    def test_total_sub_situations(self):
        sub_situations = set((s["animation_type"], s["title"]) for s in SITUATIONS)
        assert len(sub_situations) == NUM_SUB_SITUATIONS

    def test_each_sub_situation_has_50_encounters(self):
        counts = Counter((s["animation_type"], s["title"]) for s in SITUATIONS)
        for key, expected in EXPECTED_SUB_SITUATIONS.items():
            actual = counts.get(key, 0)
            assert actual == expected, (
                f"{key[0]}/{key[1]}: expected {expected} encounters, got {actual}"
            )

    def test_total_encounters(self):
        assert len(SITUATIONS) == NUM_ENCOUNTERS

    def test_banking_has_50_encounters(self):
        banking = [s for s in SITUATIONS if s["animation_type"] == "banking"]
        assert len(banking) == 50

    def test_restaurant_has_50_encounters(self):
        restaurant = [s for s in SITUATIONS if s["animation_type"] == "restaurant"]
        assert len(restaurant) == 50


class TestEncounterWords:
    def test_every_encounter_has_3_words(self):
        words_per_situation = Counter(sw["situation_id"] for sw in SITUATION_WORDS)
        situation_ids = {s["id"] for s in SITUATIONS}
        for sid in situation_ids:
            count = words_per_situation.get(sid, 0)
            assert count == 3, (
                f"Situation {sid}: expected 3 words, got {count}"
            )

    def test_total_situation_words(self):
        assert len(SITUATION_WORDS) == NUM_SITUATION_WORDS

    def test_total_encounter_words(self):
        total = sum(len(words) for words in ENCOUNTER_WORDS.values())
        assert total == NUM_SITUATION_WORDS

    def test_all_word_ids_exist(self):
        all_word_ids = set()
        for words in ENCOUNTER_WORDS.values():
            for w in words:
                all_word_ids.add(w["id"])
        for sw in SITUATION_WORDS:
            assert sw["word_id"] in all_word_ids, (
                f"word_id {sw['word_id']} not found in ENCOUNTER_WORDS"
            )

    def test_all_situation_ids_exist(self):
        situation_ids = {s["id"] for s in SITUATIONS}
        for sw in SITUATION_WORDS:
            assert sw["situation_id"] in situation_ids, (
                f"situation_id {sw['situation_id']} not found in SITUATIONS"
            )

    def test_word_positions_are_1_2_3(self):
        from collections import defaultdict
        by_situation = defaultdict(list)
        for sw in SITUATION_WORDS:
            by_situation[sw["situation_id"]].append(sw["position"])
        for sid, positions in by_situation.items():
            assert sorted(positions) == [1, 2, 3], (
                f"Situation {sid}: positions should be [1,2,3], got {sorted(positions)}"
            )

    def test_no_duplicate_word_ids(self):
        all_ids = []
        for words in ENCOUNTER_WORDS.values():
            for w in words:
                all_ids.append(w["id"])
        duplicates = [id for id, count in Counter(all_ids).items() if count > 1]
        assert not duplicates, f"Duplicate word IDs: {duplicates}"


class TestNoDuplicateSpanishWords:
    def test_no_duplicate_spanish_within_sub_situation(self):
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                spanish_words = [w[0] for w in sub["words"]]
                duplicates = [
                    w for w, count in Counter(spanish_words).items() if count > 1
                ]
                assert not duplicates, (
                    f"{category}/{sub['title']}: duplicate Spanish words: {duplicates}"
                )

    def test_encounter_hf_overlap_limited(self):
        """Encounter/HF overlap should be bounded (some overlap is accepted for common words)."""
        hf_spanish = {w["spanish"] for w in HIGH_FREQUENCY_WORDS}
        total_overlap = 0
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                overlap = [w[0] for w in sub["words"] if w[0] in hf_spanish]
                total_overlap += len(overlap)
        # Allow up to 250 overlapping words across all situations
        assert total_overlap < 250, (
            f"Too many encounter/HF overlaps: {total_overlap}"
        )

    def test_cross_situation_overlap_limited(self):
        """Cross-situation word overlap should be bounded."""
        situation_words = []
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                words = {w[0] for w in sub["words"]}
                situation_words.append((f"{category}/{sub['title']}", words))
        total_shared = 0
        for i in range(len(situation_words)):
            for j in range(i + 1, len(situation_words)):
                overlap = situation_words[i][1] & situation_words[j][1]
                total_shared += len(overlap)
        # Allow up to 400 shared words across all pairs
        assert total_shared < 400, (
            f"Too many cross-situation shared words: {total_shared}"
        )


class TestSequentialNumbering:
    def test_all_encounter_numbers_sequential(self):
        from collections import defaultdict
        by_sub = defaultdict(list)
        for s in SITUATIONS:
            by_sub[(s["animation_type"], s["title"])].append(s["encounter_number"])
        for key, numbers in by_sub.items():
            numbers.sort()
            expected_count = EXPECTED_SUB_SITUATIONS[key]
            expected = list(range(1, expected_count + 1))
            assert numbers == expected, (
                f"{key[0]}/{key[1]}: encounter numbers not 1-{expected_count}. "
                f"Got {numbers[:5]}...{numbers[-5:]}"
            )

    def test_banking_has_single_sub_situation(self):
        from collections import defaultdict
        by_title = defaultdict(list)
        for s in SITUATIONS:
            if s["animation_type"] == "banking":
                by_title[s["title"]].append(s["encounter_number"])
        assert len(by_title) == 1
        for title, numbers in by_title.items():
            assert sorted(numbers) == list(range(1, 51))

    def test_restaurant_has_single_sub_situation(self):
        from collections import defaultdict
        by_title = defaultdict(list)
        for s in SITUATIONS:
            if s["animation_type"] == "restaurant":
                by_title[s["title"]].append(s["encounter_number"])
        assert len(by_title) == 1
        for title, numbers in by_title.items():
            assert sorted(numbers) == list(range(1, 51))

    def test_core_has_47_encounters(self):
        core = [s for s in SITUATIONS if s["animation_type"] == "core"]
        assert len(core) == 47

    def test_unique_situation_ids(self):
        ids = [s["id"] for s in SITUATIONS]
        duplicates = [id for id, count in Counter(ids).items() if count > 1]
        assert not duplicates, f"Duplicate situation IDs: {duplicates}"


class TestFreeTier:
    def test_first_5_per_sub_situation_are_free(self):
        from collections import defaultdict
        by_sub = defaultdict(list)
        for s in SITUATIONS:
            by_sub[(s["animation_type"], s["title"])].append(s)
        for key, situations in by_sub.items():
            situations.sort(key=lambda s: s["encounter_number"])
            for i, s in enumerate(situations):
                if i < 5:
                    assert s["is_free"] is True, (
                        f"{key[0]}/{key[1]} encounter {i+1}: should be free"
                    )
                else:
                    assert s["is_free"] is False, (
                        f"{key[0]}/{key[1]} encounter {i+1}: should not be free"
                    )


class TestCompactDataIntegrity:
    def test_each_sub_has_correct_word_count(self):
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                assert len(sub["words"]) % 3 == 0, (
                    f"{category}/{sub['title']}: word count {len(sub['words'])} not divisible by 3"
                )

    def test_all_animation_types_in_animation_names(self):
        for category in _SUB_SITUATIONS:
            assert category in ANIMATION_NAMES, (
                f"Animation type '{category}' not found in ANIMATION_NAMES"
            )

    def test_word_tuples_are_triples(self):
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                for i, w in enumerate(sub["words"]):
                    assert isinstance(w, tuple) and len(w) == 3, (
                        f"{category}/{sub['title']} word {i}: expected (str, str, str) tuple, got {w}"
                    )
                    assert all(isinstance(el, str) for el in w), (
                        f"{category}/{sub['title']} word {i}: all elements must be strings"
                    )


class TestCatalanData:
    def test_internet_encounter_words_have_catalan(self):
        """Internet sub-situation (unchanged) should have Catalan translations."""
        for w in ENCOUNTER_WORDS.get("internet", []):
            assert "catalan" in w and w["catalan"], (
                f"{w['id']}: missing or empty catalan"
            )

    def test_no_catalan_equals_spanish(self):
        """For words that have Catalan, it should differ from Spanish (spot-check)."""
        same_count = 0
        total = 0
        for category, words in ENCOUNTER_WORDS.items():
            for w in words:
                if w.get("catalan"):
                    total += 1
                    if w["catalan"] == w["spanish"]:
                        same_count += 1
        if total > 0:
            ratio = same_count / total
            assert ratio < 0.30, (
                f"{same_count}/{total} ({ratio:.0%}) encounter words have catalan == spanish"
            )
