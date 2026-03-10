"""Data integrity tests for seed_bank.py.

Pure Python tests (no DB needed) that validate the seed data against the spec:
- 14 sub-situations total
- 50 encounters per sub-situation = 700 total
- 3 encounter words per encounter = 2,100 total
- First 5 encounters per sub-situation are free
- No duplicate Spanish words within the same sub-situation
- Sequential series_number within each sub-situation
- All word_ids in SITUATION_WORDS exist in ENCOUNTER_WORDS
"""

import pytest
from collections import Counter

from app.data.seed_bank import (
    ENCOUNTER_WORDS,
    SITUATIONS,
    SITUATION_WORDS,
    CATEGORY_NAMES,
    _SUB_SITUATIONS,
)

# Expected sub-situations with their encounter counts
EXPECTED_SUB_SITUATIONS = {
    ("airport", "Checking In"): 50,
    ("banking", "Opening a Bank Account"): 50,
    ("banking", "Wire Transfer"): 50,
    ("banking", "Currency Exchange"): 50,
    ("clothing", "Finding the Right Size"): 50,
    ("contractor", "Hiring a Plumber"): 50,
    ("groceries", "At the Supermarket"): 50,
    ("internet", "Setting Up WiFi"): 50,
    ("mechanic", "Oil Change"): 50,
    ("police", "Traffic Stop"): 50,
    ("restaurant", "Ordering Food"): 50,
    ("restaurant", "Making a Reservation"): 50,
    ("restaurant", "Asking for the Bill"): 50,
    ("small_talk", "Meeting a Neighbor"): 50,
}


class TestSubSituationCounts:
    def test_total_sub_situations(self):
        """There should be exactly 14 sub-situations."""
        sub_situations = set((s["category"], s["title"]) for s in SITUATIONS)
        assert len(sub_situations) == 14

    def test_each_sub_situation_has_50_encounters(self):
        """Every sub-situation must have exactly 50 encounters."""
        counts = Counter((s["category"], s["title"]) for s in SITUATIONS)
        for key, expected in EXPECTED_SUB_SITUATIONS.items():
            actual = counts.get(key, 0)
            assert actual == expected, (
                f"{key[0]}/{key[1]}: expected {expected} encounters, got {actual}"
            )

    def test_total_encounters(self):
        """Total encounters should be 700 (14 × 50)."""
        assert len(SITUATIONS) == 700

    def test_banking_has_150_encounters(self):
        """Banking has 3 sub-situations × 50 = 150 encounters."""
        banking = [s for s in SITUATIONS if s["category"] == "banking"]
        assert len(banking) == 150

    def test_restaurant_has_150_encounters(self):
        """Restaurant has 3 sub-situations × 50 = 150 encounters."""
        restaurant = [s for s in SITUATIONS if s["category"] == "restaurant"]
        assert len(restaurant) == 150


class TestEncounterWords:
    def test_every_encounter_has_3_words(self):
        """Every encounter (situation) must have exactly 3 words linked."""
        words_per_situation = Counter(sw["situation_id"] for sw in SITUATION_WORDS)
        situation_ids = {s["id"] for s in SITUATIONS}
        for sid in situation_ids:
            count = words_per_situation.get(sid, 0)
            assert count == 3, (
                f"Situation {sid}: expected 3 words, got {count}"
            )

    def test_total_situation_words(self):
        """Total situation-word links should be 2,100 (700 × 3)."""
        assert len(SITUATION_WORDS) == 2100

    def test_total_encounter_words(self):
        """Total encounter words should be 2,100."""
        total = sum(len(words) for words in ENCOUNTER_WORDS.values())
        assert total == 2100

    def test_all_word_ids_exist(self):
        """Every word_id in SITUATION_WORDS must exist in ENCOUNTER_WORDS."""
        all_word_ids = set()
        for words in ENCOUNTER_WORDS.values():
            for w in words:
                all_word_ids.add(w["id"])
        for sw in SITUATION_WORDS:
            assert sw["word_id"] in all_word_ids, (
                f"word_id {sw['word_id']} not found in ENCOUNTER_WORDS"
            )

    def test_all_situation_ids_exist(self):
        """Every situation_id in SITUATION_WORDS must exist in SITUATIONS."""
        situation_ids = {s["id"] for s in SITUATIONS}
        for sw in SITUATION_WORDS:
            assert sw["situation_id"] in situation_ids, (
                f"situation_id {sw['situation_id']} not found in SITUATIONS"
            )

    def test_word_positions_are_1_2_3(self):
        """Each encounter's words should have positions 1, 2, 3."""
        from collections import defaultdict
        by_situation = defaultdict(list)
        for sw in SITUATION_WORDS:
            by_situation[sw["situation_id"]].append(sw["position"])
        for sid, positions in by_situation.items():
            assert sorted(positions) == [1, 2, 3], (
                f"Situation {sid}: positions should be [1,2,3], got {sorted(positions)}"
            )

    def test_no_duplicate_word_ids(self):
        """No duplicate word IDs across all encounter words."""
        all_ids = []
        for words in ENCOUNTER_WORDS.values():
            for w in words:
                all_ids.append(w["id"])
        duplicates = [id for id, count in Counter(all_ids).items() if count > 1]
        assert not duplicates, f"Duplicate word IDs: {duplicates}"


class TestNoDuplicateSpanishWords:
    def test_no_duplicate_spanish_within_sub_situation(self):
        """No duplicate Spanish words within the same sub-situation."""
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                spanish_words = [w[0] for w in sub["words"]]
                duplicates = [
                    w for w, count in Counter(spanish_words).items() if count > 1
                ]
                assert not duplicates, (
                    f"{category}/{sub['title']}: duplicate Spanish words: {duplicates}"
                )


class TestSequentialNumbering:
    def test_sequential_series_numbers(self):
        """Series numbers should be sequential within each sub-situation."""
        from collections import defaultdict
        by_sub = defaultdict(list)
        for s in SITUATIONS:
            by_sub[(s["category"], s["title"])].append(s["series_number"])
        for key, numbers in by_sub.items():
            numbers.sort()
            expected_start = numbers[0]
            expected = list(range(expected_start, expected_start + 50))
            assert numbers == expected, (
                f"{key[0]}/{key[1]}: series numbers not sequential. "
                f"Expected {expected[:5]}...{expected[-5:]}, got {numbers[:5]}...{numbers[-5:]}"
            )

    def test_banking_numbering(self):
        """Banking: 1-50 = Opening, 51-100 = Wire, 101-150 = Exchange."""
        banking = sorted(
            [(s["title"], s["series_number"]) for s in SITUATIONS if s["category"] == "banking"],
            key=lambda x: x[1],
        )
        for title, num in banking:
            if 1 <= num <= 50:
                assert title == "Opening a Bank Account", f"banking_{num} should be Opening, got {title}"
            elif 51 <= num <= 100:
                assert title == "Wire Transfer", f"banking_{num} should be Wire, got {title}"
            elif 101 <= num <= 150:
                assert title == "Currency Exchange", f"banking_{num} should be Exchange, got {title}"

    def test_restaurant_numbering(self):
        """Restaurant: 1-50 = Ordering, 51-100 = Reservation, 101-150 = Bill."""
        restaurant = sorted(
            [(s["title"], s["series_number"]) for s in SITUATIONS if s["category"] == "restaurant"],
            key=lambda x: x[1],
        )
        for title, num in restaurant:
            if 1 <= num <= 50:
                assert title == "Ordering Food", f"restaurant_{num} should be Ordering, got {title}"
            elif 51 <= num <= 100:
                assert title == "Making a Reservation", f"restaurant_{num} should be Reservation, got {title}"
            elif 101 <= num <= 150:
                assert title == "Asking for the Bill", f"restaurant_{num} should be Bill, got {title}"

    def test_unique_situation_ids(self):
        """All situation IDs should be unique."""
        ids = [s["id"] for s in SITUATIONS]
        duplicates = [id for id, count in Counter(ids).items() if count > 1]
        assert not duplicates, f"Duplicate situation IDs: {duplicates}"


class TestFreeTier:
    def test_first_5_per_sub_situation_are_free(self):
        """First 5 encounters of each sub-situation should be is_free=True."""
        from collections import defaultdict
        by_sub = defaultdict(list)
        for s in SITUATIONS:
            by_sub[(s["category"], s["title"])].append(s)
        for key, situations in by_sub.items():
            situations.sort(key=lambda s: s["series_number"])
            for i, s in enumerate(situations):
                if i < 5:
                    assert s["is_free"] is True, (
                        f"{key[0]}/{key[1]} encounter {i+1} (series {s['series_number']}): "
                        f"should be free"
                    )
                else:
                    assert s["is_free"] is False, (
                        f"{key[0]}/{key[1]} encounter {i+1} (series {s['series_number']}): "
                        f"should not be free"
                    )


class TestCompactDataIntegrity:
    def test_each_sub_has_150_word_tuples(self):
        """Each sub-situation should have exactly 150 (spanish, english) tuples."""
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                assert len(sub["words"]) == 150, (
                    f"{category}/{sub['title']}: expected 150 words, got {len(sub['words'])}"
                )

    def test_all_categories_in_category_names(self):
        """All categories used in sub-situations should exist in CATEGORY_NAMES."""
        for category in _SUB_SITUATIONS:
            assert category in CATEGORY_NAMES, (
                f"Category '{category}' not found in CATEGORY_NAMES"
            )

    def test_word_tuples_are_pairs(self):
        """Every word entry should be a (spanish, english) tuple of 2 strings."""
        for category, sub_list in _SUB_SITUATIONS.items():
            for sub in sub_list:
                for i, w in enumerate(sub["words"]):
                    assert isinstance(w, tuple) and len(w) == 2, (
                        f"{category}/{sub['title']} word {i}: expected (str, str) tuple, got {w}"
                    )
                    assert isinstance(w[0], str) and isinstance(w[1], str), (
                        f"{category}/{sub['title']} word {i}: both elements must be strings"
                    )
