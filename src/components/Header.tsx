import React from 'react';
import { HardwareInfo } from '../types';
import { HardwareBadge } from './HardwareBadge';
import { Sparkles, Layers, ArrowRight } from 'lucide-react';

interface HeaderProps {
  hardware: HardwareInfo | null;
  hardwareLoading: boolean;
  selectedDevice: 'cuda' | 'cpu';
  onDeviceChange: (dev: 'cuda' | 'cpu') => void;
  onOpenExport?: () => void;
  totalScenes?: number;
}

export const Header: React.FC<HeaderProps> = ({
  hardware,
  hardwareLoading,
  selectedDevice,
  onDeviceChange,
  onOpenExport,
  totalScenes = 0
}) => {
  return (
    <header className="sticky top-0 z-40 bg-[#0e0f12]/90 backdrop-blur-md border-b border-white/10 px-4 sm:px-6 py-3 transition-all">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 shadow-lg shadow-blue-900/30">
            <span className="font-mono font-black text-white text-base">iA</span>
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
                imzy affilate
              </h1>
              <span className="px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30 text-[10px] font-semibold tracking-wide uppercase">
                Google Flow Edition
              </span>
            </div>
            <p className="text-[11px] text-gray-400">
              YouTube Copas Link ➔ 10s Consistent Scene AI Video Prompts
            </p>
          </div>
        </div>

        {/* Center / Right Controls */}
        <div className="flex items-center gap-3">
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
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-md shadow-blue-900/40 transition-all hover:scale-[1.02] active:scale-[0.98]"
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

