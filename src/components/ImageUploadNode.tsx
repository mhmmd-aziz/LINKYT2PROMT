import React, { useRef, useState } from 'react';
import { ImageAnalysisResult } from '../types';
import { Image as ImageIcon, UploadCloud, Trash2, Sparkles, Check, Tag, Eye, Info, RefreshCw } from 'lucide-react';

interface ImageUploadNodeProps {
  imagePreview: string | null;
  setImagePreview: (img: string | null) => void;
  imageAnalysis: ImageAnalysisResult | null;
  setImageAnalysis: (analysis: ImageAnalysisResult | null) => void;
  onApplyAnchors: (analysis: ImageAnalysisResult) => void;
  geminiApiKey: string;
}

export const ImageUploadNode: React.FC<ImageUploadNodeProps> = ({
  imagePreview,
  setImagePreview,
  imageAnalysis,
  setImageAnalysis,
  onApplyAnchors,
  geminiApiKey
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [applied, setApplied] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const processFile = (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Harap pilih file gambar (JPG, PNG, WebP).');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      const b64 = e.target?.result as string;
      setImagePreview(b64);
      triggerAnalysis(b64);
    };
    reader.readAsDataURL(file);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      processFile(file);
    }
  };

  const triggerAnalysis = async (b64: string) => {
    setAnalyzing(true);
    setApplied(false);
    try {
      const res = await fetch('/api/analyze-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image_base64: b64,
          gemini_api_key: geminiApiKey || undefined
        })
      });
      const data = await res.json();
      if (res.ok && data.analysis) {
        setImageAnalysis(data.analysis);
      }
    } catch (err) {
      console.error('Image analysis error:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleApply = () => {
    if (imageAnalysis) {
      onApplyAnchors(imageAnalysis);
      setApplied(true);
      setTimeout(() => setApplied(false), 2500);
    }
  };

  const handleRemove = () => {
    setImagePreview(null);
    setImageAnalysis(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="relative rounded-2xl bg-[#16171c] border border-white/10 p-5 sm:p-6 shadow-xl transition-all">
      {/* Node Header */}
      <div className="flex flex-wrap items-center justify-between pb-4 mb-5 border-b border-white/10 gap-2">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <ImageIcon className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-gray-400 border border-white/10">
                NODE 02
              </span>
              <h2 className="text-base font-bold text-white">Upload 1 Foto Produk / Objek Konsisten</h2>
            </div>
            <p className="text-xs text-gray-400">
              Upload 1 foto referensi produk affiliasi atau subjek yang ingin dijadikan objek konsisten di video
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {imageAnalysis && (
            <span className="text-[11px] font-medium px-2.5 py-1 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 flex items-center gap-1">
              <Eye className="w-3.5 h-3.5 text-purple-400" />
              <span>Foto Berhasil Dianalisis</span>
            </span>
          )}
        </div>
      </div>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        className="hidden"
      />

      {/* Upload & Analysis Container */}
      {!imagePreview ? (
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center gap-3 ${
            dragOver
              ? 'border-purple-500 bg-purple-500/10'
              : 'border-white/15 bg-[#0f1013] hover:border-purple-500/50 hover:bg-white/[0.02]'
          }`}
        >
          <div className="w-12 h-12 rounded-2xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
            <UploadCloud className="w-6 h-6" />
          </div>
          <div>
            <p className="text-sm font-semibold text-white">
              Klik untuk upload atau drag & drop <span className="text-purple-400">1 foto produk</span>
            </p>
            <p className="text-xs text-gray-400 mt-1">
              Format JPG, PNG, atau WebP (Foto produk affiliasi, packaging, atau tokoh)
            </p>
          </div>
          <span className="text-[11px] px-3 py-1 rounded-full bg-white/5 border border-white/10 text-gray-300">
            📸 Sistem otomatis menganalisis isi foto & mengunci objek di setiap scene
          </span>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 rounded-xl bg-[#0f1013] border border-white/10">
            {/* Image Preview Box */}
            <div className="relative group rounded-xl overflow-hidden bg-black/60 border border-white/10 aspect-square max-h-56 flex items-center justify-center">
              <img
                src={imagePreview}
                alt="Foto Produk Affiliasi"
                className="w-full h-full object-contain"
              />
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="p-2 rounded-lg bg-white/20 hover:bg-white/30 text-white text-xs flex items-center gap-1 backdrop-blur-sm"
                  title="Ganti Foto"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Ganti</span>
                </button>
                <button
                  type="button"
                  onClick={handleRemove}
                  className="p-2 rounded-lg bg-red-600/80 hover:bg-red-600 text-white text-xs flex items-center gap-1 backdrop-blur-sm"
                  title="Hapus Foto"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Hapus</span>
                </button>
              </div>
            </div>

            {/* Analysis Result Box (Bisa Dilihat Tentang Apa) */}
            <div className="md:col-span-2 flex flex-col justify-between space-y-3">
              <div>
                <div className="flex items-center justify-between pb-2 mb-2 border-b border-white/5">
                  <span className="text-xs font-bold uppercase tracking-wider text-purple-400 flex items-center gap-1.5">
                    <Eye className="w-3.5 h-3.5" />
                    Bisa Dilihat Tentang Apa (Hasil Analisis Foto):
                  </span>
                  {analyzing ? (
                    <span className="text-[11px] text-amber-400 flex items-center gap-1 animate-pulse">
                      <RefreshCw className="w-3 h-3 animate-spin" />
                      Menganalisis Foto...
                    </span>
                  ) : (
                    <span className="text-[10px] text-gray-500 font-mono">
                      {imageAnalysis?.source || 'Vision Engine'}
                    </span>
                  )}
                </div>

                {imageAnalysis ? (
                  <div className="space-y-2 text-xs">
                    <div>
                      <span className="text-gray-400 font-medium">Nama Objek / Produk:</span>{' '}
                      <span className="font-bold text-white text-sm">{imageAnalysis.product_name}</span>
                    </div>

                    <div className="flex flex-wrap items-center gap-2">
                      <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30 text-[11px] font-medium flex items-center gap-1">
                        <Tag className="w-3 h-3" />
                        {imageAnalysis.category}
                      </span>
                      {imageAnalysis.detected_text && (
                        <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[11px] font-mono">
                          Merek/Teks: {imageAnalysis.detected_text}
                        </span>
                      )}
                    </div>

                    <div>
                      <span className="text-gray-400 font-medium block">Detail Visual & Ciri Khas:</span>
                      <p className="text-gray-300 leading-relaxed text-[11px] mt-0.5 p-2 rounded-lg bg-black/40 border border-white/5">
                        {imageAnalysis.visual_description}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="py-6 text-center text-xs text-gray-500">
                    Menunggu hasil deteksi visual foto...
                  </div>
                )}
              </div>

              {/* Apply Button */}
              {imageAnalysis && (
                <div className="pt-2 flex justify-end">
                  <button
                    type="button"
                    onClick={handleApply}
                    className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-md ${
                      applied
                        ? 'bg-emerald-600 text-white'
                        : 'bg-purple-600 hover:bg-purple-500 text-white'
                    }`}
                  >
                    {applied ? <Check className="w-4 h-4 text-emerald-200" /> : <Sparkles className="w-4 h-4 text-amber-300" />}
                    <span>{applied ? 'Terkunci ke Prompt Anchors!' : 'Kunci Objek Foto ke Semua Scene'}</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
