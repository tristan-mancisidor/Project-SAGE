import { useState, useRef } from 'react'

const API_BASE = import.meta.env.VITE_API_URL || ''

function UploadZone({ onFilesUploaded, uploadedFiles = [] }) {
  const [files, setFiles] = useState(uploadedFiles)
  const [pendingFiles, setPendingFiles] = useState([])
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const droppedFiles = Array.from(e.dataTransfer.files).filter(
      f => f.type === 'application/pdf'
    )
    if (droppedFiles.length > 0) {
      setPendingFiles(prev => [...prev, ...droppedFiles])
    }
  }

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files)
    if (selectedFiles.length > 0) {
      setPendingFiles(prev => [...prev, ...selectedFiles])
    }
    e.target.value = ''
  }

  const handleConfirmUpload = async () => {
    setUploading(true)
    const uploaded = []

    for (const file of pendingFiles) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        const response = await fetch(`${API_BASE}/upload`, {
          method: 'POST',
          body: formData,
        })
        if (response.ok) {
          const data = await response.json()
          uploaded.push(data)
        }
      } catch (err) {
        console.error(`Failed to upload ${file.name}:`, err)
      }
    }

    const allFiles = [...files, ...uploaded]
    setFiles(allFiles)
    onFilesUploaded(allFiles)
    setPendingFiles([])
    setUploading(false)
  }

  const removePendingFile = (index) => {
    setPendingFiles(prev => prev.filter((_, i) => i !== index))
  }

  return (
    <div>
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`
          border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all
          ${isDragging
            ? 'border-sage-500 bg-sage-50'
            : 'border-gray-300 hover:border-sage-400 hover:bg-gray-50'
          }
        `}
      >
        <div className="text-4xl mb-3 text-gray-400">
          {uploading ? '...' : '+'}
        </div>
        <p className="text-gray-600 font-medium">
          {uploading ? 'Uploading...' : 'Drop PDF documents here'}
        </p>
        <p className="text-gray-400 text-sm mt-1">
          or click to browse
        </p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          multiple
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* Pending files awaiting confirmation */}
      {pendingFiles.length > 0 && (
        <div className="mt-4 space-y-2">
          {pendingFiles.map((file, i) => (
            <div
              key={`pending-${i}`}
              className="flex items-center gap-3 bg-sage-50 border border-sage-200 rounded-lg px-4 py-2"
            >
              <svg className="w-4 h-4 text-sage-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-gray-700 text-sm">{file.name}</span>
              <span className="text-sage-600 text-xs font-medium ml-auto">Ready</span>
              <button
                onClick={(e) => { e.stopPropagation(); removePendingFile(i) }}
                className="text-gray-400 hover:text-red-500 text-xs ml-2"
              >
                Remove
              </button>
            </div>
          ))}
          <button
            onClick={handleConfirmUpload}
            disabled={uploading}
            className="w-full mt-3 bg-sage-600 hover:bg-sage-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50"
          >
            {uploading ? 'Uploading...' : `Begin Analysis (${pendingFiles.length} file${pendingFiles.length > 1 ? 's' : ''})`}
          </button>
        </div>
      )}

      {/* Already uploaded file list */}
      {files.length > 0 && (
        <div className="mt-4 space-y-2">
          {files.map((file, i) => (
            <div
              key={file.file_id || i}
              className="flex items-center gap-3 bg-white border border-gray-200 rounded-lg px-4 py-2"
            >
              <svg className="w-4 h-4 text-green-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-gray-700 text-sm">{file.filename}</span>
              <span className="ml-auto text-green-600 text-xs font-medium">Uploaded</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default UploadZone
