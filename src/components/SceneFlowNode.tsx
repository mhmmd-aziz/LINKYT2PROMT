import React, { useState } from 'react';
import { ScenePromptItem } from '../types';
import { Copy, Check, Edit3, Camera, Clock, ShieldCheck, Film, Sparkles, MessageCircle, Volume2, Car, Mic, ArrowRight, Link } from 'lucide-react';

interface SceneFlowNodeProps {
  scenes: ScenePromptItem[];
  referenceImage?: string | null;
  engineUsed?: string;
  onUpdateScenePrompt?: (index: number, newPrompt: string) => void;
  onUpdateSceneDialogue?: (index: number, newDialogue: string) => void;
}

export const SceneFlowNode: React.FC<SceneFlowNodeProps> = ({
  scenes,
  referenceImage,
  engineUsed,
  onUpdateScenePrompt,
  onUpdateSceneDialogue
}) => {
  const [copiedPromptIndex, setCopiedPromptIndex] = useState<number | null>(null);
  const [copiedDialogueIndex, setCopiedDialogueIndex] = useState<number | null>(null);
  const [editingPromptIndex, setEditingPromptIndex] = useState<number | null>(null);
  const [editPromptText, setEditPromptText] = useState<string>('');
  const [editingDialogueIndex, setEditingDialogueIndex] = useState<number | null>(null);
  const [editDialogueText, setEditDialogueText] = useState<string>('');

  const handleCopyPrompt = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedPromptIndex(index);
    setTimeout(() => setCopiedPromptIndex(null), 2000);
  };

  const handleCopyDialogue = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedDialogueIndex(index);
    setTimeout(() => setCopiedDialogueIndex(null), 2000);
  };

  const handleStartEditPrompt = (index: number, currentPrompt: string) => {
    setEditingPromptIndex(index);
    setEditPromptText(currentPrompt);
  };

  const handleSaveEditPrompt = (index: number) => {
    if (onUpdateScenePrompt) {
      onUpdateScenePrompt(index, editPromptText);
    }
    setEditingPromptIndex(null);
  };

  const handleStartEditDialogue = (index: number, currentDialogue: string) => {
    setEditingDialogueIndex(index);
    setEditDialogueText(currentDialogue);
  };

  const handleSaveEditDialogue = (index: number) => {
    if (onUpdateSceneDialogue) {
      onUpdateSceneDialogue(index, editDialogueText);
    }
    setEditingDialogueIndex(null);
  };

  if (!scenes || scenes.length === 0) {
    return null;
  }

  return (
    <div className="relative rounded-2xl bg-[#16171c] border border-white/10 p-5 sm:p-6 shadow-xl transition-all">
      {/* Node Header */}
      <div className="flex flex-wrap items-center justify-between pb-4 mb-6 border-b border-white/10 gap-3">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-500 via-orange-500 to-red-600 flex items-center justify-center text-white shadow-md">
            <Film className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-gray-400 border border-white/10">
                FINAL FLOW NODE
              </span>
              <h2 className="text-base font-bold text-white">Alur 60 Scene Video Anak (Full Percakapan English 10s Bersambung)</h2>
            </div>
            <p className="text-xs text-gray-400">
              Percakapan full 10 detik tanpa jeda kosong dalam bahasa Inggris + Objek mobil & karakter terkunci 100% konsisten
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {engineUsed && (
            <span className="text-xs font-medium px-2.5 py-1 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-300 flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>{engineUsed}</span>
            </span>
          )}
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Mobil & Karakter Terkunci Konsisten</span>
          </span>
        </div>
      </div>

      {/* Google Flow Connection Timeline */}
      <div className="relative space-y-6 before:absolute before:inset-0 before:left-5 before:w-0.5 before:bg-gradient-to-b before:from-amber-500 before:via-orange-500 before:to-emerald-500 before:hidden md:before:block">
        {scenes.map((scene, idx) => {
          const isCopiedPrompt = copiedPromptIndex === idx;
          const isCopiedDialogue = copiedDialogueIndex === idx;
          const isEditingPrompt = editingPromptIndex === idx;
          const isEditingDialogue = editingDialogueIndex === idx;
          const dialogueText = scene.english_dialogue || scene.dialogue;
          const wordCount = scene.word_count || dialogueText.split(/\s+/).filter(Boolean).length;

          return (
            <div
              key={scene.scene_index}
              className="relative pl-0 md:pl-12 group transition-all"
            >
              {/* Timeline Flow Node Dot */}
              <div className="hidden md:flex absolute left-3.5 top-6 -translate-x-1/2 w-4 h-4 rounded-full bg-[#16171c] border-2 border-amber-500 group-hover:border-emerald-400 group-hover:scale-125 transition-all z-10 items-center justify-center">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 group-hover:bg-emerald-300"></span>
              </div>

              {/* Scene Card */}
              <div className="rounded-xl bg-[#0f1013] border border-white/10 hover:border-amber-500/40 p-4 sm:p-5 transition-all shadow-md">
                {/* Scene Meta Bar */}
                <div className="flex flex-wrap items-center justify-between gap-2 pb-3 mb-3 border-b border-white/5">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="px-2.5 py-1 rounded-lg bg-amber-600/20 text-amber-300 border border-amber-500/30 text-xs font-mono font-bold flex items-center gap-1">
                      <Car className="w-3 h-3" />
                      SCENE {scene.scene_index.toString().padStart(2, '0')} / {scenes.length}
                    </span>
                    <span className="flex items-center gap-1 font-mono text-xs px-2.5 py-1 rounded-lg bg-white/5 text-gray-300 border border-white/10">
                      <Clock className="w-3 h-3 text-amber-400" />
                      {scene.time_range} (Full 10s Penuh)
                    </span>
                    <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-800/40">
                      🗣️ {wordCount} Words (No Dead Air)
                    </span>
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    <span className="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-md bg-purple-950/80 text-purple-300 border border-purple-800/40">
                      <Camera className="w-3 h-3 text-purple-400" />
                      {scene.camera_directive}
                    </span>

                    {/* Copy Dialogue Button */}
                    <button
                      type="button"
                      onClick={() => handleCopyDialogue(dialogueText, idx)}
                      className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
                        isCopiedDialogue
                          ? 'bg-emerald-600 text-white'
                          : 'bg-white/10 hover:bg-white/15 text-gray-200 border border-white/10'
                      }`}
                      title="Copy English Voiceover (untuk ElevenLabs / TTS)"
                    >
                      {isCopiedDialogue ? <Check className="w-3.5 h-3.5 text-emerald-200" /> : <Mic className="w-3.5 h-3.5 text-amber-400" />}
                      <span>{isCopiedDialogue ? 'Voice Tersalin!' : 'Copy Voiceover'}</span>
                    </button>

                    {/* Copy Video Prompt Button */}
                    <button
                      type="button"
                      onClick={() => handleCopyPrompt(scene.video_prompt, idx)}
                      className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                        isCopiedPrompt
                          ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/40'
                          : 'bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white'
                      }`}
                    >
                      {isCopiedPrompt ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{isCopiedPrompt ? 'Prompt Tersalin!' : 'Copy Video Prompt'}</span>
                    </button>
                  </div>
                </div>

                {/* Section 1: Full 10s Continuous English Speech & Sound Effects */}
                <div className="mb-3 space-y-2">
                  <div className="p-3.5 rounded-lg bg-gradient-to-r from-[#171922] to-[#121318] border border-amber-500/20">
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-1.5 text-amber-300 text-xs font-bold">
                        <Mic className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
                        <span>Percakapan Penuh 10 Detik (Continuous English Voiceover):</span>
                      </div>
                      <div className="flex items-center gap-2">
                        {scene.story_link && (
                          <span className="text-[10px] text-gray-400 font-mono hidden sm:inline flex items-center gap-1">
                            <Link className="w-3 h-3 text-amber-400" />
                            {scene.story_link}
                          </span>
                        )}
                        <button
                          type="button"
                          onClick={() => isEditingDialogue ? handleSaveEditDialogue(idx) : handleStartEditDialogue(idx, dialogueText)}
                          className="text-[10px] text-gray-400 hover:text-white flex items-center gap-0.5"
                        >
                          <Edit3 className="w-2.5 h-2.5" />
                          <span>{isEditingDialogue ? 'Simpan' : 'Edit'}</span>
                        </button>
                      </div>
                    </div>

                    {isEditingDialogue ? (
                      <div className="space-y-1.5">
                        <textarea
                          rows={2}
                          value={editDialogueText}
                          onChange={(e) => setEditDialogueText(e.target.value)}
                          className="w-full p-2 rounded-lg bg-black/60 border border-amber-500 text-xs text-amber-100 font-mono outline-none"
                        />
                        <div className="flex justify-end gap-1.5">
                          <button
                            type="button"
                            onClick={() => setEditingDialogueIndex(null)}
                            className="px-2 py-0.5 rounded bg-white/5 text-gray-300 text-[10px]"
                          >
                            Batal
                          </button>
                          <button
                            type="button"
                            onClick={() => handleSaveEditDialogue(idx)}
                            className="px-2.5 py-0.5 rounded bg-amber-600 text-white text-[10px] font-semibold"
                          >
                            Simpan Voiceover
                          </button>
                        </div>
                      </div>
                    ) : (
                      <p className="text-xs text-amber-100 font-medium leading-relaxed tracking-wide">
                        "{dialogueText}"
                      </p>
                    )}
                  </div>

                  {/* Sound Effects Audio Cue */}
                  <div className="p-2.5 rounded-lg bg-black/30 border border-white/5 flex items-center justify-between text-xs">
                    <span className="text-[11px] text-amber-300/90 font-mono flex items-center gap-1.5">
                      <Volume2 className="w-3.5 h-3.5 text-amber-400" />
                      <span>{scene.sound_effects || '[SFX: Vroom vroom engine rev, cheerful giggles]'}</span>
                    </span>
                    <span className="text-[10px] text-gray-500 font-mono">10s Audio Cue</span>
                  </div>
                </div>

                {/* Section 2: Visual Action & Object Consistency */}
                <div className="mb-3 grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 rounded-lg bg-[#141519] border border-white/5">
                    <span className="text-[10px] font-semibold text-purple-300 block mb-0.5">
                      🎬 Aksi Main Mobil (Satu Scene 10 Detik Penuh):
                    </span>
                    <p className="text-gray-300 text-[11px] leading-relaxed">
                      {scene.action_description}
                    </p>
                  </div>

                  <div className="p-2.5 rounded-lg bg-[#141519] border border-white/5 flex gap-2.5 items-start">
                    {referenceImage && (
                      <div className="w-12 h-12 rounded-lg overflow-hidden bg-black shrink-0 border border-white/10" title="Foto Mobil Mainan Terkunci">
                        <img src={referenceImage} alt="Ref" className="w-full h-full object-cover" />
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <span className="text-[10px] font-semibold text-emerald-300 block mb-0.5 flex items-center gap-1">
                        <ShieldCheck className="w-3 h-3" />
                        Kunci Objek Konsisten Tanpa Berubah Bentuk:
                      </span>
                      <p className="text-gray-300 text-[11px] leading-relaxed line-clamp-2">
                        <span className="text-amber-400 font-medium">Mobil:</span> {scene.anchors?.product} | <span className="text-blue-400 font-medium">Anak:</span> {scene.anchors?.subject}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Section 3: Natural Fluid AI Video Prompt */}
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] font-bold text-amber-400 flex items-center gap-1">
                      <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                      Prompt Sinematik Alami (Siap Masuk Google Veo / Kling AI / Runway):
                    </span>
                    <button
                      type="button"
                      onClick={() => isEditingPrompt ? handleSaveEditPrompt(idx) : handleStartEditPrompt(idx, scene.video_prompt)}
                      className="text-[11px] text-gray-400 hover:text-white flex items-center gap-1 transition-colors"
                    >
                      <Edit3 className="w-3 h-3" />
                      <span>{isEditingPrompt ? 'Simpan' : 'Edit Prompt'}</span>
                    </button>
                  </div>

                  {isEditingPrompt ? (
                    <div className="space-y-2">
                      <textarea
                        rows={3}
                        value={editPromptText}
                        onChange={(e) => setEditPromptText(e.target.value)}
                        className="w-full p-2.5 rounded-lg bg-black/60 border border-amber-500 text-xs text-gray-100 font-mono outline-none"
                      />
                      <div className="flex justify-end gap-2">
                        <button
                          type="button"
                          onClick={() => setEditingPromptIndex(null)}
                          className="px-2.5 py-1 rounded bg-white/5 text-gray-300 text-[11px]"
                        >
                          Batal
                        </button>
                        <button
                          type="button"
                          onClick={() => handleSaveEditPrompt(idx)}
                          className="px-3 py-1 rounded bg-amber-600 text-white text-[11px] font-semibold"
                        >
                          Simpan Perubahan
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div
                      onClick={() => handleCopyPrompt(scene.video_prompt, idx)}
                      className="p-3 rounded-lg bg-black/40 border border-white/10 hover:border-amber-500/50 cursor-pointer text-xs font-mono text-gray-200 leading-relaxed break-words transition-all group/code"
                      title="Klik untuk langsung copy prompt video"
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
