import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuthStore } from './store/authStore'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import NotePage from './pages/NotePage'

const queryClient = new QueryClient()

function App() {
  const token = useAuthStore((state) => state.token)

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
            
            {/* Default route */}
            <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} replace />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
