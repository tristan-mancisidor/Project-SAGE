import { useState, useRef } from 'react'

const API_BASE = ''

function UploadZone({ onFilesUploaded }) {
  const [files, setFiles] = useState([])
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
      uploadFiles(droppedFiles)
    }
  }

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files)
    if (selectedFiles.length > 0) {
      uploadFiles(selectedFiles)
    }
  }

  const uploadFiles = async (newFiles) => {
    setUploading(true)
    const uploaded = []

    for (const file of newFiles) {
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
    setUploading(false)
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

      {/* Uploaded file list */}
      {files.length > 0 && (
        <div className="mt-4 space-y-2">
          {files.map((file, i) => (
            <div
              key={file.file_id || i}
              className="flex items-center gap-3 bg-white border border-gray-200 rounded-lg px-4 py-2"
            >
              <span className="text-sage-600 text-sm font-mono">PDF</span>
              <span className="text-gray-700 text-sm">{file.filename}</span>
              <span className="ml-auto text-green-600 text-xs">Uploaded</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default UploadZone
