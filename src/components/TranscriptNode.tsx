import React, { useState } from 'react';
import { TranscriptItem } from '../types';
import { FileText, Search, Copy, Check, ChevronDown, ChevronUp, MessageSquare } from 'lucide-react';

interface TranscriptNodeProps {
  items: TranscriptItem[];
  fullText: string;
  language: string;
  totalSegments: number;
}

export const TranscriptNode: React.FC<TranscriptNodeProps> = ({
  items,
  fullText,
  language,
  totalSegments
}) => {
  const [search, setSearch] = useState('');
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const filteredItems = items.filter((item) =>
    item.text.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="relative rounded-2xl bg-[#16171c] border border-white/10 p-5 sm:p-6 shadow-xl transition-all">
      {/* Node Header */}
      <div className="flex items-center justify-between pb-4 mb-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <MessageSquare className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-gray-400 border border-white/10">
                NODE 03
              </span>
              <h2 className="text-base font-bold text-white">Transkrip Percakapan YouTube Penuh</h2>
            </div>
            <p className="text-xs text-gray-400">
              Hasil ekstraksi audio & percakapan lengkap ({totalSegments} segmen perkataan)
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-xs text-gray-300 hover:text-white transition-colors border border-white/5"
            title="Salin seluruh transkrip"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Tersalin' : 'Salin Semua'}</span>
          </button>

          <button
            type="button"
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white transition-colors"
          >
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {isExpanded && (
        <div className="space-y-3">
          {/* Search bar */}
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-3 text-gray-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Cari kata atau topik di dalam transkrip percakapan..."
              className="w-full pl-9 pr-4 py-2 rounded-xl bg-[#0f1013] border border-white/10 text-xs text-white placeholder-gray-500 outline-none focus:border-blue-500 transition-all"
            />
          </div>

          {/* Transcript List Scroll Area */}
          <div className="max-h-64 overflow-y-auto space-y-1.5 pr-2 rounded-xl bg-[#0d0e11] p-3 border border-white/5 font-sans">
            {filteredItems.length > 0 ? (
              filteredItems.map((item, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors group"
                >
                  <span className="shrink-0 font-mono text-[11px] px-1.5 py-0.5 rounded bg-blue-950/80 text-blue-300 border border-blue-800/40 mt-0.5">
                    {formatTime(item.start)}
                  </span>
                  <p className="text-xs text-gray-300 leading-relaxed group-hover:text-white transition-colors">
                    {item.text}
                  </p>
                </div>
              ))
            ) : (
              <p className="text-xs text-gray-500 text-center py-6">
                Tidak ada percakapan yang cocok dengan pencarian.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

