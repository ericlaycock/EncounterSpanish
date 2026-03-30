#!/usr/bin/env python3
"""Cross-browser voice chat pipeline test.

Tests STT + Realtime API streaming across browsers and situations.
Uses a silence WAV (no real mic) to test the full API round-trip.

Usage:
    python scripts/playwright_cross_browser_test.py
    python scripts/playwright_cross_browser_test.py --browser chromium
    python scripts/playwright_cross_browser_test.py --situation bank_1
"""

import sys
import json
import argparse
from playwright.sync_api import sync_playwright

QA_URL = "https://qa.spanishforexpats.com"
API_URL = "https://sfe-backend-qa.up.railway.app"
EMAIL = "qa@a.com"
PASSWORD = "qaqaqa"

SITUATIONS = ["bank_1", "rest_1", "core_1", "pol_1"]
BROWSERS = ["chromium", "firefox"]

# JavaScript that runs in the browser to test the full pipeline
TEST_JS = """
async (situationId) => {
    const API = '__API_URL__';
    const token = localStorage.getItem('authToken');
    const results = { situation: situationId, errors: [] };

    try {
        // 1. Start situation + create conversation
        const startRes = await fetch(`${API}/v1/situations/${situationId}/start`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
        });
        if (!startRes.ok) throw new Error(`Start situation failed: ${startRes.status}`);

        const convRes = await fetch(`${API}/v1/conversations`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ situation_id: situationId, mode: 'voice' }),
        });
        if (!convRes.ok) throw new Error(`Create conv failed: ${convRes.status}`);
        const conv = await convRes.json();
        results.conversation_id = conv.conversation_id;

        // 2. Create silence WAV (2 seconds, 16kHz mono)
        const sampleRate = 16000, duration = 2, numSamples = sampleRate * duration;
        const buffer = new ArrayBuffer(44 + numSamples * 2);
        const view = new DataView(buffer);
        const writeStr = (off, s) => { for (let i = 0; i < s.length; i++) view.setUint8(off + i, s.charCodeAt(i)); };
        writeStr(0, 'RIFF');
        view.setUint32(4, 36 + numSamples * 2, true);
        writeStr(8, 'WAVE'); writeStr(12, 'fmt ');
        view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, 1, true);
        view.setUint32(24, sampleRate, true); view.setUint32(28, sampleRate * 2, true);
        view.setUint16(32, 2, true); view.setUint16(34, 16, true);
        writeStr(36, 'data'); view.setUint32(40, numSamples * 2, true);
        const wavBlob = new Blob([buffer], { type: 'audio/wav' });

        // 3. STT
        const fd = new FormData();
        fd.append('audio', wavBlob, 'recording.wav');
        const sttStart = performance.now();
        const sttRes = await fetch(`${API}/v1/conversations/${conv.conversation_id}/voice-turn`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: fd,
        });
        if (!sttRes.ok) throw new Error(`STT failed: ${sttRes.status}`);
        const sttData = await sttRes.json();
        results.stt_ms = Math.round(performance.now() - sttStart);
        results.transcript = sttData.user_transcript;

        // 4. Respond (streaming NDJSON with audio)
        const respondStart = performance.now();
        const respondRes = await fetch(`${API}/v1/conversations/${conv.conversation_id}/voice-turn/respond`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_transcript: sttData.user_transcript, messages_json: null }),
        });
        if (!respondRes.ok) throw new Error(`Respond failed: ${respondRes.status}`);

        let firstAudioMs = null, textMs = null, doneMs = null;
        let audioChunkCount = 0, totalAudioBytes = 0;
        let assistantText = '', conversationComplete = false;
        let audioPlayOk = false;

        const reader = respondRes.body.getReader();
        const decoder = new TextDecoder();
        let streamBuf = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            streamBuf += decoder.decode(value, { stream: true });
            const lines = streamBuf.split('\\n');
            streamBuf = lines.pop();

            for (const line of lines) {
                if (!line.trim()) continue;
                let event;
                try { event = JSON.parse(line); } catch { continue; }

                if (event.type === 'audio' && event.data) {
                    audioChunkCount++;
                    const raw = Uint8Array.from(atob(event.data), c => c.charCodeAt(0));
                    totalAudioBytes += raw.length;
                    if (firstAudioMs === null) {
                        firstAudioMs = Math.round(performance.now() - respondStart);
                    }

                    // Test AudioContext playback (first chunk only)
                    if (audioChunkCount === 1) {
                        try {
                            const ctx = new AudioContext({ sampleRate: 24000 });
                            const pcm16 = new Int16Array(raw.buffer);
                            const float32 = new Float32Array(pcm16.length);
                            for (let i = 0; i < pcm16.length; i++) float32[i] = pcm16[i] / 32768;
                            const buf = ctx.createBuffer(1, float32.length, 24000);
                            buf.getChannelData(0).set(float32);
                            const src = ctx.createBufferSource();
                            src.buffer = buf;
                            src.connect(ctx.destination);
                            src.start();
                            audioPlayOk = true;
                            await ctx.close();
                        } catch (e) {
                            results.errors.push('AudioContext: ' + e.message);
                        }
                    }

                } else if (event.type === 'text') {
                    assistantText = event.text || '';
                    textMs = Math.round(performance.now() - respondStart);

                } else if (event.type === 'done') {
                    conversationComplete = event.conversation_complete || false;
                    doneMs = Math.round(performance.now() - respondStart);

                } else if (event.type === 'error') {
                    results.errors.push('Stream error: ' + (event.message || ''));
                }
            }
        }

        results.first_audio_ms = firstAudioMs;
        results.text_ms = textMs;
        results.done_ms = doneMs;
        results.audio_chunks = audioChunkCount;
        results.audio_bytes = totalAudioBytes;
        results.assistant_text = assistantText;
        results.audio_play_ok = audioPlayOk;
        results.conversation_complete = conversationComplete;

    } catch (e) {
        results.errors.push(e.message);
    }

    return results;
}
""".replace("__API_URL__", API_URL)


def get_auth_token():
    """Get JWT token from QA backend."""
    import urllib.request
    data = json.dumps({"email": EMAIL, "password": PASSWORD}).encode()
    req = urllib.request.Request(
        f"{API_URL}/v1/auth/login",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    res = urllib.request.urlopen(req)
    return json.loads(res.read())["access_token"]


def run_tests(browser_name: str, situations: list, playwright):
    """Run tests for one browser across all situations."""
    browser_type = getattr(playwright, browser_name)
    browser = browser_type.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Login via token injection
    page.goto(f"{QA_URL}/login")
    token = get_auth_token()
    page.evaluate(f"""() => {{
        localStorage.setItem('authToken', '{token}');
        localStorage.setItem('isAdmin', 'true');
        localStorage.setItem('userEmail', '{EMAIL}');
    }}""")

    results = []
    for sit in situations:
        print(f"    {sit}...", end="", flush=True)

        # Navigate to voice chat to establish page context
        page.goto(f"{QA_URL}/situation/{sit}/voice-chat?phase=2")
        page.wait_for_timeout(2000)  # Wait for page load

        # Run the test
        try:
            result = page.evaluate(TEST_JS, sit)
            results.append(result)
            stt = result.get("stt_ms", "ERR")
            fa = result.get("first_audio_ms", "ERR")
            txt = result.get("text_ms", "ERR")
            done = result.get("done_ms", "ERR")
            audio_ok = "✓" if result.get("audio_play_ok") else "✗"
            errors = result.get("errors", [])

            if errors:
                print(f" ERRORS: {errors}")
            else:
                print(f" STT={stt}ms 1stAudio={fa}ms Text={txt}ms Total={done}ms Audio={audio_ok}")
        except Exception as e:
            print(f" EXCEPTION: {e}")
            results.append({"situation": sit, "errors": [str(e)]})

    browser.close()
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", choices=BROWSERS, help="Test only this browser")
    parser.add_argument("--situation", help="Test only this situation (e.g., bank_1)")
    args = parser.parse_args()

    browsers = [args.browser] if args.browser else BROWSERS
    situations = [args.situation] if args.situation else SITUATIONS

    all_results = {}

    with sync_playwright() as p:
        for browser_name in browsers:
            print(f"\n{'='*60}")
            print(f"  {browser_name.upper()}")
            print(f"{'='*60}")
            all_results[browser_name] = run_tests(browser_name, situations, p)

    # Summary table
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")

    for browser_name, results in all_results.items():
        print(f"\n=== {browser_name.upper()} ===")
        print(f"{'Situation':<12} | {'STT':>6} | {'1st Audio':>9} | {'Text':>6} | {'Total':>6} | {'Audio':>5} | {'Errors'}")
        print(f"{'-'*12}-+-{'-'*6}-+-{'-'*9}-+-{'-'*6}-+-{'-'*6}-+-{'-'*5}-+-{'-'*20}")
        for r in results:
            sit = r.get("situation", "?")
            stt = f"{r.get('stt_ms', 0)}ms" if r.get("stt_ms") else "ERR"
            fa = f"{r.get('first_audio_ms', 0)}ms" if r.get("first_audio_ms") else "ERR"
            txt = f"{r.get('text_ms', 0)}ms" if r.get("text_ms") else "ERR"
            done = f"{r.get('done_ms', 0)}ms" if r.get("done_ms") else "ERR"
            audio = "✓" if r.get("audio_play_ok") else "✗"
            errors = "; ".join(r.get("errors", []))[:40] or "none"
            print(f"{sit:<12} | {stt:>6} | {fa:>9} | {txt:>6} | {done:>6} | {audio:>5} | {errors}")


if __name__ == "__main__":
    main()
