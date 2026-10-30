import React from 'react';
import { HardwareInfo } from '../types';
import { HardwareBadge } from './HardwareBadge';
import { Layers, ArrowRight, Key, Car, Bot } from 'lucide-react';

interface HeaderProps {
  hardware: HardwareInfo | null;
  hardwareLoading: boolean;
  selectedDevice: 'cuda' | 'cpu';
  onDeviceChange: (dev: 'cuda' | 'cpu') => void;
  apiToken: string;
  provider: string;
  onOpenApiKeyModal: () => void;
  onOpenExport?: () => void;
  totalScenes?: number;
}

export const Header: React.FC<HeaderProps> = ({
  hardware,
  hardwareLoading,
  selectedDevice,
  onDeviceChange,
  apiToken,
  provider,
  onOpenApiKeyModal,
  onOpenExport,
  totalScenes = 0
}) => {
  const isTokenActive = Boolean(apiToken && apiToken.trim());

  const getEnginePillText = () => {
    if (!isTokenActive) return 'AI: Kids Director ⚡';
    if (provider === 'huggingface_deepseek') return 'AI: DeepSeek-V4.1 🤗';
    if (provider === 'deepseek_official') return 'AI: DeepSeek 🐳';
    if (provider === 'gemini') return 'AI: Gemini 1.5 ✨';
    return 'AI: DeepSeek-V4.1 🟢';
  };

  return (
    <header className="sticky top-0 z-40 bg-[#0e0f12]/90 backdrop-blur-md border-b border-white/10 px-4 sm:px-6 py-3 transition-all">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 via-orange-600 to-red-600 shadow-lg shadow-amber-900/30">
            <Car className="w-5 h-5 text-white animate-pulse" />
            <div className="absolute -bottom-1 -right-1 flex gap-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#4285F4]"></span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#EA4335]"></span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#FBBC05]"></span>
              <span className="w-1.5 h-1.5 rounded-full bg-[#34A853]"></span>
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
                imzy tools yt
              </h1>
              <span className="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-semibold tracking-wide uppercase">
                DeepSeek-V4.1 Engine
              </span>
            </div>
            <p className="text-[11px] text-gray-400">
              Kids Video 60 Scene Remake • Fluid Storyboard Prompts & Sound Effects
            </p>
          </div>
        </div>

        {/* Center / Right Controls */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* AI Engine & API Key Pill */}
          <button
            type="button"
            onClick={onOpenApiKeyModal}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-xs font-medium transition-all ${
              isTokenActive
                ? 'bg-amber-950/40 border-amber-500/40 text-amber-300 hover:border-amber-400 shadow-sm'
                : 'bg-white/5 border-white/10 text-gray-300 hover:border-white/20'
            }`}
            title="Klik untuk memilih model DeepSeek V4.1 Flash / Hugging Face / DeepSeek API"
          >
            <Bot className="w-3.5 h-3.5 text-amber-400" />
            <span>{getEnginePillText()}</span>
          </button>

          {/* Hardware Auto-Detect Pill */}
          <HardwareBadge
            hardware={hardware}
            loading={hardwareLoading}
            selectedDevice={selectedDevice}
            onDeviceChange={onDeviceChange}
          />

          {totalScenes > 0 && onOpenExport && (
            <button
              onClick={onOpenExport}
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white text-xs font-semibold shadow-md shadow-amber-900/40 transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              <Layers className="w-3.5 h-3.5" />
              <span>Export {totalScenes} Scenes</span>
              <ArrowRight className="w-3 h-3 ml-0.5" />
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
