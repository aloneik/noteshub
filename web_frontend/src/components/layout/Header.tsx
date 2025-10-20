import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'

export default function Header() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-indigo-600">NoteHub</h1>
          </div>
          
          <div className="flex items-center space-x-4">
            {user && (
              <>
                <span className="text-gray-700">
                  Welcome, <span className="font-medium">{user.username}</span>
                  {user.is_admin && (
                    <span className="ml-2 px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                      Admin
                    </span>
                  )}
                </span>
                {user.is_admin && (
                  <button
                    onClick={() => navigate('/admin')}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                  >
                    Admin Panel
                  </button>
                )}
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
