"""Prompt integrity tests for prompts.json.

Pure Python tests (no DB needed) that validate prompt content and routing logic.
Run with: python3.11 -m pytest tests/test_prompts.py --noconftest -v
"""

import pytest

from app.services.llm_gateway import load_prompt
from app.services.voice_turn_service import (
    get_conversation_system_prompt,
    build_conversation_prompt,
)


CONVERSATION_PROMPTS = [
    "conversation_agent",
    "conversation_agent_spanish",
    "conversation_agent_catalan",
    "conversation_agent_catalan_english",
    "grammar_conjugation_agent",
    "grammar_pronouns_agent",
    "grammar_gustar_agent",
]


class TestPromptsLoad:
    @pytest.mark.parametrize("agent_id", CONVERSATION_PROMPTS)
    def test_all_prompts_load(self, agent_id):
        """Every prompt in prompts.json loads successfully."""
        content = load_prompt(agent_id, "v1")
        assert isinstance(content, str)
        assert len(content) > 0


class TestEnglishModeRule:
    def test_conversation_agent_has_speak_in_english(self):
        """English-mode Spanish prompt must say 'Speak in English'."""
        content = load_prompt("conversation_agent", "v1")
        assert "Speak in English" in content

    def test_conversation_agent_catalan_english_has_speak_in_english(self):
        """English-mode Catalan prompt must say 'Speak in English'."""
        content = load_prompt("conversation_agent_catalan_english", "v1")
        assert "Speak in English" in content

    def test_conversation_agent_spanish_no_speak_in_english(self):
        """Spanish-mode prompt must NOT say 'Speak in English'."""
        content = load_prompt("conversation_agent_spanish", "v1")
        assert "Speak in English" not in content

    def test_conversation_agent_catalan_no_speak_in_english(self):
        """Catalan-mode prompt must NOT say 'Speak in English'."""
        content = load_prompt("conversation_agent_catalan", "v1")
        assert "Speak in English" not in content


class TestLanguageReferences:
    def test_conversation_agent_references_spanish(self):
        """The default conversation_agent should reference Spanish."""
        content = load_prompt("conversation_agent", "v1")
        assert "Spanish" in content

    def test_conversation_agent_catalan_english_references_catalan(self):
        """The catalan_english prompt should reference Catalan."""
        content = load_prompt("conversation_agent_catalan_english", "v1")
        assert "Catalan" in content

    def test_conversation_agent_catalan_english_no_spanish_target_ref(self):
        """The catalan_english prompt should not reference Spanish as the target language."""
        content = load_prompt("conversation_agent_catalan_english", "v1")
        assert "Spanish" not in content


class TestGetConversationSystemPrompt:
    def test_english_mode_default(self):
        """english mode, catalan_mode=False → conversation_agent."""
        prompt = get_conversation_system_prompt("english", catalan_mode=False)
        assert "Speak in English" in prompt
        assert "Spanish" in prompt

    def test_english_mode_catalan(self):
        """english mode, catalan_mode=True → conversation_agent_catalan_english."""
        prompt = get_conversation_system_prompt("english", catalan_mode=True)
        assert "Speak in English" in prompt
        assert "Catalan" in prompt

    def test_spanish_text_mode(self):
        """spanish_text → conversation_agent_spanish."""
        prompt = get_conversation_system_prompt("spanish_text", catalan_mode=False)
        assert "Speak in English" not in prompt
        assert "simple Spanish" in prompt

    def test_spanish_audio_mode(self):
        """spanish_audio → conversation_agent_spanish."""
        prompt = get_conversation_system_prompt("spanish_audio", catalan_mode=False)
        assert "Speak in English" not in prompt

    def test_catalan_text_mode(self):
        """catalan_text, catalan_mode=True → conversation_agent_catalan."""
        prompt = get_conversation_system_prompt("catalan_text", catalan_mode=True)
        assert "Speak in English" not in prompt
        assert "simple Catalan" in prompt

    def test_catalan_audio_mode(self):
        """catalan_audio, catalan_mode=True → conversation_agent_catalan."""
        prompt = get_conversation_system_prompt("catalan_audio", catalan_mode=True)
        assert "Speak in English" not in prompt


class TestBuildConversationPrompt:
    def test_spanish_mode_default(self):
        """Default build_conversation_prompt says 'Spanish'."""
        prompt = build_conversation_prompt(
            situation_title="Test",
            words=[],
            used_spoken_word_ids=[],
            user_transcript="hello",
            catalan_mode=False,
        )
        assert "Spanish" in prompt
        assert "Catalan" not in prompt

    def test_catalan_mode(self):
        """catalan_mode=True build_conversation_prompt says 'Catalan'."""
        prompt = build_conversation_prompt(
            situation_title="Test",
            words=[],
            used_spoken_word_ids=[],
            user_transcript="hello",
            catalan_mode=True,
        )
        assert "Catalan" in prompt
        assert "Spanish" not in prompt
