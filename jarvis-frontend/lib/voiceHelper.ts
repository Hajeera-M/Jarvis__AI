/**
 * voiceHelper.ts
 * Singleton voice selector for JARVIS TTS.
 * Caches preferred voices after first load so every
 * utterance uses exactly the same voice every time.
 */

let _cachedEnVoice: SpeechSynthesisVoice | null = null;
let _cachedHiVoice: SpeechSynthesisVoice | null = null;
let _voicesLoaded = false;

function pickEnglishVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null {
  // 1. Female Indian English
  const femaleIN = voices.find(
    (v) => v.lang.toLowerCase().startsWith("en-in") && v.name.toLowerCase().includes("female")
  );
  if (femaleIN) return femaleIN;

  // 2. Any Indian English
  const anyIN = voices.find((v) => v.lang.toLowerCase().startsWith("en-in"));
  if (anyIN) return anyIN;

  // 3. Female British English
  const femaleGB = voices.find(
    (v) => v.lang.toLowerCase().startsWith("en-gb") && v.name.toLowerCase().includes("female")
  );
  if (femaleGB) return femaleGB;

  // 4. Female US English
  const femaleUS = voices.find(
    (v) => v.lang.toLowerCase().startsWith("en-us") && v.name.toLowerCase().includes("female")
  );
  if (femaleUS) return femaleUS;

  // 5. Any Female English
  const anyFemale = voices.find(
    (v) => v.lang.toLowerCase().startsWith("en") && v.name.toLowerCase().includes("female")
  );
  if (anyFemale) return anyFemale;

  // 6. Any English fallback
  return voices.find((v) => v.lang.toLowerCase().startsWith("en")) ?? null;
}

function pickHindiVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null {
  // 1. Female Hindi-IN
  const femaleHI = voices.find(
    (v) => v.lang.toLowerCase().startsWith("hi-in") && v.name.toLowerCase().includes("female")
  );
  if (femaleHI) return femaleHI;

  // 2. Any Hindi-IN
  const anyHI = voices.find((v) => v.lang.toLowerCase().startsWith("hi"));
  if (anyHI) return anyHI;

  // 3. Fallback to Indian English if no Hindi available
  return pickEnglishVoice(voices);
}

function loadVoices(): void {
  if (_voicesLoaded) return;
  const voices = window.speechSynthesis.getVoices();
  if (voices.length === 0) return; // Not loaded yet — onvoiceschanged will retry

  _cachedEnVoice = pickEnglishVoice(voices);
  _cachedHiVoice = pickHindiVoice(voices);
  _voicesLoaded = true;
}

/**
 * Call this once at app init to warm up the voice cache.
 * Also registers the onvoiceschanged event to handle async loading.
 */
export function initVoices(): void {
  if (typeof window === "undefined") return;
  loadVoices();
  window.speechSynthesis.onvoiceschanged = () => {
    _voicesLoaded = false; // Reset so we reload with full list
    loadVoices();
  };
}

/**
 * Returns the consistently cached preferred voice for the given language.
 * @param lang - "en" | "hi" | "hinglish" | any string (defaults to English)
 */
export function getPreferredVoice(lang: string): SpeechSynthesisVoice | null {
  if (typeof window === "undefined") return null;

  // Attempt to load if not done yet
  if (!_voicesLoaded) loadVoices();

  const l = lang.toLowerCase();
  // Hinglish should use the Indian English voice for natural stress on Roman characters
  const isHinglish = l === "hinglish";
  const isHindi = l === "hi" || (l.startsWith("hi") && !isHinglish);
  
  return isHindi ? _cachedHiVoice : _cachedEnVoice;
}
