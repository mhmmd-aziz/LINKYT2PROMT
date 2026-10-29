import React, { useState } from 'react';
import { HardwareInfo } from '../types';
import { Cpu, Zap, Activity, Info, X } from 'lucide-react';

interface HardwareBadgeProps {
  hardware: HardwareInfo | null;
  loading: boolean;
  selectedDevice: 'cuda' | 'cpu';
  onDeviceChange: (dev: 'cuda' | 'cpu') => void;
}

export const HardwareBadge: React.FC<HardwareBadgeProps> = ({
  hardware,
  loading,
  selectedDevice,
  onDeviceChange
}) => {
  const [showModal, setShowModal] = useState(false);

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-gray-400 animate-pulse">
        <Activity className="w-3.5 h-3.5 animate-spin text-blue-400" />
        <span>Mendeteksi Hardware (GPU/CPU)...</span>
      </div>
    );
  }

  if (!hardware) {
    return null;
  }

  const isGpuAvailable = hardware.gpu && hardware.gpu.available;
  const isUsingGpu = selectedDevice === 'cuda' && isGpuAvailable;

  return (
    <>
      <div 
        onClick={() => setShowModal(true)}
        className="flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-[#1c1d22] border border-white/10 hover:border-blue-500/50 cursor-pointer transition-all shadow-sm group"
        title="Klik untuk detail hardware & pengaturan komputasi"
      >
        {isUsingGpu ? (
          <div className="flex items-center gap-1.5">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-xs font-medium text-emerald-300">GPU:</span>
            <span className="text-xs font-semibold text-gray-200 max-w-[190px] truncate">
              {hardware.gpu.device_name || 'NVIDIA GPU'}
            </span>
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-800/50">
              {hardware.gpu.total_vram_gb} GB VRAM
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-1.5">
            <span className="inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            <Cpu className="w-3.5 h-3.5 text-blue-400" />
            <span className="text-xs font-medium text-blue-300">CPU Mode:</span>
            <span className="text-xs font-semibold text-gray-200 max-w-[170px] truncate">
              {hardware.cpu.cpu_count_logical} Threads Active
            </span>
          </div>
        )}

        <Info className="w-3 h-3 text-gray-400 group-hover:text-blue-400 transition-colors" />
      </div>

      {/* Hardware Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-150">
          <div className="bg-[#18191e] border border-white/15 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative">
            <button
              onClick={() => setShowModal(false)}
              className="absolute top-4 right-4 p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3 mb-5">
              <div className="p-2.5 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
                <Zap className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  Auto-Detect Hardware System
                  <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    Active
                  </span>
                </h3>
                <p className="text-xs text-gray-400">Pilih akselerasi hardware untuk transkrip & pemrosesan cepat</p>
              </div>
            </div>

            {/* Device Selector */}
            <div className="mb-5 p-3.5 rounded-xl bg-[#121316] border border-white/10">
              <label className="text-xs font-medium text-gray-300 block mb-2">Mode Komputasi yang Digunakan:</label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  disabled={!isGpuAvailable}
                  onClick={() => onDeviceChange('cuda')}
                  className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${
                    selectedDevice === 'cuda'
                      ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/30'
                      : 'bg-white/5 text-gray-300 hover:bg-white/10 disabled:opacity-40 disabled:cursor-not-allowed'
                  }`}
                >
                  <Zap className="w-4 h-4 text-amber-300" />
                  GPU (NVIDIA CUDA) {isGpuAvailable ? '⚡ Cepat' : '(Tidak Ada)'}
                </button>
                <button
                  type="button"
                  onClick={() => onDeviceChange('cpu')}
                  className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${
                    selectedDevice === 'cpu'
                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/30'
                      : 'bg-white/5 text-gray-300 hover:bg-white/10'
                  }`}
                >
                  <Cpu className="w-4 h-4 text-blue-300" />
                  CPU (Fallback Mode)
                </button>
              </div>
            </div>

            {/* GPU Details */}
            <div className="space-y-3">
              <div className="p-3.5 rounded-xl bg-[#202227] border border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
                    <Zap className="w-3.5 h-3.5" />
                    Dedicated GPU (NVIDIA CUDA)
                  </span>
                  <span className="text-[11px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-mono">
                    {hardware.gpu.status}
                  </span>
                </div>
                {hardware.gpu.available ? (
                  <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs">
                    <div>
                      <span className="text-gray-400">Device:</span>{' '}
                      <span className="font-semibold text-gray-200">{hardware.gpu.device_name}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Total VRAM:</span>{' '}
                      <span className="font-semibold text-gray-200">{hardware.gpu.total_vram_gb} GB ({hardware.gpu.total_vram_mb} MB)</span>
                    </div>
                    <div>
                      <span className="text-gray-400">CUDA Version:</span>{' '}
                      <span className="font-semibold text-gray-200">{hardware.gpu.cuda_version || '12.x'}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Device Count:</span>{' '}
                      <span className="font-semibold text-gray-200">{hardware.gpu.device_count} GPU</span>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-amber-300/80">
                    Tidak ditemukan GPU NVIDIA dengan CUDA. Sistem otomatis berjalan menggunakan mode CPU.
                  </p>
                )}
              </div>

              {/* CPU Details */}
              <div className="p-3.5 rounded-xl bg-[#202227] border border-white/10">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-blue-400 flex items-center gap-1.5">
                    <Cpu className="w-3.5 h-3.5" />
                    Central Processor (CPU & RAM)
                  </span>
                  <span className="text-[11px] px-2 py-0.5 rounded bg-blue-950 text-blue-300 font-mono">
                    {hardware.cpu.cpu_count_logical} Threads
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs">
                  <div className="col-span-2">
                    <span className="text-gray-400">Processor:</span>{' '}
                    <span className="font-semibold text-gray-200">{hardware.cpu.processor}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Physical Cores:</span>{' '}
                    <span className="font-semibold text-gray-200">{hardware.cpu.cpu_count_physical} Cores</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Logical Threads:</span>{' '}
                    <span className="font-semibold text-gray-200">{hardware.cpu.cpu_count_logical} Threads</span>
                  </div>
                  <div>
                    <span className="text-gray-400">RAM Total:</span>{' '}
                    <span className="font-semibold text-gray-200">{hardware.cpu.ram_total_gb} GB</span>
                  </div>
                  <div>
                    <span className="text-gray-400">RAM Available:</span>{' '}
                    <span className="font-semibold text-gray-200">{hardware.cpu.ram_available_gb} GB</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-5 flex justify-end">
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition-colors"
              >
                Terapkan & Tutup
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

