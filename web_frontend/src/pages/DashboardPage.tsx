import Header from '../components/layout/Header'
import NotesList from '../components/notes/NotesList'

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Your Notes</h2>
          <p className="mt-2 text-gray-600">
            Create and manage your notes and daily plans
          </p>
        </div>
        
        <NotesList />
      </main>
    </div>
  )
}
