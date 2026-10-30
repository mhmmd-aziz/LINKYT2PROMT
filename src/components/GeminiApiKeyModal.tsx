import React, { useState } from 'react';
import { Key, Sparkles, Check, AlertCircle, ExternalLink, X, Shield, Cpu } from 'lucide-react';

interface GeminiApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  geminiApiKey: string;
  setGeminiApiKey: (key: string) => void;
  engineStatus: string;
}

export const GeminiApiKeyModal: React.FC<GeminiApiKeyModalProps> = ({
  isOpen,
  onClose,
  geminiApiKey,
  setGeminiApiKey,
  engineStatus
}) => {
  const [inputKey, setInputKey] = useState(geminiApiKey);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ valid: boolean; message: string } | null>(null);

  if (!isOpen) return null;

  const handleTestAndSave = async () => {
    if (!inputKey.trim()) {
      setGeminiApiKey('');
      localStorage.removeItem('imzy_gemini_api_key');
      setTestResult({ valid: false, message: 'API Key dihapus. Beralih ke Smart Local Director Engine (Free/Offline).' });
      return;
    }

    setTesting(true);
    setTestResult(null);

    try {
      const res = await fetch('/api/gemini/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ gemini_api_key: inputKey.trim() })
      });
      const data = await res.json();
      setTestResult(data);
      if (data.valid) {
        setGeminiApiKey(inputKey.trim());
        localStorage.setItem('imzy_gemini_api_key', inputKey.trim());
      }
    } catch (err: any) {
      setTestResult({ valid: false, message: `Gagal verifikasi: ${err.message}` });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="bg-[#18191e] border border-white/15 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 mb-5">
          <div className="p-2.5 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
            <Key className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              Pengaturan AI Prompt Engine
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/30 font-semibold">
                Google Flow
              </span>
            </h3>
            <p className="text-xs text-gray-400">Bagaimana prompt video dihasilkan & integrasi Gemini API</p>
          </div>
        </div>

        {/* Engine Explanation (Menjawab: "kamu menghasilkan prompt pake apa ni kok gada api") */}
        <div className="space-y-3 mb-5">
          <div className="p-3.5 rounded-xl bg-[#121316] border border-white/10 text-xs space-y-2">
            <p className="font-semibold text-gray-200 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              Dua Mesin Penghasil Prompt di imzy affilate:
            </p>
            <div className="space-y-1.5 pl-2 text-gray-300">
              <div className="flex items-start gap-2">
                <span className="text-emerald-400 font-bold">1.</span>
                <p>
                  <strong className="text-white">Google Gemini 1.5 Flash AI API:</strong> Menganalisis foto produk yang diupload secara multimodal vision + transkrip 10 detik untuk menyusun prompt video sinematik konsisten tingkat lanjut.
                </p>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-blue-400 font-bold">2.</span>
                <p>
                  <strong className="text-white">Smart Local Director Engine (Default):</strong> Berjalan 100% lokal, cepat, dan gratis tanpa butuh API key jika Anda tidak ingin memasukkan kuota API.
                </p>
              </div>
            </div>
          </div>

          {/* API Key Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-xs font-semibold text-gray-300">
                Google Gemini API Key (Opsional / Rekomendasi):
              </label>
              <a
                href="https://aistudio.google.com/app/apikey"
                target="_blank"
                rel="noreferrer"
                className="text-[11px] text-blue-400 hover:text-blue-300 flex items-center gap-1 transition-colors"
              >
                <span>Dapatkan Free API Key</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>

            <div className="relative">
              <input
                type="password"
                value={inputKey}
                onChange={(e) => setInputKey(e.target.value)}
                placeholder="Tempel Gemini API Key (AIzaSy...)"
                className="w-full px-3.5 py-2.5 rounded-xl bg-[#0f1013] border border-white/15 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-xs text-white placeholder-gray-500 outline-none font-mono"
              />
            </div>
            <p className="text-[11px] text-gray-500">
              API Key Anda disimpan aman di browser lokal Anda dan hanya digunakan untuk panggilan model Google Gemini.
            </p>
          </div>

          {testResult && (
            <div
              className={`p-3 rounded-xl border text-xs flex items-start gap-2 ${
                testResult.valid
                  ? 'bg-emerald-950/40 border-emerald-800/50 text-emerald-300'
                  : 'bg-amber-950/40 border-amber-800/50 text-amber-300'
              }`}
            >
              {testResult.valid ? <Check className="w-4 h-4 shrink-0 mt-0.5 text-emerald-400" /> : <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-amber-400" />}
              <div>
                <p className="font-semibold">{testResult.message}</p>
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-3 border-t border-white/10">
          <span className="text-[11px] text-gray-400">
            Status: <span className="font-semibold text-gray-200">{engineStatus}</span>
          </span>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3.5 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-gray-300 text-xs font-semibold"
            >
              Tutup
            </button>
            <button
              type="button"
              disabled={testing}
              onClick={handleTestAndSave}
              className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition-colors flex items-center gap-1.5"
            >
              {testing ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Memverifikasi...</span>
                </>
              ) : (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>Simpan & Aktifkan</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

