/**
 * voiceHelper.ts
 * Singleton voice selector for JARVIS TTS.
 * Caches preferred voices after first load so every
 * utterance uses exactly the same voice every time.
 */

let _cachedEnVoice: SpeechSynthesisVoice | null = null;
let _cachedHiVoice: SpeechSynthesisVoice | null = null;
let _voicesLoaded = false;

const NEURAL_HINTS = ["neural", "natural", "google", "online", "aria", "guy", "male", "wavenet", "david", "mark"];

function pickEnglishVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null {
  const vList = voices.filter(v => v.lang.toLowerCase().startsWith("en"));
  
  // 1. High-Fidelity Neural/Natural (Male Preferred)
  const neuralMale = vList.find(v => 
    NEURAL_HINTS.some(h => v.name.toLowerCase().includes(h)) && 
    (v.name.toLowerCase().includes("male") || v.name.toLowerCase().includes("guy") || v.name.toLowerCase().includes("david") || v.name.toLowerCase().includes("mark"))
  );
  if (neuralMale) return neuralMale;

  // 2. Any High-Fidelity Neural
  const neuralAny = vList.find(v => NEURAL_HINTS.some(h => v.name.toLowerCase().includes(h)));
  if (neuralAny) return neuralAny;

  // 3. Regional Male (Indian English)
  const maleIN = vList.find(
    (v) => v.lang.toLowerCase().startsWith("en-in") && (v.name.toLowerCase().includes("male") || v.name.toLowerCase().includes("guy"))
  );
  if (maleIN) return maleIN;

  // 4. Any Indian English
  const anyIN = vList.find((v) => v.lang.toLowerCase().startsWith("en-in"));
  if (anyIN) return anyIN;

  // 5. Male British/US fallback
  const anyMale = vList.find((v) => v.name.toLowerCase().includes("male") || v.name.toLowerCase().includes("guy"));
  if (anyMale) return anyMale;

  // 6. Generic Fallback
  return vList[0] || null;
}

function pickHindiVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | null {
  const vList = voices.filter(v => v.lang.toLowerCase().startsWith("hi"));
  
  // 1. High-Fidelity Neural (Google/Microsoft Premium)
  const premium = vList.find(v => 
    v.name.includes("Google हिन्दी") || 
    v.name.includes("Heera") || 
    v.name.includes("Swara") ||
    v.name.toLowerCase().includes("neural") ||
    v.name.toLowerCase().includes("online")
  );
  if (premium) return premium;

  // 2. Any Female Hindi-IN
  const femaleHI = vList.find(v => v.name.toLowerCase().includes("female"));
  if (femaleHI) return femaleHI;

  // 3. Any Hindi-IN
  if (vList.length > 0) return vList[0];

  // 4. Fallback to Indian English if no Hindi available
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
