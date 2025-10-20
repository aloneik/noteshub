import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useParams, useNavigate } from 'react-router-dom'
import { adminApi } from '../api/admin'

export default function AdminUserDetail() {
  const { userId } = useParams<{ userId: string }>()
  const navigate = useNavigate()
  const [expandedNoteId, setExpandedNoteId] = useState<number | null>(null)

  const { data: notes, isLoading } = useQuery({
    queryKey: ['admin', 'user', userId, 'notes'],
    queryFn: () => adminApi.getUserNotes(Number(userId)),
    enabled: !!userId,
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading user notes...</div>
      </div>
    )
  }

  const toggleNote = (noteId: number) => {
    setExpandedNoteId(expandedNoteId === noteId ? null : noteId)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <button
              onClick={() => navigate('/admin')}
              className="mb-4 text-indigo-600 hover:text-indigo-800 flex items-center"
            >
              <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Admin Panel
            </button>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              User #{userId} Notes
            </h1>
            <p className="text-gray-600">
              {notes?.length || 0} notes found
            </p>
          </div>
        </div>

        {/* Notes List */}
        <div className="space-y-4">
          {notes?.map((note) => (
            <div
              key={note.id}
              className="bg-white rounded-lg shadow-md overflow-hidden"
            >
              {/* Note Header - Clickable */}
              <div
                onClick={() => toggleNote(note.id)}
                className="px-6 py-4 border-b border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {note.title}
                    </h3>
                    <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                      <span>ID: {note.id}</span>
                      <span>•</span>
                      <span>{note.plans?.length || 0} plans</span>
                      <span>•</span>
                      <span>{new Date(note.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <svg
                    className={`w-6 h-6 text-gray-400 transition-transform ${
                      expandedNoteId === note.id ? 'transform rotate-180' : ''
                    }`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>

              {/* Note Content - Expandable */}
              {expandedNoteId === note.id && (
                <div className="px-6 py-4">
                  {/* Content */}
                  <div className="mb-6">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Content:</h4>
                    {note.content ? (
                      <div className="bg-gray-50 rounded-lg p-4 text-gray-800 whitespace-pre-wrap">
                        {note.content}
                      </div>
                    ) : (
                      <p className="text-gray-400 italic">No content</p>
                    )}
                  </div>

                  {/* Plans */}
                  {note.plans && note.plans.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-gray-700 mb-3">
                        Daily Plans ({note.plans.length}):
                      </h4>
                      <div className="space-y-2">
                        {note.plans.map((plan) => (
                          <div
                            key={plan.id}
                            className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                          >
                            <div className="flex-shrink-0">
                              {plan.is_done ? (
                                <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                                  <path
                                    fillRule="evenodd"
                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                    clipRule="evenodd"
                                  />
                                </svg>
                              ) : (
                                <svg className="w-5 h-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                                  <path
                                    fillRule="evenodd"
                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12z"
                                    clipRule="evenodd"
                                  />
                                </svg>
                              )}
                            </div>
                            <span
                              className={`flex-1 ${
                                plan.is_done ? 'line-through text-gray-500' : 'text-gray-900'
                              }`}
                            >
                              {plan.title}
                            </span>
                            <span className="text-xs text-gray-400">
                              {new Date(plan.created_at).toLocaleString()}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {notes?.length === 0 && (
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <p className="text-gray-500">This user has no notes yet.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
