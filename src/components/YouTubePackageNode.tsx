import React, { useState } from 'react';
import { YouTubePackage } from '../types';
import { 
  Sparkles, 
  Copy, 
  Check, 
  Flame, 
  Image as ImageIcon, 
  FileText, 
  Tag, 
  Clock, 
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Award,
  Zap,
  Layers,
  Video
} from 'lucide-react';

interface YouTubePackageNodeProps {
  packageData: YouTubePackage;
  referenceImage?: string | null;
}

export const YouTubePackageNode: React.FC<YouTubePackageNodeProps> = ({
  packageData,
  referenceImage
}) => {
  const [copiedTitleIndex, setCopiedTitleIndex] = useState<number | null>(null);
  const [copiedThumbnail, setCopiedThumbnail] = useState<boolean>(false);
  const [copiedDescription, setCopiedDescription] = useState<boolean>(false);
  const [copiedTags, setCopiedTags] = useState<boolean>(false);
  const [thumbnailTab, setThumbnailTab] = useState<'primary' | 'alt'>('primary');
  const [showFullDesc, setShowFullDesc] = useState<boolean>(false);
  const [selectedText, setSelectedText] = useState<string>(
    packageData.thumbnail_text || 'VROOM VROOM! 🚗'
  );
  const [customText, setCustomText] = useState<string>('');

  const defaultTextOptions = packageData.thumbnail_text_options || [
    'VROOM VROOM! 🚗',
    'SUPER SPEED! ⚡',
    'MISSION WIN! 🏆',
    'LET\'S GO! 🚀',
    'GO GO GO! 🏁'
  ];

  const handleCopyText = (text: string, type: 'title' | 'thumbnail' | 'desc' | 'tags', index?: number) => {
    navigator.clipboard.writeText(text);
    if (type === 'title' && index !== undefined) {
      setCopiedTitleIndex(index);
      setTimeout(() => setCopiedTitleIndex(null), 2000);
    } else if (type === 'thumbnail') {
      setCopiedThumbnail(true);
      setTimeout(() => setCopiedThumbnail(false), 2000);
    } else if (type === 'desc') {
      setCopiedDescription(true);
      setTimeout(() => setCopiedDescription(false), 2000);
    } else if (type === 'tags') {
      setCopiedTags(true);
      setTimeout(() => setCopiedTags(false), 2000);
    }
  };

  const currentTextToRender = customText.trim() || selectedText.replace(/[^\w\s\?!°#\-]/g, '').trim() || 'EPIC JUMP!';

  const rawThumbnailPrompt = thumbnailTab === 'primary' 
    ? packageData.thumbnail_prompt 
    : (packageData.thumbnail_alt_prompt || packageData.thumbnail_prompt);

  // Dynamically embed the chosen 3D text into the thumbnail prompt
  const activeThumbnailPrompt = rawThumbnailPrompt
    .replace(/reading exactly "[^"]*"/g, `reading exactly "${currentTextToRender}"`)
    .replace(/title text "[^"]*"/g, `title text "${currentTextToRender}"`);

  return (
    <div className="relative rounded-2xl bg-[#16171c] border-2 border-red-500/30 p-5 sm:p-6 shadow-2xl transition-all">
      {/* Node Header */}
      <div className="flex flex-wrap items-center justify-between pb-4 mb-6 border-b border-white/10 gap-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-red-600 via-orange-600 to-amber-600 flex items-center justify-center text-white shadow-lg shadow-red-900/40">
            <svg className="w-5 h-5 fill-white" viewBox="0 0 24 24">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-red-950/80 text-red-300 border border-red-800/40 font-bold">
                VIRAL YT KIT
              </span>
              <h2 className="text-base font-extrabold text-white">
                Judul FYP, Deskripsi SEO & AI Thumbnail Prompt
              </h2>
            </div>
            <p className="text-xs text-gray-400">
              Paket siap upload YouTube: Judul hype b. Inggris ber-CTR tinggi, deskripsi lengkap timestamps, dan prompt thumbnail untuk Gemini / Imagen
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-red-500/15 border border-red-500/30 text-red-300 flex items-center gap-1.5">
            <Flame className="w-3.5 h-3.5 text-red-400 fill-red-400" />
            <span>High-CTR Algorithm Ready</span>
          </span>
        </div>
      </div>

      <div className="space-y-6">
        {/* 1. VIRAL FYP TITLES (ENGLISH) */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-amber-300" />
              <span>5 Pilihan Judul Video YouTube Hype / FYP (Bahasa Inggris):</span>
            </label>
            <span className="text-[11px] text-gray-400">Klik untuk langsung salin judul</span>
          </div>

          <div className="space-y-2">
            {packageData.viral_titles.map((titleText, idx) => {
              const isRecommended = idx === 0;
              const isCopied = copiedTitleIndex === idx;

              return (
                <div
                  key={idx}
                  className={`p-3.5 rounded-xl border transition-all flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 ${
                    isRecommended
                      ? 'bg-gradient-to-r from-amber-950/30 via-[#181920] to-[#121318] border-amber-500/40 shadow-md'
                      : 'bg-[#0f1013] border-white/10 hover:border-white/20'
                  }`}
                >
                  <div className="flex items-start gap-2.5 flex-1 min-w-0">
                    <span className="shrink-0 w-6 h-6 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-xs font-mono font-bold text-gray-400">
                      {idx + 1}
                    </span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        {isRecommended && (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                            <Award className="w-3 h-3 text-amber-400" />
                            🏆 Rekomendasi #1 (Highest CTR)
                          </span>
                        )}
                        <span className="text-[10px] text-gray-500 font-mono">
                          {idx === 0 ? 'Stunt Ramp Focus' : idx === 1 ? 'Championship Challenge' : idx === 2 ? 'Obstacle Run' : idx === 3 ? 'Story Adventure' : 'Speed Challenge'}
                        </span>
                      </div>
                      <p className="text-xs sm:text-sm font-bold text-gray-100 break-words leading-relaxed font-sans">
                        {titleText}
                      </p>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => handleCopyText(titleText, 'title', idx)}
                    className={`shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                      isCopied
                        ? 'bg-emerald-600 text-white shadow-md'
                        : isRecommended
                        ? 'bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white'
                        : 'bg-white/10 hover:bg-white/15 text-gray-200 border border-white/10'
                    }`}
                  >
                    {isCopied ? <Check className="w-3.5 h-3.5 text-emerald-100" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{isCopied ? 'Tersalin!' : 'Salin Judul'}</span>
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* 2. AI THUMBNAIL PROMPT (GEMINI / IMAGEN 3 / MIDJOURNEY) */}
        <div className="p-4 sm:p-5 rounded-xl bg-gradient-to-br from-[#18131d] via-[#141219] to-[#0e0f14] border-2 border-purple-500/30 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-white/10">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-purple-600/20 border border-purple-500/30 text-purple-300">
                <ImageIcon className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  Prompt Gambar Thumbnail AI (Google Gemini / Imagen 3 / Midjourney)
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 font-semibold">
                    16:9 Widescreen (1280x720)
                  </span>
                </h3>
                <p className="text-xs text-gray-400">
                  Prompt sinematik 3D CGI dengan pop-out mobil melompat ke arah kamera & wajah anak kagum
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={() => handleCopyText(activeThumbnailPrompt, 'thumbnail')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-lg ${
                copiedThumbnail
                  ? 'bg-emerald-600 text-white shadow-emerald-900/40'
                  : 'bg-gradient-to-r from-purple-600 via-pink-600 to-amber-600 hover:from-purple-500 hover:to-amber-500 text-white shadow-purple-900/40'
              }`}
            >
              {copiedThumbnail ? <Check className="w-4 h-4 text-emerald-100" /> : <Copy className="w-4 h-4" />}
              <span>{copiedThumbnail ? 'Prompt Thumbnail Tersalin! ✅' : 'Salin Prompt Thumbnail Gemini'}</span>
            </button>
          </div>

          {/* Thumbnail Style Tabs */}
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => setThumbnailTab('primary')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                thumbnailTab === 'primary'
                  ? 'bg-purple-600 text-white shadow-md'
                  : 'bg-white/5 text-gray-400 hover:bg-white/10'
              }`}
            >
              🚀 Opsi 1: Action Jump Hero Shot (Paling Populer & FYP)
            </button>
            {packageData.thumbnail_alt_prompt && (
              <button
                type="button"
                onClick={() => setThumbnailTab('alt')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  thumbnailTab === 'alt'
                    ? 'bg-purple-600 text-white shadow-md'
                    : 'bg-white/5 text-gray-400 hover:bg-white/10'
                }`}
              >
                👦 Opsi 2: Close-up Happy Kid POV (Sentuhan Emosional)
              </button>
            )}
          </div>

          {/* 3D Thumbnail Text Overlay Selector */}
          <div className="p-3 rounded-xl bg-black/40 border border-purple-500/20 space-y-2">
            <div className="flex flex-wrap items-center justify-between gap-1.5">
              <label className="text-[11px] font-bold text-amber-300 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                <span>Pilih Teks 3D Menarik Pada Gambar Thumbnail:</span>
              </label>
              <span className="text-[10px] text-gray-400">
                Tercetak langsung di gambar: <strong className="text-yellow-300">"{currentTextToRender}"</strong>
              </span>
            </div>

            <div className="flex flex-wrap items-center gap-1.5">
              {defaultTextOptions.map((opt, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => { setSelectedText(opt); setCustomText(''); }}
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                    (selectedText === opt && !customText.trim())
                      ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-md shadow-amber-900/40 scale-105'
                      : 'bg-white/5 text-gray-300 hover:bg-white/10 border border-white/10'
                  }`}
                >
                  {opt}
                </button>
              ))}

              <input
                type="text"
                value={customText}
                onChange={(e) => setCustomText(e.target.value)}
                placeholder="Atau ketik teks sendiri..."
                className="px-2.5 py-1 rounded-lg bg-black/60 border border-white/15 text-xs text-yellow-200 placeholder-gray-500 outline-none focus:border-amber-400 w-36 sm:w-44"
              />
            </div>
          </div>

          {/* Prompt Box */}
          <div
            onClick={() => handleCopyText(activeThumbnailPrompt, 'thumbnail')}
            className="p-3.5 rounded-xl bg-black/60 border border-purple-500/20 hover:border-purple-400/50 cursor-pointer text-xs font-mono text-purple-100 leading-relaxed break-words transition-all group"
            title="Klik untuk langsung copy prompt thumbnail"
          >
            {activeThumbnailPrompt}
          </div>

          {/* Tips Box */}
          <div className="p-3 rounded-lg bg-black/40 border border-white/5 text-xs text-gray-300 space-y-1">
            <div className="font-semibold text-amber-300 flex items-center gap-1.5 text-[11px]">
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              <span>Cara Pakai di Google Gemini / Imagen 3:</span>
            </div>
            <p className="text-[11px] text-gray-400 leading-relaxed">
              Buka <a href="https://gemini.google.com" target="_blank" rel="noreferrer" className="text-purple-400 underline hover:text-purple-300">Gemini (gemini.google.com)</a> atau AI Studio, tempel prompt di atas, lalu minta: <em>"Generate this image in 16:9 aspect ratio for YouTube thumbnail"</em>.
            </p>
          </div>
        </div>

        {/* 3. SEO DESCRIPTION WITH TIMESTAMPS */}
        <div className="p-4 sm:p-5 rounded-xl bg-[#0f1013] border border-white/10 space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-white/5">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-emerald-400" />
              <h3 className="text-sm font-bold text-white">
                Deskripsi Video YouTube (SEO + Chapter Timestamps)
              </h3>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setShowFullDesc(!showFullDesc)}
                className="text-xs text-gray-400 hover:text-white flex items-center gap-1 transition-colors"
              >
                <span>{showFullDesc ? 'Ringkas Tampilan' : 'Lihat Selengkapnya'}</span>
                {showFullDesc ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>
              <button
                type="button"
                onClick={() => handleCopyText(packageData.description, 'desc')}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  copiedDescription
                    ? 'bg-emerald-600 text-white'
                    : 'bg-emerald-600/20 text-emerald-300 hover:bg-emerald-600/30 border border-emerald-500/30'
                }`}
              >
                {copiedDescription ? <Check className="w-3.5 h-3.5 text-emerald-100" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copiedDescription ? 'Deskripsi Tersalin!' : 'Salin Deskripsi'}</span>
              </button>
            </div>
          </div>

          <div className={`p-3.5 rounded-lg bg-black/40 border border-white/5 text-xs text-gray-300 font-mono whitespace-pre-wrap leading-relaxed overflow-hidden transition-all ${showFullDesc ? 'max-h-none' : 'max-h-48'}`}>
            {packageData.description}
          </div>
        </div>

        {/* 4. TOP SEO TAGS FOR YOUTUBE STUDIO */}
        <div className="p-4 rounded-xl bg-[#0f1013] border border-white/10 space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-gray-300 flex items-center gap-1.5">
              <Tag className="w-3.5 h-3.5 text-blue-400" />
              <span>Tags YouTube SEO ({packageData.tags.length} Kata Kunci):</span>
            </span>
            <button
              type="button"
              onClick={() => handleCopyText(packageData.tags.join(', '), 'tags')}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                copiedTags
                  ? 'bg-blue-600 text-white'
                  : 'bg-blue-600/20 text-blue-300 hover:bg-blue-600/30 border border-blue-500/30'
              }`}
            >
              {copiedTags ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedTags ? 'Tags Tersalin!' : 'Salin Semua Tags (Koma)'}</span>
            </button>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {packageData.tags.map((tag, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-gray-300 text-xs font-mono"
              >
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
