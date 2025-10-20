import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { plansApi } from '../../api/plans'
import type { Plan } from '../../types'

interface PlansListProps {
  noteId: number
  plans: Plan[]
}

export default function PlansList({ noteId, plans }: PlansListProps) {
  const queryClient = useQueryClient()
  const [isAdding, setIsAdding] = useState(false)
  const [newPlanText, setNewPlanText] = useState('')
  const [editingPlanId, setEditingPlanId] = useState<number | null>(null)
  const [editingText, setEditingText] = useState('')

  // Create plan mutation
  const createMutation = useMutation({
    mutationFn: (data: { noteId: number; title: string }) => 
      plansApi.create(data.noteId, { title: data.title, is_done: false }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['note', noteId] })
      setIsAdding(false)
      setNewPlanText('')
    },
  })

  // Update plan mutation
  const updateMutation = useMutation({
    mutationFn: ({ planId, title, is_done }: { planId: number; title?: string; is_done?: boolean }) =>
      plansApi.update(noteId, planId, { title, is_done }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['note', noteId] })
      setEditingPlanId(null)
      setEditingText('')
    },
  })

  // Delete plan mutation
  const deleteMutation = useMutation({
    mutationFn: (planId: number) => plansApi.delete(noteId, planId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['note', noteId] })
    },
  })

  const handleAddPlan = (e: React.FormEvent) => {
    e.preventDefault()
    if (newPlanText.trim()) {
      createMutation.mutate({ noteId, title: newPlanText })
    }
  }

  const handleTogglePlan = (plan: Plan) => {
    updateMutation.mutate({ planId: plan.id, is_done: !plan.is_done })
  }

  const handleDeletePlan = (planId: number) => {
    if (confirm('Delete this plan?')) {
      deleteMutation.mutate(planId)
    }
  }

  const handleStartEdit = (plan: Plan) => {
    setEditingPlanId(plan.id)
    setEditingText(plan.title)
  }

  const handleSaveEdit = (planId: number) => {
    if (editingText.trim()) {
      updateMutation.mutate({ planId, title: editingText })
    }
  }

  const handleCancelEdit = () => {
    setEditingPlanId(null)
    setEditingText('')
  }

  const handleKeyPress = (e: React.KeyboardEvent, planId: number) => {
    if (e.key === 'Enter') {
      handleSaveEdit(planId)
    } else if (e.key === 'Escape') {
      handleCancelEdit()
    }
  }

  const completedCount = plans.filter(p => p.is_done).length

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">
          Daily Plans
          {plans.length > 0 && (
            <span className="ml-2 text-sm font-normal text-gray-500">
              ({completedCount}/{plans.length} completed)
            </span>
          )}
        </h3>
      </div>

      {/* Plans List */}
      <div className="space-y-2">
        {plans.map((plan) => (
          <div
            key={plan.id}
            className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <input
              type="checkbox"
              checked={plan.is_done}
              onChange={() => handleTogglePlan(plan)}
              className="w-5 h-5 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500 flex-shrink-0"
              disabled={editingPlanId === plan.id}
            />
            
            {editingPlanId === plan.id ? (
              // Edit mode
              <>
                <input
                  type="text"
                  value={editingText}
                  onChange={(e) => setEditingText(e.target.value)}
                  onKeyDown={(e) => handleKeyPress(e, plan.id)}
                  className="flex-1 px-2 py-1 border border-indigo-500 rounded focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  autoFocus
                />
                <button
                  onClick={() => handleSaveEdit(plan.id)}
                  className="text-green-600 hover:text-green-700 flex-shrink-0"
                  disabled={updateMutation.isPending}
                  title="Save"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </button>
                <button
                  onClick={handleCancelEdit}
                  className="text-gray-400 hover:text-gray-600 flex-shrink-0"
                  title="Cancel"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </>
            ) : (
              // View mode
              <>
                <span
                  className={`flex-1 cursor-pointer ${
                    plan.is_done ? 'line-through text-gray-500' : 'text-gray-900'
                  }`}
                  onClick={() => handleStartEdit(plan)}
                  title="Click to edit"
                >
                  {plan.title}
                </span>
                <button
                  onClick={() => handleStartEdit(plan)}
                  className="text-gray-400 hover:text-indigo-600 flex-shrink-0"
                  title="Edit"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  onClick={() => handleDeletePlan(plan.id)}
                  className="text-gray-400 hover:text-red-600 flex-shrink-0"
                  disabled={deleteMutation.isPending}
                  title="Delete"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </>
            )}
          </div>
        ))}

        {plans.length === 0 && !isAdding && (
          <div className="text-center py-8 text-gray-500">
            No plans yet. Add your first daily plan!
          </div>
        )}
      </div>

      {/* Add Plan Form */}
      {isAdding ? (
        <form onSubmit={handleAddPlan} className="flex space-x-2">
          <input
            type="text"
            placeholder="New plan..."
            value={newPlanText}
            onChange={(e) => setNewPlanText(e.target.value)}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
            autoFocus
          />
          <button
            type="submit"
            disabled={createMutation.isPending}
            className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            Add
          </button>
          <button
            type="button"
            onClick={() => {
              setIsAdding(false)
              setNewPlanText('')
            }}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
          >
            Cancel
          </button>
        </form>
      ) : (
        <button
          onClick={() => setIsAdding(true)}
          className="w-full px-4 py-2 border-2 border-dashed border-gray-300 rounded-md text-gray-600 hover:border-indigo-500 hover:text-indigo-600 transition-colors"
        >
          + Add Plan
        </button>
      )}
    </div>
  )
}
