import React, { useState } from 'react';
import { ScenePromptItem } from '../types';
import { Video, Copy, Check, Edit3, Camera, Clock, ShieldCheck, Film, Sparkles, MessageCircle, AlertCircle } from 'lucide-react';

interface SceneFlowNodeProps {
  scenes: ScenePromptItem[];
  onUpdateScenePrompt?: (index: number, newPrompt: string) => void;
}

export const SceneFlowNode: React.FC<SceneFlowNodeProps> = ({
  scenes,
  onUpdateScenePrompt
}) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editPromptText, setEditPromptText] = useState<string>('');

  const handleCopyPrompt = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleStartEdit = (index: number, currentPrompt: string) => {
    setEditingIndex(index);
    setEditPromptText(currentPrompt);
  };

  const handleSaveEdit = (index: number) => {
    if (onUpdateScenePrompt) {
      onUpdateScenePrompt(index, editPromptText);
    }
    setEditingIndex(null);
  };

  if (!scenes || scenes.length === 0) {
    return null;
  }

  return (
    <div className="relative rounded-2xl bg-[#16171c] border border-white/10 p-5 sm:p-6 shadow-xl transition-all">
      {/* Node Header */}
      <div className="flex flex-wrap items-center justify-between pb-4 mb-6 border-b border-white/10 gap-3">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center text-white shadow-md">
            <Film className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-gray-400 border border-white/10">
                NODE 04 (FINAL FLOW)
              </span>
              <h2 className="text-base font-bold text-white">Alur Prompt-to-Video Konsisten (Per 10 Detik Penuh)</h2>
            </div>
            <p className="text-xs text-gray-400">
              Total {scenes.length} Scene siap dimasukkan ke Google Veo / Kling AI / Runway / Luma
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Objek & Karakter Konsisten Terhubung</span>
          </span>
        </div>
      </div>

      {/* Google Flow Connection Timeline */}
      <div className="relative space-y-6 before:absolute before:inset-0 before:left-5 before:w-0.5 before:bg-gradient-to-b before:from-blue-500 before:via-purple-500 before:to-emerald-500 before:hidden md:before:block">
        {scenes.map((scene, idx) => {
          const isCopied = copiedIndex === idx;
          const isEditing = editingIndex === idx;

          return (
            <div
              key={scene.scene_index}
              className="relative pl-0 md:pl-12 group transition-all"
            >
              {/* Timeline Flow Node Dot */}
              <div className="hidden md:flex absolute left-3.5 top-6 -translate-x-1/2 w-4 h-4 rounded-full bg-[#16171c] border-2 border-blue-500 group-hover:border-emerald-400 group-hover:scale-125 transition-all z-10 items-center justify-center">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-400 group-hover:bg-emerald-300"></span>
              </div>

              {/* Scene Card */}
              <div className="rounded-xl bg-[#0f1013] border border-white/10 hover:border-blue-500/40 p-4 sm:p-5 transition-all shadow-md">
                {/* Scene Meta Bar */}
                <div className="flex flex-wrap items-center justify-between gap-2 pb-3 mb-3 border-b border-white/5">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-lg bg-blue-600/20 text-blue-300 border border-blue-500/30 text-xs font-mono font-bold">
                      SCENE {scene.scene_index.toString().padStart(2, '0')}
                    </span>
                    <span className="flex items-center gap-1 font-mono text-xs px-2.5 py-1 rounded-lg bg-white/5 text-gray-300 border border-white/10">
                      <Clock className="w-3 h-3 text-amber-400" />
                      {scene.time_range} ({scene.duration_sec}s Penuh)
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-md bg-purple-950/80 text-purple-300 border border-purple-800/40">
                      <Camera className="w-3 h-3 text-purple-400" />
                      {scene.camera_directive}
                    </span>

                    <button
                      type="button"
                      onClick={() => handleCopyPrompt(scene.video_prompt, idx)}
                      className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                        isCopied
                          ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/40'
                          : 'bg-blue-600 hover:bg-blue-500 text-white'
                      }`}
                    >
                      {isCopied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{isCopied ? 'Tersalin!' : 'Copy Prompt'}</span>
                    </button>
                  </div>
                </div>

                {/* Section 1: 10s Spoken Dialogue */}
                <div className="mb-3 p-3 rounded-lg bg-[#141519] border border-white/5">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[11px] font-semibold text-gray-400 flex items-center gap-1">
                      <MessageCircle className="w-3 h-3 text-blue-400" />
                      Percakapan Satu Scene 10 Detik Penuh:
                    </span>
                    <span className="text-[10px] text-emerald-400 font-mono">100% Spoken Audio</span>
                  </div>
                  <p className="text-xs text-gray-200 italic leading-relaxed">
                    "{scene.dialogue}"
                  </p>
                </div>

                {/* Section 2: Visual Action & Object Consistency */}
                <div className="mb-3 grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 rounded-lg bg-[#141519] border border-white/5">
                    <span className="text-[10px] font-semibold text-purple-300 block mb-0.5">
                      🎬 Visual Action & Alur Gerak:
                    </span>
                    <p className="text-gray-300 text-[11px] leading-relaxed">
                      {scene.action_description}
                    </p>
                  </div>

                  <div className="p-2.5 rounded-lg bg-[#141519] border border-white/5">
                    <span className="text-[10px] font-semibold text-emerald-300 block mb-0.5 flex items-center gap-1">
                      <ShieldCheck className="w-3 h-3" />
                      Konsistensi Objek & Karakter:
                    </span>
                    <p className="text-gray-300 text-[11px] leading-relaxed line-clamp-2">
                      <span className="text-emerald-400 font-medium">Objek:</span> {scene.anchors?.product} | <span className="text-blue-400 font-medium">Subjek:</span> {scene.anchors?.subject}
                    </p>
                  </div>
                </div>

                {/* Section 3: AI Video Prompt (Direct Flow to Video) */}
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-bold text-blue-400 flex items-center gap-1">
                      <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                      Prompt Siap Pakai (Google Flow ➔ Video AI):
                    </span>
                    <button
                      type="button"
                      onClick={() => isEditing ? handleSaveEdit(idx) : handleStartEdit(idx, scene.video_prompt)}
                      className="text-[11px] text-gray-400 hover:text-white flex items-center gap-1 transition-colors"
                    >
                      <Edit3 className="w-3 h-3" />
                      <span>{isEditing ? 'Simpan' : 'Edit Prompt'}</span>
                    </button>
                  </div>

                  {isEditing ? (
                    <div className="space-y-2">
                      <textarea
                        rows={3}
                        value={editPromptText}
                        onChange={(e) => setEditPromptText(e.target.value)}
                        className="w-full p-2.5 rounded-lg bg-black/60 border border-blue-500 text-xs text-gray-100 font-mono outline-none"
                      />
                      <div className="flex justify-end gap-2">
                        <button
                          type="button"
                          onClick={() => setEditingIndex(null)}
                          className="px-2.5 py-1 rounded bg-white/5 text-gray-300 text-[11px]"
                        >
                          Batal
                        </button>
                        <button
                          type="button"
                          onClick={() => handleSaveEdit(idx)}
                          className="px-3 py-1 rounded bg-blue-600 text-white text-[11px] font-semibold"
                        >
                          Simpan Perubahan
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div
                      onClick={() => handleCopyPrompt(scene.video_prompt, idx)}
                      className="p-3 rounded-lg bg-black/40 border border-white/10 hover:border-blue-500/50 cursor-pointer text-xs font-mono text-gray-200 leading-relaxed break-words transition-all group/code"
                      title="Klik untuk langsung copy prompt"
                    >
                      {scene.video_prompt}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

