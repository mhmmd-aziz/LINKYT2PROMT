import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { UrlInputNode } from './components/UrlInputNode';
import { ImageUploadNode } from './components/ImageUploadNode';
import { ConsistencyNode } from './components/ConsistencyNode';
import { TranscriptNode } from './components/TranscriptNode';
import { SceneFlowNode } from './components/SceneFlowNode';
import { ExportModal } from './components/ExportModal';
import { GeminiApiKeyModal } from './components/GeminiApiKeyModal';
import {
  HardwareInfo,
  VideoMetadata,
  TranscriptItem,
  ScenePromptItem,
  SceneAnchors,
  ImageAnalysisResult,
  KidsVideoVision
} from './types';
import { ArrowDown, Sparkles, Car } from 'lucide-react';

export const App: React.FC = () => {
  // Hardware state
  const [hardware, setHardware] = useState<HardwareInfo | null>(null);
  const [hardwareLoading, setHardwareLoading] = useState<boolean>(true);
  const [selectedDevice, setSelectedDevice] = useState<'cuda' | 'cpu'>('cuda');

  // AI Engine & API Key state
  const [geminiApiKey, setGeminiApiKey] = useState<string>(() => {
    return localStorage.getItem('imsy_gemini_api_key') || '';
  });
  const [apiKeyModalOpen, setApiKeyModalOpen] = useState<boolean>(false);
  const [engineUsed, setEngineUsed] = useState<string>('Smart Local Kids Director Engine');

  // Video & Extraction state
  const [url, setUrl] = useState<string>('');
  const [extractLoading, setExtractLoading] = useState<boolean>(false);
  const [extractError, setExtractError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<VideoMetadata | null>(null);
  const [videoVision, setVideoVision] = useState<KidsVideoVision | null>(null);
  const [transcriptItems, setTranscriptItems] = useState<TranscriptItem[]>([]);
  const [fullTranscriptText, setFullTranscriptText] = useState<string>('');
  const [detectedLanguage, setDetectedLanguage] = useState<string>('id');

  // Image Upload & Vision state (1 Foto Mainan Mobil / Tokoh)
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageAnalysis, setImageAnalysis] = useState<ImageAnalysisResult | null>(null);

  // Consistency & Scene Generator state
  const [sceneDuration, setSceneDuration] = useState<number>(10); // Exactly 10s as requested
  const [language, setLanguage] = useState<string>('id');
  const [anchors, setAnchors] = useState<SceneAnchors>({
    subject: 'Anak kecil laki-laki usia 4 tahun berambut cokelat rapi mengenakan kaos garis biru-oranye ceria, wajah riang tersenyum gembira',
    product: 'Mainan mobil monster truck anak warna merah menyala dengan strip kuning cerah, ban off-road besar bergerigi hitam, bodi 3D Pixar mengkilap',
    setting: 'Kamar bermain anak yang terang dan ceria dengan lintasan balap melingkar warna oranye, jembatan kayu mini, dan balok susun',
    style: 'Gaya animasi 3D Pixar/Disney bertekstur ultra-realistis, warna jenuh sangat cerah (vibrant saturated), pencahayaan hangat ramah anak, gerakan halus 24fps'
  });

  // Generated Scenes (Max 60 Scenes)
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
      setVideoVision(data.video_vision || null);
      setTranscriptItems(data.items || []);
      setFullTranscriptText(data.full_text || '');
      setDetectedLanguage(data.language || 'id');
      setLanguage(data.language === 'en' ? 'en' : 'id');

      // Update default car and arena anchors if vision detected specific kids theme
      if (data.video_vision) {
        setAnchors((prev) => ({
          ...prev,
          product: prev.product.includes('monster truck') ? (data.video_vision.default_car || prev.product) : prev.product,
          setting: data.video_vision.default_arena || prev.setting
        }));
      }

      // Auto generate scenes immediately
      triggerGenerate(data.items, data.metadata, data.language);
    } catch (err: any) {
      setExtractError(err.message || 'Terjadi kesalahan saat memproses URL.');
    } finally {
      setExtractLoading(false);
    }
  };

  // Apply Image Analysis to Anchors
  const handleApplyImageAnchors = (analysis: ImageAnalysisResult) => {
    setAnchors((prev) => ({
      ...prev,
      product: analysis.recommended_anchor_product || analysis.product_name,
      subject: analysis.recommended_anchor_subject || prev.subject,
      setting: analysis.recommended_setting || prev.setting
    }));
  };

  // Trigger Prompt Generation (Max 60 Scenes)
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
          custom_style: anchors.style,
          image_context: imageAnalysis || undefined,
          gemini_api_key: geminiApiKey || undefined
        })
      });

      const json = await res.json();
      if (!res.ok) {
        throw new Error(json.detail || 'Gagal membuat prompt konsisten.');
      }

      setScenes(json.scenes || []);
      if (json.video_vision) {
        setVideoVision(json.video_vision);
      }
      setEngineUsed(json.engine_used || (geminiApiKey ? 'Google Gemini 1.5 Flash Vision' : 'Smart Local Kids Director'));
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
    <div className="min-h-screen bg-[#0a0b0d] text-gray-100 flex flex-col font-sans selection:bg-amber-600 selection:text-white">
      {/* Sticky Google Flow Header */}
      <Header
        hardware={hardware}
        hardwareLoading={hardwareLoading}
        selectedDevice={selectedDevice}
        onDeviceChange={setSelectedDevice}
        geminiApiKey={geminiApiKey}
        onOpenApiKeyModal={() => setApiKeyModalOpen(true)}
        onOpenExport={() => setExportModalOpen(true)}
        totalScenes={scenes.length}
      />

      {/* Main Flow Canvas */}
      <main className="flex-1 max-w-5xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8 google-flow-grid">
        {/* Intro Hero Banner */}
        <div className="text-center space-y-2 py-4">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-semibold">
            <Car className="w-3.5 h-3.5" />
            <span>Google Flow Visual Pipeline • Kids YouTube Remake AI</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            Video YouTube Anak ➔ 60 Scene AI Video Prompts Konsisten
          </h2>
          <p className="text-xs sm:text-sm text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Copas link video YouTube anak (lagi main mobil, monster truck, sound effects ceria) + Upload 1 foto mainan. Sistem membaca visi cerita dan menyusun ulang ke <span className="text-amber-400 font-medium">versi 60 scene konsisten</span> siap render ke video AI!
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
            videoVision={videoVision}
            error={extractError}
          />

          {/* Flow Connector Arrow */}
          <div className="flex justify-center my-4">
            <div className="w-8 h-8 rounded-full bg-[#18191e] border border-white/15 flex items-center justify-center text-amber-400 shadow-md">
              <ArrowDown className="w-4 h-4 animate-bounce" />
            </div>
          </div>
        </div>

        {/* FLOW NODE 02: Upload 1 Foto Mainan Mobil / Karakter Konsisten */}
        <div className="relative">
          <ImageUploadNode
            imagePreview={imagePreview}
            setImagePreview={setImagePreview}
            imageAnalysis={imageAnalysis}
            setImageAnalysis={setImageAnalysis}
            onApplyAnchors={handleApplyImageAnchors}
            geminiApiKey={geminiApiKey}
          />

          {/* Flow Connector Arrow */}
          <div className="flex justify-center my-4">
            <div className="w-8 h-8 rounded-full bg-[#18191e] border border-white/15 flex items-center justify-center text-purple-400 shadow-md">
              <ArrowDown className="w-4 h-4" />
            </div>
          </div>
        </div>

        {/* FLOW NODE 03: Consistency & 10s Scene Controls (Max 60 Scenes) */}
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
            hasUploadedImage={Boolean(imagePreview)}
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

        {/* FLOW NODE 04: Full Conversation Transcript */}
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

        {/* FINAL FLOW NODE: Scenes Prompt-to-Video Matrix */}
        {scenes.length > 0 && (
          <div className="relative">
            <SceneFlowNode
              scenes={scenes}
              referenceImage={imagePreview}
              engineUsed={engineUsed}
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

      {/* Gemini API Key & Engine Modal */}
      <GeminiApiKeyModal
        isOpen={apiKeyModalOpen}
        onClose={() => setApiKeyModalOpen(false)}
        geminiApiKey={geminiApiKey}
        setGeminiApiKey={setGeminiApiKey}
        engineStatus={geminiApiKey ? 'Google Gemini 1.5 Flash Vision AI' : 'Smart Local Kids Director Engine (Free/Offline)'}
      />

      {/* Footer */}
      <footer className="border-t border-white/10 bg-[#0c0d10] py-6 px-4 text-center text-xs text-gray-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-gray-400">imsy tools yt</span>
            <span>•</span>
            <span>Kids YouTube Remake AI (60 Scene Architecture)</span>
          </div>
          <div className="flex items-center gap-4 text-gray-400 text-[11px]">
            <span>10s Per Scene</span>
            <span>•</span>
            <span>Toy Car & Character Lock</span>
            <span>•</span>
            <span>Cheerful Sound Effects</span>
            <span>•</span>
            <span>GPU Accelerated (RTX 3050 CUDA)</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
