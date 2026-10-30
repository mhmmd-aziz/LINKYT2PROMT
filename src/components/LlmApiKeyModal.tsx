import React, { useState } from 'react';
import { Key, Sparkles, Check, AlertCircle, ExternalLink, X, Shield, Cpu, Bot } from 'lucide-react';

interface LlmApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  apiToken: string;
  setApiToken: (token: string) => void;
  provider: string;
  setProvider: (provider: string) => void;
  engineStatus: string;
}

export const LlmApiKeyModal: React.FC<LlmApiKeyModalProps> = ({
  isOpen,
  onClose,
  apiToken,
  setApiToken,
  provider,
  setProvider,
  engineStatus
}) => {
  const [inputToken, setInputToken] = useState(apiToken);
  const [selectedProvider, setSelectedProvider] = useState(provider || 'huggingface_deepseek');
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ valid: boolean; message: string } | null>(null);

  if (!isOpen) return null;

  const handleTestAndSave = async () => {
    if (!inputToken.trim()) {
      setApiToken('');
      localStorage.removeItem('imzy_llm_token');
      localStorage.removeItem('imzy_llm_provider');
      localStorage.removeItem('imsy_llm_token');
      localStorage.removeItem('imsy_llm_provider');
      setTestResult({ valid: false, message: 'Token dikosongkan. Beralih ke Smart Kids Director Engine (Dynamic Local Mode).' });
      return;
    }

    setTesting(true);
    setTestResult(null);

    try {
      const res = await fetch('/api/llm/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_token: inputToken.trim(),
          provider: selectedProvider
        })
      });
      const data = await res.json();
      setTestResult(data);
      if (data.valid) {
        setApiToken(inputToken.trim());
        setProvider(data.provider || selectedProvider);
        localStorage.setItem('imzy_llm_token', inputToken.trim());
        localStorage.setItem('imzy_llm_provider', data.provider || selectedProvider);
        localStorage.setItem('imsy_llm_token', inputToken.trim());
        localStorage.setItem('imsy_llm_provider', data.provider || selectedProvider);
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
          <div className="p-2.5 rounded-xl bg-amber-600/20 border border-amber-500/30 text-amber-400">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              Pengaturan AI LLM Engine
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 font-semibold">
                DeepSeek-V4.1-Flash
              </span>
            </h3>
            <p className="text-xs text-gray-400">Pilih provider LLM untuk menyusun prompt video anak yang hidup & adaptif</p>
          </div>
        </div>

        {/* Provider Switcher */}
        <div className="mb-4">
          <label className="text-xs font-semibold text-gray-300 block mb-2">Pilih Model / Provider LLM:</label>
          <div className="grid grid-cols-3 gap-2 text-xs">
            <button
              type="button"
              onClick={() => setSelectedProvider('huggingface_deepseek')}
              className={`p-2.5 rounded-xl border text-center transition-all ${
                selectedProvider === 'huggingface_deepseek'
                  ? 'bg-amber-600/30 border-amber-500 text-amber-200 font-bold'
                  : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
              }`}
            >
              <span className="block text-sm mb-0.5">🤗</span>
              <span>DeepSeek-V4.1</span>
              <span className="block text-[10px] text-amber-400/80">(Hugging Face)</span>
            </button>

            <button
              type="button"
              onClick={() => setSelectedProvider('deepseek_official')}
              className={`p-2.5 rounded-xl border text-center transition-all ${
                selectedProvider === 'deepseek_official'
                  ? 'bg-blue-600/30 border-blue-500 text-blue-200 font-bold'
                  : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
              }`}
            >
              <span className="block text-sm mb-0.5">🐳</span>
              <span>DeepSeek API</span>
              <span className="block text-[10px] text-blue-400/80">(Official API)</span>
            </button>

            <button
              type="button"
              onClick={() => setSelectedProvider('gemini')}
              className={`p-2.5 rounded-xl border text-center transition-all ${
                selectedProvider === 'gemini'
                  ? 'bg-purple-600/30 border-purple-500 text-purple-200 font-bold'
                  : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10'
              }`}
            >
              <span className="block text-sm mb-0.5">✨</span>
              <span>Gemini Vision</span>
              <span className="block text-[10px] text-purple-400/80">(Google AI)</span>
            </button>
          </div>
        </div>

        {/* Input Box */}
        <div className="space-y-3 mb-5">
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-xs font-semibold text-gray-300">
                {selectedProvider === 'huggingface_deepseek'
                  ? 'Hugging Face User Access Token (hf_...):'
                  : selectedProvider === 'deepseek_official'
                  ? 'DeepSeek Official API Key (sk-...):'
                  : 'Google Gemini API Key (AIza...):'}
              </label>

              {selectedProvider === 'huggingface_deepseek' && (
                <a
                  href="https://huggingface.co/settings/tokens"
                  target="_blank"
                  rel="noreferrer"
                  className="text-[11px] text-amber-400 hover:text-amber-300 flex items-center gap-1 transition-colors"
                >
                  <span>Ambil Free HF Token</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
              {selectedProvider === 'deepseek_official' && (
                <a
                  href="https://platform.deepseek.com/api_keys"
                  target="_blank"
                  rel="noreferrer"
                  className="text-[11px] text-blue-400 hover:text-blue-300 flex items-center gap-1 transition-colors"
                >
                  <span>DeepSeek Console</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
              {selectedProvider === 'gemini' && (
                <a
                  href="https://aistudio.google.com/app/apikey"
                  target="_blank"
                  rel="noreferrer"
                  className="text-[11px] text-purple-400 hover:text-purple-300 flex items-center gap-1 transition-colors"
                >
                  <span>Google AI Studio</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>

            <input
              type="password"
              value={inputToken}
              onChange={(e) => setInputToken(e.target.value)}
              placeholder={
                selectedProvider === 'huggingface_deepseek'
                  ? 'Tempel Hugging Face Token (hf_...)'
                  : selectedProvider === 'deepseek_official'
                  ? 'Tempel DeepSeek Key (sk-...)'
                  : 'Tempel Gemini Key (AIza...)'
              }
              className="w-full px-3.5 py-2.5 rounded-xl bg-[#0f1013] border border-white/15 focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 text-xs text-white placeholder-gray-500 outline-none font-mono"
            />
            <p className="text-[11px] text-gray-500">
              {selectedProvider === 'huggingface_deepseek'
                ? 'Model yang digunakan: deepseek-ai/DeepSeek-V4.1-Flash-1017 via Hugging Face Router.'
                : 'Token disimpan aman di browser lokal Anda.'}
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
            Engine Aktif: <span className="font-semibold text-gray-200">{engineStatus}</span>
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
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white text-xs font-semibold transition-colors flex items-center gap-1.5"
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

