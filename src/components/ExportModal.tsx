import React, { useState } from 'react';
import { ScenePromptItem, VideoMetadata } from '../types';
import { X, Copy, Check, Download, FileText, FileSpreadsheet, Code, Film, Car } from 'lucide-react';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  scenes: ScenePromptItem[];
  metadata: VideoMetadata | null;
}

export const ExportModal: React.FC<ExportModalProps> = ({
  isOpen,
  onClose,
  scenes,
  metadata
}) => {
  const [copiedType, setCopiedType] = useState<string | null>(null);

  if (!isOpen) return null;

  const generateAllPromptsText = () => {
    let result = `=== IMSY TOOLS YT - KIDS YOUTUBE 60 SCENE PROMPT FLOW ===\n`;
    result += `Video Acuan: ${metadata?.title || 'Kids YouTube Video'}\n`;
    result += `Total Scenes: ${scenes.length} (10 Detik per Scene Penuh)\n`;
    result += `Tema: Video Anak Main Mobil & Sound Effects Ceria\n`;
    result += `Konsistensi Mainan & Karakter: Aktif 100%\n\n`;

    scenes.forEach((s) => {
      result += `[SCENE ${s.scene_index.toString().padStart(2, '0')} | ${s.time_range} | ${s.duration_sec}s]\n`;
      result += `Suara / Percakapan 10s: "${s.dialogue}"\n`;
      if (s.sound_effects) {
        result += `Sound Effects (SFX): ${s.sound_effects}\n`;
      }
      result += `Prompt Video AI:\n${s.video_prompt}\n`;
      result += `Negative Prompt: ${s.negative_prompt}\n`;
      result += `----------------------------------------------------\n\n`;
    });
    return result;
  };

  const handleCopyAll = () => {
    const text = generateAllPromptsText();
    navigator.clipboard.writeText(text);
    setCopiedType('all');
    setTimeout(() => setCopiedType(null), 2000);
  };

  const handleDownloadJSON = () => {
    const data = {
      project: "imsy tools yt",
      theme: "Kids Video Toy Car Play & Sound Effects",
      generated_at: new Date().toISOString(),
      metadata: metadata,
      total_scenes: scenes.length,
      scene_duration_sec: 10,
      scenes: scenes
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imsy-tools-yt-scenes-${metadata?.id || 'export'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadCSV = () => {
    const header = "Scene,TimeRange,DurationSec,SpokenAudio,SoundEffects,VideoPrompt,CameraDirective,NegativePrompt\n";
    const rows = scenes.map(s => {
      const escape = (str: string) => `"${(str || '').replace(/"/g, '""')}"`;
      return `${s.scene_index},${escape(s.time_range)},${s.duration_sec},${escape(s.dialogue)},${escape(s.sound_effects || '')},${escape(s.video_prompt)},${escape(s.camera_directive)},${escape(s.negative_prompt)}`;
    }).join('\n');

    const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imsy-tools-yt-scenes-${metadata?.id || 'export'}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadSRT = () => {
    let srt = '';
    const toSrtTime = (sec: number) => {
      const hrs = Math.floor(sec / 3600);
      const mins = Math.floor((sec % 3600) / 60);
      const secs = Math.floor(sec % 60);
      const millis = Math.floor((sec % 1) * 1000);
      return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${millis.toString().padStart(3, '0')}`;
    };

    scenes.forEach((s) => {
      srt += `${s.scene_index}\n`;
      srt += `${toSrtTime(s.start_time)} --> ${toSrtTime(s.end_time)}\n`;
      srt += `${s.dialogue}\n\n`;
    });

    const blob = new Blob([srt], { type: 'text/plain;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imsy-tools-yt-subs-${metadata?.id || 'subs'}.srt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-150">
      <div className="bg-[#18191e] border border-white/15 rounded-2xl max-w-2xl w-full p-6 shadow-2xl relative flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/10 mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-600/20 border border-amber-500/30 text-amber-400">
              <Car className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Export Alur Video Anak ({scenes.length} Scene)</h3>
              <p className="text-xs text-gray-400">imsy tools yt • Simpan prompt siap pakai untuk generator video AI</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
          <button
            type="button"
            onClick={handleCopyAll}
            className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-medium text-xs shadow-md transition-all active:scale-[0.98]"
          >
            {copiedType === 'all' ? <Check className="w-5 h-5 text-emerald-300" /> : <Copy className="w-5 h-5" />}
            <span>{copiedType === 'all' ? 'Tersalin!' : 'Copy Semua Prompt'}</span>
          </button>

          <button
            type="button"
            onClick={handleDownloadJSON}
            className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-[#23252b] hover:bg-[#2c2e36] text-gray-200 border border-white/10 font-medium text-xs transition-all active:scale-[0.98]"
          >
            <Code className="w-5 h-5 text-purple-400" />
            <span>Download JSON</span>
          </button>

          <button
            type="button"
            onClick={handleDownloadCSV}
            className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-[#23252b] hover:bg-[#2c2e36] text-gray-200 border border-white/10 font-medium text-xs transition-all active:scale-[0.98]"
          >
            <FileSpreadsheet className="w-5 h-5 text-emerald-400" />
            <span>Download CSV / Sheet</span>
          </button>

          <button
            type="button"
            onClick={handleDownloadSRT}
            className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-[#23252b] hover:bg-[#2c2e36] text-gray-200 border border-white/10 font-medium text-xs transition-all active:scale-[0.98]"
          >
            <FileText className="w-5 h-5 text-amber-400" />
            <span>Download Subtitle (.SRT)</span>
          </button>
        </div>

        {/* Preview Codebox */}
        <div className="flex-1 overflow-y-auto rounded-xl bg-black/60 p-4 border border-white/10 font-mono text-[11px] text-gray-300 leading-relaxed">
          <pre className="whitespace-pre-wrap">{generateAllPromptsText()}</pre>
        </div>

        {/* Footer */}
        <div className="mt-4 flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-semibold transition-colors"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  );
};
