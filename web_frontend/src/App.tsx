import { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuthStore } from './store/authStore'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import NotePage from './pages/NotePage'
import AdminPanel from './pages/AdminPanel'
import AdminUserDetail from './pages/AdminUserDetail'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false, // Don't retry on 401 errors
      refetchOnWindowFocus: false,
    },
  },
})

function App() {
  const token = useAuthStore((state) => state.token)
  const [isInitialized, setIsInitialized] = useState(false)

  useEffect(() => {
    // On app load, zustand persist has already loaded state from localStorage
    // Just mark as initialized
    setIsInitialized(true)
  }, [])

  // Don't render routes until we've checked auth state
  if (!isInitialized) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-gray-500">Loading...</div>
      </div>
    )
  }

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            {/* Auth routes */}
            <Route path="/login" element={!token ? <LoginPage /> : <Navigate to="/dashboard" />} />
            <Route path="/register" element={!token ? <RegisterPage /> : <Navigate to="/dashboard" />} />
            
            {/* Protected routes */}
            <Route 
              path="/dashboard" 
              element={token ? <DashboardPage /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/notes/:id" 
              element={token ? <NotePage /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/admin" 
              element={token ? <AdminPanel /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/admin/users/:userId" 
              element={token ? <AdminUserDetail /> : <Navigate to="/login" />} 
            />
            
            {/* Default route */}
            <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} replace />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
