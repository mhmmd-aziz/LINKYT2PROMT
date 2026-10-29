import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { UrlInputNode } from './components/UrlInputNode';
import { ConsistencyNode } from './components/ConsistencyNode';
import { TranscriptNode } from './components/TranscriptNode';
import { SceneFlowNode } from './components/SceneFlowNode';
import { ExportModal } from './components/ExportModal';
import {
  HardwareInfo,
  VideoMetadata,
  TranscriptItem,
  ScenePromptItem,
  SceneAnchors
} from './types';
import { ArrowDown, Cpu, Zap, Layers, Sparkles } from 'lucide-react';

export const App: React.FC = () => {
  // Hardware state
  const [hardware, setHardware] = useState<HardwareInfo | null>(null);
  const [hardwareLoading, setHardwareLoading] = useState<boolean>(true);
  const [selectedDevice, setSelectedDevice] = useState<'cuda' | 'cpu'>('cuda');

  // Video & Extraction state
  const [url, setUrl] = useState<string>('');
  const [extractLoading, setExtractLoading] = useState<boolean>(false);
  const [extractError, setExtractError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<VideoMetadata | null>(null);
  const [transcriptItems, setTranscriptItems] = useState<TranscriptItem[]>([]);
  const [fullTranscriptText, setFullTranscriptText] = useState<string>('');
  const [detectedLanguage, setDetectedLanguage] = useState<string>('id');

  // Consistency & Scene Generator state
  const [sceneDuration, setSceneDuration] = useState<number>(10); // Fixed 10s as user requested
  const [language, setLanguage] = useState<string>('id');
  const [anchors, setAnchors] = useState<SceneAnchors>({
    subject: 'Kreator affiliasi pria/wanita muda Indonesia usia 25 tahun, mengenakan kaos polo kasual modern rapi, ramah dan antusias',
    product: 'Produk rekomendasi affiliasi unggulan berdesain modern elegan, bersih dan berkelas',
    setting: 'Studio minimalis modern dengan aksen kayu akustik dan pencahayaan studio hangat bokeh',
    style: 'Kualitas sinematik 8K, foto-realistis, pencahayaan komersial studio profesional, karakter wajah & pakaian 100% konsisten antar scene, 24fps'
  });

  // Generated Scenes
  const [generating, setGenerating] = useState<boolean>(false);
  const [scenes, setScenes] = useState<ScenePromptItem[]>([]);
  const [exportModalOpen, setExportModalOpen] = useState<boolean>(false);

  // Fetch hardware on mount
  useEffect(() => {
    const fetchHardware = async () => {
      try {
        setHardwareLoading(true);
        const res = await fetch('/api/hardware');
        if (res.ok) {
          const data: HardwareInfo = await res.json();
          setHardware(data);
          setSelectedDevice(data.recommended_device || 'cuda');
        }
      } catch (err) {
        console.warn('Hardware fetch error, falling back to local defaults:', err);
      } finally {
        setHardwareLoading(false);
      }
    };
    fetchHardware();
  }, []);

  // Handle YouTube URL Extraction
  const handleExtract = async (overrideUrl?: string) => {
    const targetUrl = overrideUrl || url;
    if (!targetUrl.trim()) return;

    setExtractLoading(true);
    setExtractError(null);

    try {
      const res = await fetch('/api/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: targetUrl.trim(),
          prefer_device: selectedDevice
        })
      });

      const json = await res.json();
      if (!res.ok) {
        throw new Error(json.detail || 'Gagal mengekstrak transkrip YouTube.');
      }

      const data = json.data;
      setMetadata(data.metadata);
      setTranscriptItems(data.items || []);
      setFullTranscriptText(data.full_text || '');
      setDetectedLanguage(data.language || 'id');
      setLanguage(data.language === 'en' ? 'en' : 'id');

      // Auto generate scenes immediately for smooth Google Flow UX
      triggerGenerate(data.items, data.metadata, data.language);
    } catch (err: any) {
      setExtractError(err.message || 'Terjadi kesalahan saat memproses URL.');
    } finally {
      setExtractLoading(false);
    }
  };

  // Trigger Prompt Generation
  const triggerGenerate = async (
    items = transcriptItems,
    meta = metadata,
    lang = language
  ) => {
    if (!meta) return;

    setGenerating(true);
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          metadata: meta,
          transcript_items: items,
          duration: meta.duration || (items.length ? items[items.length - 1].end : 60),
          scene_duration: sceneDuration,
          language: lang,
          custom_subject: anchors.subject,
          custom_product: anchors.product,
          custom_setting: anchors.setting,
          custom_style: anchors.style
        })
      });

      const json = await res.json();
      if (!res.ok) {
        throw new Error(json.detail || 'Gagal membuat prompt konsisten.');
      }

      setScenes(json.scenes || []);
      if (json.anchors) {
        setAnchors((prev) => ({
          ...prev,
          ...json.anchors
        }));
      }
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const handleUpdateScenePrompt = (index: number, newPrompt: string) => {
    setScenes((prev) => {
      const copy = [...prev];
      if (copy[index]) {
        copy[index] = { ...copy[index], video_prompt: newPrompt };
      }
      return copy;
    });
  };

  return (
    <div className="min-h-screen bg-[#0a0b0d] text-gray-100 flex flex-col font-sans selection:bg-blue-600 selection:text-white">
      {/* Sticky Google Flow Header */}
      <Header
        hardware={hardware}
        hardwareLoading={hardwareLoading}
        selectedDevice={selectedDevice}
        onDeviceChange={setSelectedDevice}
        onOpenExport={() => setExportModalOpen(true)}
        totalScenes={scenes.length}
      />

      {/* Main Flow Canvas */}
      <main className="flex-1 max-w-5xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8 google-flow-grid">
        {/* Intro Hero Banner */}
        <div className="text-center space-y-2 py-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>Google Flow Visual Pipeline • Affiliate Video AI</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            YouTube Transcript ➔ Alur Prompt Video 10 Detik
          </h2>
          <p className="text-xs sm:text-sm text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Cukup copas link YouTube. Sistem otomatis membaca seluruh percakapan, membagi per 10 detik penuh, dan menyusun prompt video AI dengan <span className="text-emerald-400 font-medium">objek & tokoh 100% konsisten</span>.
          </p>
        </div>

        {/* FLOW NODE 01: YouTube URL Input */}
        <div className="relative">
          <UrlInputNode
            url={url}
            setUrl={setUrl}
            loading={extractLoading}
            onExtract={handleExtract}
            metadata={metadata}
            error={extractError}
          />

          {/* Flow Connector Arrow */}
          <div className="flex justify-center my-4">
            <div className="w-8 h-8 rounded-full bg-[#18191e] border border-white/15 flex items-center justify-center text-blue-400 shadow-md">
              <ArrowDown className="w-4 h-4 animate-bounce" />
            </div>
          </div>
        </div>

        {/* FLOW NODE 02: Consistency & 10s Scene Controls */}
        <div className="relative">
          <ConsistencyNode
            duration={metadata?.duration || 0}
            sceneDuration={sceneDuration}
            setSceneDuration={setSceneDuration}
            language={language}
            setLanguage={setLanguage}
            anchors={anchors}
            setAnchors={setAnchors}
            onGenerate={() => triggerGenerate()}
            generating={generating}
            disabled={!metadata}
          />

          {/* Flow Connector Arrow */}
          {transcriptItems.length > 0 && (
            <div className="flex justify-center my-4">
              <div className="w-8 h-8 rounded-full bg-[#18191e] border border-white/15 flex items-center justify-center text-emerald-400 shadow-md">
                <ArrowDown className="w-4 h-4" />
              </div>
            </div>
          )}
        </div>

        {/* FLOW NODE 03: Full Conversation Transcript */}
        {transcriptItems.length > 0 && (
          <div className="relative">
            <TranscriptNode
              items={transcriptItems}
              fullText={fullTranscriptText}
              language={detectedLanguage}
              totalSegments={transcriptItems.length}
            />

            {/* Flow Connector Arrow */}
            <div className="flex justify-center my-4">
              <div className="w-8 h-8 rounded-full bg-[#18191e] border border-white/15 flex items-center justify-center text-purple-400 shadow-md">
                <ArrowDown className="w-4 h-4" />
              </div>
            </div>
          </div>
        )}

        {/* FLOW NODE 04: Scenes Prompt-to-Video Matrix */}
        {scenes.length > 0 && (
          <div className="relative">
            <SceneFlowNode
              scenes={scenes}
              onUpdateScenePrompt={handleUpdateScenePrompt}
            />
          </div>
        )}
      </main>

      {/* Export Modal */}
      <ExportModal
        isOpen={exportModalOpen}
        onClose={() => setExportModalOpen(false)}
        scenes={scenes}
        metadata={metadata}
      />

      {/* Footer */}
      <footer className="border-t border-white/10 bg-[#0c0d10] py-6 px-4 text-center text-xs text-gray-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-gray-400">imzy affilate</span>
            <span>•</span>
            <span>Google Flow Video AI Architecture</span>
          </div>
          <div className="flex items-center gap-4 text-gray-400 text-[11px]">
            <span>10s Per Scene</span>
            <span>•</span>
            <span>Object Continuity Lock</span>
            <span>•</span>
            <span>GPU Accelerated (CUDA)</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;

