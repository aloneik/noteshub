import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { notesApi } from '../api/notes'
import Header from '../components/layout/Header'
import PlansList from '../components/plans/PlansList'
import type { Note } from '../types'

export default function NotePage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const noteId = parseInt(id || '0')

  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState('')
  const [editContent, setEditContent] = useState('')

  // Fetch note
  const { data: note, isLoading, error } = useQuery<Note>({
    queryKey: ['note', noteId],
    queryFn: () => notesApi.get(noteId),
    enabled: !!noteId,
  })

  // Update note mutation
  const updateMutation = useMutation({
    mutationFn: (data: { title: string; content: string }) =>
      notesApi.update(noteId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['note', noteId] })
      queryClient.invalidateQueries({ queryKey: ['notes'] })
      setIsEditing(false)
    },
  })

  // Delete note mutation
  const deleteMutation = useMutation({
    mutationFn: () => notesApi.delete(noteId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes'] })
      navigate('/dashboard')
    },
  })

  const handleEdit = () => {
    if (note) {
      setEditTitle(note.title)
      setEditContent(note.content || '')
      setIsEditing(true)
    }
  }

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault()
    updateMutation.mutate({
      title: editTitle,
      content: editContent,
    })
  }

  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this note?')) {
      deleteMutation.mutate()
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="flex justify-center items-center py-12">
          <div className="text-gray-500">Loading note...</div>
        </div>
      </div>
    )
  }

  if (error || !note) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header />
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">Note not found</div>
          </div>
          <button
            onClick={() => navigate('/dashboard')}
            className="mt-4 text-indigo-600 hover:text-indigo-700"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate('/dashboard')}
          className="mb-4 text-indigo-600 hover:text-indigo-700 flex items-center"
        >
          <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Dashboard
        </button>

        {/* Note Card */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          {isEditing ? (
            <form onSubmit={handleSave} className="space-y-4">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full text-2xl font-bold px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Note title..."
              />
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Note content..."
              />
              <div className="flex space-x-2">
                <button
                  type="submit"
                  disabled={updateMutation.isPending}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
                >
                  {updateMutation.isPending ? 'Saving...' : 'Save'}
                </button>
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <>
              <div className="flex justify-between items-start mb-4">
                <h1 className="text-3xl font-bold text-gray-900">{note.title}</h1>
                <div className="flex space-x-2">
                  <button
                    onClick={handleEdit}
                    className="px-3 py-1 text-sm text-indigo-600 hover:bg-indigo-50 rounded-md"
                  >
                    Edit
                  </button>
                  <button
                    onClick={handleDelete}
                    disabled={deleteMutation.isPending}
                    className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded-md disabled:opacity-50"
                  >
                    Delete
                  </button>
                </div>
              </div>
              
              {note.content && (
                <p className="text-gray-700 whitespace-pre-wrap mb-4">{note.content}</p>
              )}
              
              <div className="text-xs text-gray-500">
                Created: {new Date(note.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </div>
            </>
          )}
        </div>

        {/* Plans Section */}
        <div className="bg-white rounded-lg shadow p-6">
          <PlansList noteId={noteId} plans={note.plans || []} />
        </div>
      </main>
    </div>
  )
}
