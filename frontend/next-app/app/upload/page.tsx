'use client'

import React, { useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowLeft, Upload, FileText, Copy, Check, Bot, Building } from 'lucide-react'

export default function UploadPage() {
  const router = useRouter()
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [pastedContent, setPastedContent] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [isPasting, setIsPasting] = useState(false)
  const [prdType, setPrdType] = useState<'agent' | 'platform'>('agent')
  const [detectedType, setDetectedType] = useState<'agent' | 'platform' | null>(null)
  const [copied, setCopied] = useState(false)
  const [uploadedPRD, setUploadedPRD] = useState<any>(null)
  const [showSuccessMessage, setShowSuccessMessage] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const detectTypeFromContent = async (content: string) => {
    if (!content.trim()) return
    
    try {
      // Create a temporary file to send to the backend for type detection
      const blob = new Blob([content], { type: 'text/markdown' })
      const file = new File([blob], `temp-${Date.now()}.md`, { type: 'text/markdown' })
      
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch('/api/v1/prds/upload', {
        method: 'POST',
        body: formData,
      })
      
      if (response.ok) {
        const result = await response.json()
        if (result.prd_type) {
          setDetectedType(result.prd_type)
          setPrdType(result.prd_type)
        }
      }
    } catch (error) {
      console.error('Error detecting type:', error)
    }
  }

  // Removed createAgentFromPRD - PRDs should just go to queue, not automatically create agents

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setPastedContent('') // Clear pasted content when file is selected
      setDetectedType(null) // Reset detection
      // Auto-upload the file immediately after selection
      setTimeout(() => handleFileUpload(file), 100)
    }
  }

  const handleFileDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file && (file.name.endsWith('.md') || file.name.endsWith('.txt'))) {
      setSelectedFile(file)
      setPastedContent('') // Clear pasted content when file is selected
      setDetectedType(null) // Reset detection
      // Auto-upload the file immediately after drop
      setTimeout(() => handleFileUpload(file), 100)
    }
  }

  const handleFileUpload = async (file?: File) => {
    const fileToUpload = file || selectedFile
    if (!fileToUpload) return

    setIsUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', fileToUpload)

      const response = await fetch('/api/v1/prds/upload', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const result = await response.json()
        // Set the detected type from the response
        if (result.prd_type) {
          setDetectedType(result.prd_type)
          setPrdType(result.prd_type)
        }
        
        // Store the uploaded PRD and show success
        setUploadedPRD(result)
        setShowSuccessMessage(true)
        
        // Clear the form
        setSelectedFile(null)
        setPastedContent('')
        
        // Auto-redirect to main page after 2 seconds to show PRD in queue
        setTimeout(() => {
          router.push('/')
        }, 2000)
      } else {
        const error = await response.json()
        alert(`Upload failed: ${error.detail}`)
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('Upload failed. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

  const handlePasteUpload = async () => {
    if (!pastedContent.trim()) return

    setIsPasting(true)
    try {
      // Create a temporary file from pasted content
      const blob = new Blob([pastedContent], { type: 'text/markdown' })
      const file = new File([blob], 'pasted-prd.md', { type: 'text/markdown' })

      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/v1/prds/upload', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const result = await response.json()
        // Set the detected type from the response
        if (result.prd_type) {
          setDetectedType(result.prd_type)
          setPrdType(result.prd_type)
        }
        
        // Store the uploaded PRD and show success
        setUploadedPRD(result)
        setShowSuccessMessage(true)
        
        // Clear the form
        setSelectedFile(null)
        setPastedContent('')
        
        // Auto-redirect to main page after 2 seconds to show PRD in queue
        setTimeout(() => {
          router.push('/')
        }, 2000)
      } else {
        const error = await response.json()
        alert(`Upload failed: ${error.detail}`)
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('Upload failed. Please try again.')
    } finally {
      setIsPasting(false)
    }
  }


  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(pastedContent)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy: ', err)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={() => router.back()}
            className="mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          
          <div className="text-center">
            <h1 className="text-3xl font-bold tracking-tight">Upload PRD</h1>
            <p className="text-muted-foreground mt-2">
              Upload your completed, formatted PRD to add it to the agent creation queue
            </p>
          </div>
        </div>

        {/* Success Message */}
        {showSuccessMessage && uploadedPRD && (
          <Card className="mb-6 border-green-200 bg-green-50">
            <CardHeader>
              <CardTitle className="text-green-800 flex items-center gap-2">
                <Check className="h-5 w-5" />
                PRD Uploaded Successfully!
              </CardTitle>
              <CardDescription className="text-green-700">
                Your PRD has been uploaded and added to the queue! Redirecting to dashboard...
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="text-green-700 border-green-300">
                    {uploadedPRD.prd_type || 'agent'} PRD
                  </Badge>
                  <span className="text-sm text-green-700">
                    ID: {uploadedPRD.id}
                  </span>
                </div>
                <p className="text-sm text-green-700">
                  <strong>Title:</strong> {uploadedPRD.title}
                </p>
                <div className="flex gap-2">
                  <Button
                    onClick={() => router.push('/?tab=prds')}
                    className="bg-green-600 hover:bg-green-700 text-white"
                  >
                    View in PRDs Tab
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setShowSuccessMessage(false)}
                    className="border-green-300 text-green-700 hover:bg-green-100"
                  >
                    Continue Uploading
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <div className="grid gap-6 md:grid-cols-2">
          {/* File Upload Option */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                Upload File
              </CardTitle>
              <CardDescription>
                Drag & drop or click to upload a .md or .txt file. It will be processed automatically.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div 
                className="border-2 border-dashed border-gray-300 hover:border-gray-400 rounded-lg p-6 text-center cursor-pointer transition-colors"
                onDrop={handleFileDrop}
                onDragOver={(e) => e.preventDefault()}
                onDragEnter={(e) => e.preventDefault()}
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="space-y-4">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".md,.txt"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  
                  {isUploading ? (
                    <div className="flex flex-col items-center gap-2">
                      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                      <span className="text-sm text-gray-600">Processing {selectedFile?.name}...</span>
                    </div>
                  ) : selectedFile ? (
                    <div className="flex flex-col items-center gap-2">
                      <FileText className="h-6 w-6 text-green-600" />
                      <span className="text-sm text-green-600 font-medium">{selectedFile.name}</span>
                      <span className="text-xs text-gray-500">Processing automatically...</span>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-2">
                      <Upload className="h-8 w-8 text-gray-400" />
                      <span className="text-sm text-gray-600">Click to browse or drag & drop</span>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="text-xs text-muted-foreground text-center">
                Supported formats: .md, .txt • Files are processed automatically
              </div>
            </CardContent>
          </Card>

          {/* Paste Content Option */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Copy className="h-5 w-5" />
                Paste Content
              </CardTitle>
              <CardDescription>
                Copy and paste your PRD markdown content directly
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <textarea
                  value={pastedContent}
                  onChange={(e) => {
                    setPastedContent(e.target.value)
                    setDetectedType(null) // Reset detection when content changes
                  }}
                  placeholder="Paste your PRD markdown content here..."
                  className="w-full h-64 p-3 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onFocus={() => setSelectedFile(null)} // Clear file selection when pasting
                />
                
                <div className="flex gap-2">
                  <Button
                    onClick={handlePasteUpload}
                    disabled={!pastedContent.trim() || isPasting}
                    className="flex-1"
                  >
                    {isPasting ? 'Processing...' : 'Parse & Create PRD'}
                  </Button>
                  
                  {pastedContent && (
                    <>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => detectTypeFromContent(pastedContent)}
                        disabled={detectedType !== null}
                        className="px-3 flex items-center gap-1"
                      >
                        <Bot className="h-4 w-4" />
                        {detectedType ? 'Detected' : 'Detect Type'}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={copyToClipboard}
                        className="px-3"
                      >
                        {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                      </Button>
                    </>
                  )}
                </div>
              </div>
              
              <div className="text-xs text-muted-foreground">
                Paste your complete PRD in markdown format
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Help Section */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>How it works</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="text-center space-y-2">
                <div className="w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto text-sm font-semibold">
                  1
                </div>
                <h4 className="font-medium">Upload PRD</h4>
                <p className="text-sm text-muted-foreground">
                  Upload a file or paste your PRD content
                </p>
              </div>
              <div className="text-center space-y-2">
                <div className="w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto text-sm font-semibold">
                  2
                </div>
                <h4 className="font-medium">Auto-Parse</h4>
                <p className="text-sm text-muted-foreground">
                  We automatically extract all the details
                </p>
              </div>
              <div className="text-center space-y-2">
                <div className="w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center mx-auto text-sm font-semibold">
                  3
                </div>
                <h4 className="font-medium">Added to Queue</h4>
                <p className="text-sm text-muted-foreground">
                  Your PRD is now in the agent creation queue
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
