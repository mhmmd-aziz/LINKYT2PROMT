import React from 'react';
import { SceneAnchors } from '../types';
import { Layers, ShieldCheck, Box, Sliders, Sparkles, Globe2, Camera, Eye, AlertTriangle, Car, Music } from 'lucide-react';

interface ConsistencyNodeProps {
  duration: number;
  sceneDuration: number;
  setSceneDuration: (sec: number) => void;
  language: string;
  setLanguage: (lang: string) => void;
  anchors: SceneAnchors;
  setAnchors: React.Dispatch<React.SetStateAction<SceneAnchors>>;
  onGenerate: () => void;
  generating: boolean;
  disabled: boolean;
  hasUploadedImage: boolean;
}

export const ConsistencyNode: React.FC<ConsistencyNodeProps> = ({
  duration,
  sceneDuration,
  setSceneDuration,
  language,
  setLanguage,
  anchors,
  setAnchors,
  onGenerate,
  generating,
  disabled,
  hasUploadedImage
}) => {
  const rawScenes = Math.max(1, Math.ceil(duration / (sceneDuration || 10)));
  const totalCalculatedScenes = Math.min(20, rawScenes);
  const isCapped = rawScenes > 20;

  return (
    <div className="relative rounded-2xl bg-[#16171c] border border-white/10 p-5 sm:p-6 shadow-xl transition-all">
      {/* Node Header */}
      <div className="flex flex-wrap items-center justify-between pb-4 mb-5 border-b border-white/10 gap-2">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-emerald-600/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-gray-400 border border-white/10">
                NODE 03
              </span>
              <h2 className="text-base font-bold text-white">Konsistensi Mobil Mainan & Karakter (Versi 20 Scene)</h2>
            </div>
            <p className="text-xs text-gray-400">
              Satu scene 10 detik penuh, mobil dan tokoh anak konsisten 100% dari scene 1 hingga scene 20
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[11px] font-mono px-3 py-1 rounded-full bg-blue-500/15 border border-blue-500/30 text-blue-300 font-semibold">
            {totalCalculatedScenes} Scene {isCapped ? '(Max 20 Capped)' : ''} ({sceneDuration}s / scene)
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {/* Max 20 Scene Notice if video is longer */}
        {isCapped && (
          <div className="p-3 rounded-xl bg-amber-950/30 border border-amber-800/40 text-amber-300 text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400" />
            <p>
              Video berdurasi {Math.floor(duration/60)}m {Math.floor(duration%60)}s ({rawScenes} segmen). Sistem menyusun cerita menjadi tepat <strong>20 scene prompt (alur video anak bersambung)</strong> agar cerita fokus, padat, dan konsisten.
            </p>
          </div>
        )}

        {/* Scene Duration & Language Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded-xl bg-[#0f1013] border border-white/5">
          <div>
            <label className="text-xs font-semibold text-gray-300 flex items-center gap-1.5 mb-1.5">
              <Sliders className="w-3.5 h-3.5 text-blue-400" />
              Durasi Per Scene (Standar AI Video Anak):
            </label>
            <div className="flex items-center gap-2">
              <div className="px-3 py-2 rounded-lg bg-[#1c1d22] border border-white/15 text-sm font-bold text-emerald-400 font-mono flex items-center gap-2">
                <span>⏱️ {sceneDuration} Detik Penuh</span>
                <span className="text-[10px] text-gray-400 font-normal">(Rekomendasi Utama)</span>
              </div>
              <div className="flex gap-1">
                {[5, 10, 15].map((sec) => (
                  <button
                    key={sec}
                    type="button"
                    onClick={() => setSceneDuration(sec)}
                    className={`px-2.5 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                      sceneDuration === sec
                        ? 'bg-blue-600 text-white'
                        : 'bg-white/5 text-gray-400 hover:bg-white/10'
                    }`}
                  >
                    {sec}s
                  </button>
                ))}
              </div>
            </div>
            <p className="text-[11px] text-gray-500 mt-1">
              Menghasilkan hingga 60 scene prompt ({totalCalculatedScenes} scene aktif, {Math.round(totalCalculatedScenes * sceneDuration)} detik video anak).
            </p>
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-300 flex items-center gap-1.5 mb-1.5">
              <Globe2 className="w-3.5 h-3.5 text-blue-400" />
              Bahasa Narasi & Efek Suara:
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setLanguage('id')}
                className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg text-xs font-medium transition-all ${
                  language === 'id'
                    ? 'bg-blue-600 text-white font-semibold'
                    : 'bg-[#1c1d22] border border-white/10 text-gray-400 hover:text-white'
                }`}
              >
                <span>🇮🇩 Bahasa Indonesia</span>
              </button>
              <button
                type="button"
                onClick={() => setLanguage('en')}
                className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg text-xs font-medium transition-all ${
                  language === 'en'
                    ? 'bg-blue-600 text-white font-semibold'
                    : 'bg-[#1c1d22] border border-white/10 text-gray-400 hover:text-white'
                }`}
              >
                <span>🇬🇧 English</span>
              </button>
            </div>
            <p className="text-[11px] text-gray-500 mt-1">
              Dialog, sound effect, dan prompt diselaraskan dengan bahasa asli video YouTube.
            </p>
          </div>
        </div>

        {/* Master Anchors for Toy Car & Character Continuity */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-gray-400 flex items-center gap-1.5">
              <Car className="w-3.5 h-3.5 text-amber-400" />
              Master Continuity Anchors (Kunci Konsistensi Mobil & Tokoh Anak):
            </span>
            <span className="text-[11px] text-emerald-400 font-medium flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5" />
              {hasUploadedImage ? 'Terkunci Sesuai Foto Mainan' : 'Terkunci Otomatis di Setiap Scene'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {/* Primary Toy Car */}
            <div className="p-3 rounded-xl bg-[#0f1013] border border-white/10 focus-within:border-amber-500/50 transition-all">
              <label className="font-semibold text-amber-300 block mb-1 flex items-center gap-1">
                <span>🏎️ Mobil Mainan Utama (Model, Warna, Ban):</span>
              </label>
              <textarea
                rows={2}
                value={anchors.product}
                onChange={(e) => setAnchors({ ...anchors, product: e.target.value })}
                placeholder="Contoh: Mobil Monster Truck merah bergaris kuning neon, roda hitam bergerigi besar, bodi 3D Pixar..."
                className="w-full bg-transparent text-gray-200 placeholder-gray-600 text-xs outline-none resize-none"
              />
            </div>

            {/* Child Character / Driver */}
            <div className="p-3 rounded-xl bg-[#0f1013] border border-white/10 focus-within:border-blue-500/50 transition-all">
              <label className="font-semibold text-blue-300 block mb-1 flex items-center gap-1">
                <span>👦 Tokoh Karakter Anak / Sopir Ceria:</span>
              </label>
              <textarea
                rows={2}
                value={anchors.subject}
                onChange={(e) => setAnchors({ ...anchors, subject: e.target.value })}
                placeholder="Contoh: Anak laki-laki usia 4 tahun, kaos garis biru-oranye ceria, wajah riang tersenyum gembira..."
                className="w-full bg-transparent text-gray-200 placeholder-gray-600 text-xs outline-none resize-none"
              />
            </div>

            {/* Play Arena / Track */}
            <div className="p-3 rounded-xl bg-[#0f1013] border border-white/10 focus-within:border-purple-500/50 transition-all">
              <label className="font-semibold text-purple-300 block mb-1 flex items-center gap-1">
                <span>🎪 Arena Bermain & Lintasan Balap:</span>
              </label>
              <textarea
                rows={2}
                value={anchors.setting}
                onChange={(e) => setAnchors({ ...anchors, setting: e.target.value })}
                placeholder="Contoh: Kamar bermain anak yang cerah dengan lintasan balap melingkar oranye, jembatan kayu, dan rintangan balok..."
                className="w-full bg-transparent text-gray-200 placeholder-gray-600 text-xs outline-none resize-none"
              />
            </div>

            {/* Visual Style & Sounds */}
            <div className="p-3 rounded-xl bg-[#0f1013] border border-white/10 focus-within:border-emerald-500/50 transition-all">
              <label className="font-semibold text-emerald-300 block mb-1 flex items-center gap-1">
                <span>🎬 Gaya Visual Animasi 3D & Efek Suara:</span>
              </label>
              <textarea
                rows={2}
                value={anchors.style}
                onChange={(e) => setAnchors({ ...anchors, style: e.target.value })}
                placeholder="Contoh: Animasi 3D Pixar/Disney, warna jenuh sangat cerah, pencahayaan ramah anak, sound effect ceria, 24fps..."
                className="w-full bg-transparent text-gray-200 placeholder-gray-600 text-xs outline-none resize-none"
              />
            </div>
          </div>
        </div>

        {/* Generate Button */}
        <div className="pt-2 flex justify-end">
          <button
            type="button"
            disabled={disabled || generating}
            onClick={onGenerate}
            className="w-full sm:w-auto flex items-center justify-center gap-2.5 px-6 py-3 rounded-xl bg-gradient-to-r from-amber-600 via-orange-600 to-red-600 hover:from-amber-500 hover:to-red-500 text-white font-bold text-sm shadow-lg shadow-amber-900/30 disabled:opacity-40 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
          >
            {generating ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Menganalisis & Menyusun {totalCalculatedScenes} Scene Prompt...</span>
              </>
            ) : (
              <>
                <Car className="w-4 h-4 text-white" />
                <span>{hasUploadedImage ? '🚀 Analisis Video + Foto & Buat 60 Scene AI Prompt' : '🚀 Buat 60 Scene Alur Video Anak Konsisten'}</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
