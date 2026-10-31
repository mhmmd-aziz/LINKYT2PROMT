import React, { useState } from 'react';
import { ScenePromptItem, VideoMetadata, YouTubePackage } from '../types';
import { X, Copy, Check, Download, FileText, FileSpreadsheet, Code, Film, Car, Mic, Video, Sparkles } from 'lucide-react';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  scenes: ScenePromptItem[];
  metadata: VideoMetadata | null;
  youtubePackage?: YouTubePackage | null;
}

export const ExportModal: React.FC<ExportModalProps> = ({
  isOpen,
  onClose,
  scenes,
  metadata,
  youtubePackage
}) => {
  const [copiedType, setCopiedType] = useState<string | null>(null);

  if (!isOpen) return null;

  const generateYouTubeKitText = () => {
    if (!youtubePackage) return '';
    let kit = `=== IMZY TOOLS YT - VIRAL YOUTUBE KIT (HYPE TITLES, SEO DESCRIPTION & THUMBNAIL) ===\n\n`;
    kit += `--- 1. RECOMMENDED VIRAL YOUTUBE TITLE (HIGHEST CTR) ---\n`;
    kit += `${youtubePackage.primary_title}\n\n`;
    kit += `--- 2. ALL 5 VIRAL FYP TITLE VARIATIONS ---\n`;
    youtubePackage.viral_titles.forEach((t, i) => {
      kit += `${i + 1}. ${t}\n`;
    });
    kit += `\n--- 3. AI THUMBNAIL GENERATION PROMPT (GEMINI / IMAGEN 3 / MIDJOURNEY - 16:9) ---\n`;
    kit += `${youtubePackage.thumbnail_prompt}\n\n`;
    if (youtubePackage.thumbnail_alt_prompt) {
      kit += `--- ALTERNATIVE CLOSE-UP THUMBNAIL PROMPT ---\n${youtubePackage.thumbnail_alt_prompt}\n\n`;
    }
    kit += `--- 4. FULL YOUTUBE SEO DESCRIPTION (WITH TIMESTAMPS) ---\n`;
    kit += `${youtubePackage.description}\n\n`;
    kit += `--- 5. TOP SEARCH TAGS (FOR YOUTUBE STUDIO TAGS FIELD) ---\n`;
    kit += `${youtubePackage.tags.join(', ')}\n\n`;
    return kit;
  };

  const generateAllPromptsText = () => {
    let result = '';
    if (youtubePackage) {
      result += generateYouTubeKitText();
      result += `====================================================================\n\n`;
    }
    result += `=== IMZY TOOLS YT - KIDS ${scenes.length}-SCENE VIDEO FLOW (ENGLISH CONTINUOUS SCRIPT) ===\n`;
    result += `Video Reference: ${metadata?.title || 'Kids YouTube Video'}\n`;
    result += `Total Scenes: ${scenes.length} (Full 10-Second Continuous Spoken English)\n`;
    result += `Object & Character Locking: 100% Consistent\n\n`;

    scenes.forEach((s) => {
      const dialogue = s.english_dialogue || s.dialogue;
      result += `[SCENE ${s.scene_index.toString().padStart(2, '0')} | ${s.time_range} | 10s Penuh | ${s.word_count || ''} Words${s.is_closing ? ' | 🏆 PENUTUP FILM' : ''}]\n`;
      if (s.act) {
        result += `Narrative Act: ${s.act} (${s.milestone || ''})\n`;
      }
      result += `Spoken English Voiceover (No Dead Air):\n"${dialogue}"\n\n`;
      if (s.sound_effects) {
        result += `Sound Effects (SFX): ${s.sound_effects}\n\n`;
      }
      if (s.visual_effects) {
        result += `Visual Effects (VFX): ${s.visual_effects}\n\n`;
      }
      result += `AI Video Generation Prompt:\n${s.video_prompt}\n\n`;
      result += `Negative Prompt: ${s.negative_prompt}\n`;
      result += `----------------------------------------------------\n\n`;
    });
    return result;
  };

  const generateVoiceoverOnlyScript = () => {
    let script = `=== IMZY TOOLS YT - FULL ENGLISH VOICEOVER SCRIPT (FOR ELEVENLABS / TTS) ===\n\n`;
    scenes.forEach((s) => {
      const dialogue = s.english_dialogue || s.dialogue;
      script += `[Scene ${s.scene_index} - ${s.time_range}]\n${dialogue}\n\n`;
    });
    return script;
  };

  const handleCopyAll = () => {
    const text = generateAllPromptsText();
    navigator.clipboard.writeText(text);
    setCopiedType('all');
    setTimeout(() => setCopiedType(null), 2000);
  };

  const handleCopyVoiceover = () => {
    const script = generateVoiceoverOnlyScript();
    navigator.clipboard.writeText(script);
    setCopiedType('voiceover');
    setTimeout(() => setCopiedType(null), 2000);
  };

  const handleCopyYouTubeKit = () => {
    const kit = generateYouTubeKitText();
    navigator.clipboard.writeText(kit);
    setCopiedType('ytkit');
    setTimeout(() => setCopiedType(null), 2000);
  };

  const handleDownloadYouTubeKitTXT = () => {
    const kit = generateYouTubeKitText();
    const blob = new Blob([kit], { type: 'text/plain;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imzy-youtube-kit-${metadata?.id || 'viral'}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadJSON = () => {
    const data = {
      project: "imzy tools yt",
      theme: "Kids Video Toy Car Play (Continuous English Story)",
      generated_at: new Date().toISOString(),
      metadata: metadata,
      youtube_package: youtubePackage || undefined,
      total_scenes: scenes.length,
      scene_duration_sec: 10,
      scenes: scenes
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imzy-tools-yt-${scenes.length}scenes-${metadata?.id || 'export'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadVoiceoverTXT = () => {
    const script = generateVoiceoverOnlyScript();
    const blob = new Blob([script], { type: 'text/plain;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imzy-voiceover-script-${metadata?.id || 'voice'}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadCSV = () => {
    const header = "Scene,TimeRange,DurationSec,WordCount,Act,Milestone,IsClosing,SpokenEnglishDialogue,SoundEffects,VisualEffects,VideoPrompt,CameraDirective,NegativePrompt\n";
    const rows = scenes.map(s => {
      const escape = (str: string) => `"${(str || '').replace(/"/g, '""')}"`;
      const dialogue = s.english_dialogue || s.dialogue;
      return `${s.scene_index},${escape(s.time_range)},${s.duration_sec},${s.word_count || ''},${escape(s.act || '')},${escape(s.milestone || '')},${s.is_closing ? 'YES' : 'NO'},${escape(dialogue)},${escape(s.sound_effects || '')},${escape(s.visual_effects || '')},${escape(s.video_prompt)},${escape(s.camera_directive)},${escape(s.negative_prompt)}`;
    }).join('\n');

    const blob = new Blob([header + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imzy-tools-yt-scenes-${metadata?.id || 'export'}.csv`;
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
      const dialogue = s.english_dialogue || s.dialogue;
      srt += `${s.scene_index}\n`;
      srt += `${toSrtTime(s.start_time)} --> ${toSrtTime(s.end_time)}\n`;
      srt += `${dialogue}\n\n`;
    });

    const blob = new Blob([srt], { type: 'text/plain;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `imzy-english-subs-${metadata?.id || 'subs'}.srt`;
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
              <h3 className="text-lg font-bold text-white">Export Alur Video Anak & Voiceover ({scenes.length} Scene)</h3>
              <p className="text-xs text-gray-400">Percakapan Full 10 Detik English Bersambung + Prompt Video Sinematik</p>
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
        <div className="grid grid-cols-2 sm:grid-cols-6 gap-2 mb-4">
          <button
            type="button"
            onClick={handleCopyAll}
            className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white font-medium text-xs shadow-md transition-all active:scale-[0.98]"
          >
            {copiedType === 'all' ? <Check className="w-5 h-5 text-emerald-200" /> : <Copy className="w-5 h-5" />}
            <span>{copiedType === 'all' ? 'Tersalin!' : 'Copy Semua Prompt'}</span>
          </button>

          {youtubePackage && (
            <button
              type="button"
              onClick={handleCopyYouTubeKit}
              className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-gradient-to-r from-red-600 to-purple-600 hover:from-red-500 hover:to-purple-500 text-white font-medium text-xs shadow-md transition-all active:scale-[0.98]"
            >
              {copiedType === 'ytkit' ? <Check className="w-5 h-5 text-emerald-200" /> : <Video className="w-5 h-5 text-red-300" />}
              <span>{copiedType === 'ytkit' ? 'Kit Tersalin!' : 'Copy YouTube Kit'}</span>
            </button>
          )}

          <button
            type="button"
            onClick={handleCopyVoiceover}
            className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs shadow-md transition-all active:scale-[0.98]"
          >
            {copiedType === 'voiceover' ? <Check className="w-5 h-5 text-emerald-200" /> : <Mic className="w-5 h-5" />}
            <span>{copiedType === 'voiceover' ? 'Tersalin!' : 'Copy English Script'}</span>
          </button>

          {youtubePackage ? (
            <button
              type="button"
              onClick={handleDownloadYouTubeKitTXT}
              className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-[#23252b] hover:bg-[#2c2e36] text-gray-200 border border-white/10 font-medium text-xs transition-all active:scale-[0.98]"
            >
              <FileText className="w-5 h-5 text-red-400" />
              <span>Download YT Kit (.TXT)</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={handleDownloadVoiceoverTXT}
              className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-[#23252b] hover:bg-[#2c2e36] text-gray-200 border border-white/10 font-medium text-xs transition-all active:scale-[0.98]"
            >
              <FileText className="w-5 h-5 text-amber-400" />
              <span>Download Voice (.TXT)</span>
            </button>
          )}

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
            onClick={handleDownloadSRT}
            className="flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl bg-[#23252b] hover:bg-[#2c2e36] text-gray-200 border border-white/10 font-medium text-xs transition-all active:scale-[0.98]"
          >
            <Film className="w-5 h-5 text-emerald-400" />
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
