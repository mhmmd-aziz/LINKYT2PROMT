import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { UrlInputNode } from './components/UrlInputNode';
import { ImageUploadNode } from './components/ImageUploadNode';
import { ConsistencyNode } from './components/ConsistencyNode';
import { TranscriptNode } from './components/TranscriptNode';
import { SceneFlowNode } from './components/SceneFlowNode';
import { YouTubePackageNode } from './components/YouTubePackageNode';
import { ExportModal } from './components/ExportModal';
import { LlmApiKeyModal } from './components/LlmApiKeyModal';
import {
  HardwareInfo,
  VideoMetadata,
  TranscriptItem,
  ScenePromptItem,
  SceneAnchors,
  ImageAnalysisResult,
  KidsVideoVision,
  YouTubePackage
} from './types';
import { ArrowDown, Sparkles, Car } from 'lucide-react';

export const App: React.FC = () => {
  // Hardware state
  const [hardware, setHardware] = useState<HardwareInfo | null>(null);
  const [hardwareLoading, setHardwareLoading] = useState<boolean>(true);
  const [selectedDevice, setSelectedDevice] = useState<'cuda' | 'cpu'>('cuda');

  // AI LLM Engine & API Token state (DeepSeek-V4.1-Flash default)
  const [apiToken, setApiToken] = useState<string>(() => {
    return localStorage.getItem('imzy_llm_token') || localStorage.getItem('imsy_llm_token') || localStorage.getItem('imsy_gemini_api_key') || '';
  });
  const [llmProvider, setLlmProvider] = useState<string>(() => {
    return localStorage.getItem('imzy_llm_provider') || localStorage.getItem('imsy_llm_provider') || 'huggingface_deepseek';
  });
  const [apiKeyModalOpen, setApiKeyModalOpen] = useState<boolean>(false);
  const [engineUsed, setEngineUsed] = useState<string>('Smart Kids Director Engine');

  // Video & Extraction state
  const [url, setUrl] = useState<string>('');
  const [extractLoading, setExtractLoading] = useState<boolean>(false);
  const [extractError, setExtractError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<VideoMetadata | null>(null);
  const [videoVision, setVideoVision] = useState<KidsVideoVision | null>(null);
  const [transcriptItems, setTranscriptItems] = useState<TranscriptItem[]>([]);
  const [fullTranscriptText, setFullTranscriptText] = useState<string>('');
  const [detectedLanguage, setDetectedLanguage] = useState<string>('en');

  // Image Upload & Vision state (1 Foto Mainan Mobil / Tokoh)
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageAnalysis, setImageAnalysis] = useState<ImageAnalysisResult | null>(null);

  // Consistency & Scene Generator state
  const [sceneDuration, setSceneDuration] = useState<number>(10); // Exactly 10s as requested
  const [language, setLanguage] = useState<string>('en'); // Always English dialogue as requested
  const [anchors, setAnchors] = useState<SceneAnchors>({
    subject: 'Cheerful 4-year-old toddler with neat brown hair wearing a bright blue and orange striped shirt, beaming with a happy energetic smile',
    product: 'Gleaming crimson red stunt monster truck with bright yellow flame decals, oversized rugged off-road tires, and rounded cartoon headlights in 3D Pixar style',
    setting: 'Sunlit kids playroom track featuring vibrant orange looping ramps, mini wooden suspension bridges, and colorful stacking blocks',
    style: 'Cinematic 3D Pixar animation aesthetic, 8K ultra-vibrant saturated colors, warm soft playroom lighting, realistic glossy toy textures, 24fps smooth motion'
  });

  // Generated Scenes (Max 20 Scenes) & Viral YouTube Kit
  const [generating, setGenerating] = useState<boolean>(false);
  const [scenes, setScenes] = useState<ScenePromptItem[]>([]);
  const [youtubePackage, setYoutubePackage] = useState<YouTubePackage | null>(null);
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

  // Handle YouTube URL Extraction (Does NOT auto-generate prompts! Clears previous output)
  const handleExtract = async (overrideUrl?: string) => {
    const targetUrl = overrideUrl || url;
    if (!targetUrl.trim()) return;

    setExtractLoading(true);
    setExtractError(null);
    setScenes([]); // Clear old scenes so user doesn't see old prompt
    setYoutubePackage(null); // Clear old YouTube kit

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
      setDetectedLanguage(data.language || 'en');
      setLanguage('en'); // Always English dialogue generation

      // Update default arena if vision detected specific kids theme
      if (data.video_vision) {
        setAnchors((prev) => ({
          ...prev,
          product: imageAnalysis ? (imageAnalysis.recommended_anchor_product || imageAnalysis.product_name) : (prev.product.includes('monster truck') ? (data.video_vision.default_car || prev.product) : prev.product),
          setting: data.video_vision.default_arena || prev.setting
        }));
      }

      // DO NOT auto-generate prompts here! User must upload/confirm image and click generate button.
    } catch (err: any) {
      setExtractError(err.message || 'Terjadi kesalahan saat memproses URL.');
    } finally {
      setExtractLoading(false);
    }
  };

  // Apply Image Analysis to Anchors (Locks photo anchors; does not prematurely generate)
  const handleApplyImageAnchors = (analysis: ImageAnalysisResult) => {
    setImageAnalysis(analysis);
    setAnchors((prev) => ({
      ...prev,
      product: analysis.recommended_anchor_product || analysis.product_name,
      subject: analysis.recommended_anchor_subject || prev.subject,
      setting: analysis.recommended_setting || prev.setting
    }));
    // Note: Do not auto-generate immediately. Let user review and click the action button.
  };

  // Trigger Prompt Generation (Max 60 Scenes combining YouTube Vision + Image Context)
  const triggerGenerate = async (
    items = transcriptItems,
    meta = metadata,
    lang = 'en',
    currentImageAnalysis = imageAnalysis
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
          language: 'en', // Strict English dialogue generation
          custom_subject: anchors.subject,
          custom_product: anchors.product,
          custom_setting: anchors.setting,
          custom_style: anchors.style,
          image_context: currentImageAnalysis || undefined,
          api_token: apiToken || undefined,
          provider: llmProvider || undefined
        })
      });

      const json = await res.json();
      if (!res.ok) {
        throw new Error(json.detail || 'Gagal membuat prompt konsisten.');
      }

      setScenes(json.scenes || []);
      if (json.youtube_package) {
        setYoutubePackage(json.youtube_package);
      }
      if (json.video_vision) {
        setVideoVision(json.video_vision);
      }
      setEngineUsed(json.engine_used || (apiToken ? 'DeepSeek-V4.1-Flash AI' : 'Smart Kids Director Engine'));
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

  const handleUpdateSceneDialogue = (index: number, newDialogue: string) => {
    setScenes((prev) => {
      const copy = [...prev];
      if (copy[index]) {
        copy[index] = {
          ...copy[index],
          dialogue: newDialogue,
          english_dialogue: newDialogue,
          word_count: newDialogue.split(/\s+/).filter(Boolean).length
        };
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
        apiToken={apiToken}
        provider={llmProvider}
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
            <span>DeepSeek-V4.1-Flash • Continuous 10s English Storyboard</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            Video YouTube Anak ➔ 20 Scene Percakapan English Full 10s Bersambung
          </h2>
          <p className="text-xs sm:text-sm text-gray-400 max-w-2xl mx-auto leading-relaxed">
            Satu scene <span className="text-emerald-400 font-semibold">full 10 detik percakapan English tanpa jeda kosong</span> dan <span className="text-amber-400 font-semibold">alur bersambung di setiap scene</span>. Objek mobil mainan & tokoh anak dikunci 100% konsisten tanpa morphing!
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
            geminiApiKey={apiToken}
          />

          {/* Flow Connector Arrow */}
          <div className="flex justify-center my-4">
            <div className="w-8 h-8 rounded-full bg-[#18191e] border border-white/15 flex items-center justify-center text-purple-400 shadow-md">
              <ArrowDown className="w-4 h-4" />
            </div>
          </div>
        </div>

        {/* COMBINED ACTION CTA: Analisis Video YT + Foto Mainan & Buat 20 Scene Prompt Konsisten */}
        {metadata && (
          <div className="relative p-5 sm:p-6 rounded-2xl bg-gradient-to-r from-[#1b1510] via-[#1c1412] to-[#17121b] border-2 border-amber-500/40 shadow-2xl flex flex-col sm:flex-row items-center justify-between gap-4 animate-in fade-in duration-200">
            <div className="space-y-1.5 flex-1">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
                <span className="text-xs font-bold text-amber-300 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  {imagePreview ? '🎯 Siap Analisis: Video YouTube + Foto Mainan Terhubung!' : '💡 Langkah Berikutnya: Upload Foto Mainan Mobil'}
                </span>
              </div>
              <p className="text-sm font-bold text-white leading-snug">
                {imagePreview
                  ? `Mobil Mainan "${imageAnalysis?.product_name || 'Foto Terdeteksi'}" diselaraskan ke alur video "${metadata.title.slice(0, 50)}..."`
                  : 'Upload 1 foto mobil mainan di Node 02 di atas agar model dan warna mobilmu terkunci 100% konsisten di seluruh 20 scene.'}
              </p>
              <p className="text-xs text-gray-400 leading-relaxed">
                Menghasilkan alur 20 scene bersambung dengan <span className="text-emerald-400 font-semibold">percakapan English full 10 detik tanpa jeda kosong</span> dan tombol salin prompt siap pakai untuk Google Flow / Veo / Kling.
              </p>
            </div>

            <button
              type="button"
              disabled={generating}
              onClick={() => triggerGenerate()}
              className="w-full sm:w-auto shrink-0 flex items-center justify-center gap-2.5 px-6 py-4 rounded-xl bg-gradient-to-r from-amber-500 via-orange-500 to-red-600 hover:from-amber-400 hover:to-red-500 text-white font-extrabold text-sm shadow-xl shadow-amber-900/50 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50"
            >
              {generating ? (
                <>
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Menganalisis & Menyusun 20 Scene...</span>
                </>
              ) : (
                <>
                  <Car className="w-4 h-4 text-white" />
                  <span>{imagePreview ? '🚀 Analisis Video + Foto & Buat 20 Scene AI Prompt' : '🚀 Buat 20 Scene AI Prompt Konsisten'}</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* FLOW NODE 03: Consistency & 10s Scene Controls (Max 20 Scenes) */}
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

        {/* FLOW NODE: Viral YouTube Kit (Judul FYP, Deskripsi SEO & AI Thumbnail Gemini Prompt) */}
        {youtubePackage && (
          <div className="relative">
            <YouTubePackageNode
              packageData={youtubePackage}
              referenceImage={imagePreview}
            />

            {/* Flow Connector Arrow */}
            <div className="flex justify-center my-4">
              <div className="w-8 h-8 rounded-full bg-[#18191e] border border-white/15 flex items-center justify-center text-red-400 shadow-md">
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
              onUpdateSceneDialogue={handleUpdateSceneDialogue}
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
        youtubePackage={youtubePackage}
      />

      {/* DeepSeek / HuggingFace LLM Key & Engine Modal */}
      <LlmApiKeyModal
        isOpen={apiKeyModalOpen}
        onClose={() => setApiKeyModalOpen(false)}
        apiToken={apiToken}
        setApiToken={setApiToken}
        provider={llmProvider}
        setProvider={setLlmProvider}
        engineStatus={
          apiToken
            ? llmProvider === 'huggingface_deepseek'
              ? 'DeepSeek-V4.1-Flash (Hugging Face)'
              : llmProvider === 'deepseek_official'
              ? 'DeepSeek Official API'
              : 'Google Gemini 1.5 Flash'
            : 'Smart Kids Director Engine (Dynamic Local Mode)'
        }
      />

      {/* Footer */}
      <footer className="border-t border-white/10 bg-[#0c0d10] py-6 px-4 text-center text-xs text-gray-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-gray-400">imzy tools yt</span>
            <span>•</span>
            <span>Full 10s Continuous English Speech & Story Flow</span>
          </div>
          <div className="flex items-center gap-4 text-gray-400 text-[11px]">
            <span>Full 10s Spoken English</span>
            <span>•</span>
            <span>Zero Dead Air</span>
            <span>•</span>
            <span>Toy Car Continuity Lock</span>
            <span>•</span>
            <span>RTX 3050 CUDA</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
