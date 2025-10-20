import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { adminApi } from '../api/admin'
import { useNavigate } from 'react-router-dom'

export default function AdminPanel() {
  const navigate = useNavigate()
  const [expandedNoteId, setExpandedNoteId] = useState<number | null>(null)

  const { data: users, isLoading: usersLoading, error: usersError } = useQuery({
    queryKey: ['admin', 'users'],
    queryFn: adminApi.getAllUsers,
  })

  const { data: notes, isLoading: notesLoading, error: notesError } = useQuery({
    queryKey: ['admin', 'notes'],
    queryFn: adminApi.getAllNotes,
  })

  // Check for 403 error (not admin)
  if (usersError && 'response' in usersError && (usersError as any).response?.status === 403) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Access Denied</h2>
          <p className="text-gray-600 mb-4">You don't have admin privileges.</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    )
  }

  if (usersLoading || notesLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading admin data...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Admin Panel</h1>
          <p className="text-gray-600">Manage all users and notes</p>
        </div>

        {/* Users Section */}
        <div className="bg-white rounded-lg shadow-md mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              All Users ({users?.length || 0})
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Username
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Role
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {users?.map((user) => (
                  <tr key={user.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {user.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => navigate(`/admin/users/${user.id}`)}
                        className="text-indigo-600 hover:text-indigo-800 hover:underline"
                      >
                        {user.username}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {user.is_admin ? (
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          Admin
                        </span>
                      ) : (
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                          User
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Notes Section */}
        <div className="bg-white rounded-lg shadow-md">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              All Notes ({notes?.length || 0})
            </h2>
          </div>
          <div className="p-6 space-y-4">
            {notes?.map((note) => (
              <div
                key={note.id}
                className="border border-gray-200 rounded-lg overflow-hidden"
              >
                {/* Note Header - Clickable */}
                <div
                  onClick={() => setExpandedNoteId(expandedNoteId === note.id ? null : note.id)}
                  className="px-4 py-3 bg-gray-50 cursor-pointer hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-md font-semibold text-gray-900">{note.title}</h3>
                      <div className="mt-1 flex items-center space-x-3 text-xs text-gray-500">
                        <span>ID: {note.id}</span>
                        <span>•</span>
                        <span>
                          Owner:{' '}
                          <button
                            onClick={(e) => {
                              e.stopPropagation()
                              navigate(`/admin/users/${note.owner_id}`)
                            }}
                            className="text-indigo-600 hover:underline"
                          >
                            #{note.owner_id}
                          </button>
                        </span>
                        <span>•</span>
                        <span>{note.plans?.length || 0} plans</span>
                        <span>•</span>
                        <span>{new Date(note.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <svg
                      className={`w-5 h-5 text-gray-400 transition-transform ${
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
                  <div className="px-4 py-3 bg-white">
                    {/* Content */}
                    <div className="mb-4">
                      <h4 className="text-xs font-medium text-gray-700 mb-2">Content:</h4>
                      {note.content ? (
                        <div className="bg-gray-50 rounded p-3 text-sm text-gray-800 whitespace-pre-wrap">
                          {note.content}
                        </div>
                      ) : (
                        <p className="text-sm text-gray-400 italic">No content</p>
                      )}
                    </div>

                    {/* Plans */}
                    {note.plans && note.plans.length > 0 && (
                      <div>
                        <h4 className="text-xs font-medium text-gray-700 mb-2">
                          Plans ({note.plans.length}):
                        </h4>
                        <div className="space-y-2">
                          {note.plans.map((plan: any) => (
                            <div
                              key={plan.id}
                              className="flex items-center space-x-2 text-sm"
                            >
                              {plan.is_done ? (
                                <svg className="w-4 h-4 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                  <path
                                    fillRule="evenodd"
                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                    clipRule="evenodd"
                                  />
                                </svg>
                              ) : (
                                <svg className="w-4 h-4 text-gray-300 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                  <path
                                    fillRule="evenodd"
                                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12z"
                                    clipRule="evenodd"
                                  />
                                </svg>
                              )}
                              <span className={plan.is_done ? 'line-through text-gray-500' : 'text-gray-900'}>
                                {plan.title}
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
              <div className="text-center py-8 text-gray-500">
                No notes found in the system.
              </div>
            )}
          </div>
        </div>

        {/* Back to Dashboard Button */}
        <div className="mt-8 text-center">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}
