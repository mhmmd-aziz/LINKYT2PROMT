import React, { useState } from 'react';
import { VideoMetadata, KidsVideoVision } from '../types';
import { Link2, Sparkles, Clock, User, CheckCircle2, AlertCircle, PlayCircle, ClipboardPaste, Video, Car, Compass } from 'lucide-react';

interface UrlInputNodeProps {
  url: string;
  setUrl: (url: string) => void;
  loading: boolean;
  onExtract: (overrideUrl?: string) => void;
  metadata: VideoMetadata | null;
  videoVision?: KidsVideoVision | null;
  error: string | null;
}

export const UrlInputNode: React.FC<UrlInputNodeProps> = ({
  url,
  setUrl,
  loading,
  onExtract,
  metadata,
  videoVision,
  error
}) => {
  const [pasteSuccess, setPasteSuccess] = useState(false);

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) {
        setUrl(text);
        setPasteSuccess(true);
        setTimeout(() => setPasteSuccess(false), 2000);
      }
    } catch (err) {
      console.warn("Clipboard access denied:", err);
    }
  };

  const sampleLinks = [
    { label: "🚗 Main Mobil Anak (Toy Cars)", url: "https://www.youtube.com/watch?v=dQw4w9WgXcQ" },
    { label: "🚛 Monster Truck Jump", url: "https://www.youtube.com/watch?v=jNQXAC9IVRw" },
    { label: "🏁 Balapan Mobil Lintasan", url: "https://www.youtube.com/shorts/kJQP7kiw5Fk" }
  ];

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s (${seconds} detik)`;
  };

  return (
    <div className="relative rounded-2xl bg-[#16171c] border border-white/10 p-5 sm:p-6 shadow-xl transition-all">
      {/* Node Header */}
      <div className="flex flex-wrap items-center justify-between pb-4 mb-5 border-b border-white/10 gap-2">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-red-600/20 border border-red-500/30 flex items-center justify-center text-red-400">
            <Video className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-gray-400 border border-white/10">
                NODE 01
              </span>
              <h2 className="text-base font-bold text-white">Input Link Video YouTube Anak (Main Mobil / Kartun)</h2>
            </div>
            <p className="text-xs text-gray-400">
              Copas link video YT orang lain yang ingin dibuat ulang versinya (20 scene prompt alur bersambung)
            </p>
          </div>
        </div>

        {metadata && (
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Video & Visi Terhubung</span>
          </div>
        )}
      </div>

      {/* Input Box */}
      <div className="space-y-3">
        <div className="relative flex flex-col sm:flex-row gap-2">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-500">
              <Link2 className="w-4 h-4" />
            </div>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Copas link YouTube di sini (contoh: video anak main mobil, Hot Wheels, monster truck, balapan)"
              className="w-full pl-10 pr-24 py-3 rounded-xl bg-[#0f1013] border border-white/15 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-sm text-white placeholder-gray-500 outline-none transition-all"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && url.trim()) {
                  onExtract();
                }
              }}
            />
            <button
              type="button"
              onClick={handlePaste}
              className="absolute inset-y-1.5 right-1.5 px-2.5 rounded-lg bg-white/5 hover:bg-white/10 text-gray-300 hover:text-white text-xs flex items-center gap-1.5 transition-colors border border-white/5"
              title="Paste dari Clipboard"
            >
              <ClipboardPaste className="w-3.5 h-3.5" />
              <span>{pasteSuccess ? 'Tersalin!' : 'Paste'}</span>
            </button>
          </div>

          <button
            type="button"
            disabled={loading || !url.trim()}
            onClick={() => onExtract()}
            className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-red-600 via-amber-600 to-blue-600 hover:from-red-500 hover:to-blue-500 text-white font-semibold text-sm shadow-lg shadow-red-900/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Membaca Visi & Audio...</span>
              </>
            ) : (
              <>
                <Car className="w-4 h-4" />
                <span>Ekstrak & Baca Visi Video</span>
              </>
            )}
          </button>
        </div>

        {/* Quick Sample Chips */}
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs text-gray-400">
          <span className="text-[11px] text-gray-500">Coba Link:</span>
          {sampleLinks.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setUrl(sample.url);
                onExtract(sample.url);
              }}
              className="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-gray-300 text-[11px] transition-colors"
            >
              {sample.label}
            </button>
          ))}
        </div>

        {error && (
          <div className="flex items-start gap-2.5 p-3 rounded-xl bg-red-950/40 border border-red-800/50 text-red-300 text-xs mt-3">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-red-400" />
            <div>
              <p className="font-semibold">Gagal memproses link YouTube:</p>
              <p className="opacity-90">{error}</p>
            </div>
          </div>
        )}

        {/* Video Preview & Vision Concept Card */}
        {metadata && (
          <div className="mt-4 space-y-3 animate-in fade-in duration-200">
            <div className="p-4 rounded-xl bg-[#0f1013] border border-white/10 flex flex-col sm:flex-row gap-4">
              <div className="relative w-full sm:w-48 h-28 sm:h-auto rounded-lg overflow-hidden bg-black shrink-0 border border-white/10">
                <img
                  src={metadata.thumbnail}
                  alt={metadata.title}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    (e.target as HTMLElement).style.display = 'none';
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-2">
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-black/80 text-white flex items-center gap-1">
                    <PlayCircle className="w-3 h-3 text-red-400" />
                    {formatDuration(metadata.duration)}
                  </span>
                </div>
              </div>

              <div className="flex-1 flex flex-col justify-between space-y-2">
                <div>
                  <h3 className="text-sm font-semibold text-white line-clamp-2 leading-snug">
                    {metadata.title}
                  </h3>
                  <div className="flex flex-wrap items-center gap-3 mt-2 text-xs text-gray-400">
                    <span className="flex items-center gap-1">
                      <User className="w-3.5 h-3.5 text-gray-500" />
                      {metadata.author}
                    </span>
                    <span className="flex items-center gap-1 font-mono">
                      <Clock className="w-3.5 h-3.5 text-gray-500" />
                      Durasi Asli: {formatDuration(metadata.duration)}
                    </span>
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-white/5">
                  <span className="text-[11px] text-gray-400">
                    Target Alur Scene 10 Detik:
                  </span>
                  <span className="text-[11px] font-mono font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
                    {Math.min(20, Math.max(1, Math.ceil(metadata.duration / 10)))} Scene (Maksimal 20)
                  </span>
                </div>
              </div>
            </div>

            {/* Video Vision Understood Box */}
            {videoVision && (
              <div className="p-3.5 rounded-xl bg-gradient-to-r from-blue-950/30 via-purple-950/20 to-amber-950/20 border border-blue-500/30 text-xs">
                <div className="flex items-center gap-2 mb-1.5">
                  <Compass className="w-4 h-4 text-amber-400 animate-spin" />
                  <span className="font-bold text-amber-300 uppercase tracking-wide text-[11px]">
                    Visi & Alur Cerita Video YouTube yang Dibaca Sistem:
                  </span>
                </div>
                <p className="text-gray-200 font-medium">
                  {videoVision.vision_theme}
                </p>
                <p className="text-gray-400 text-[11px] mt-1 leading-relaxed">
                  {videoVision.vision_summary}
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
