import { Navigate, Route, Routes } from 'react-router-dom'
import { Dashboard } from './components/Dashboard'
import { RoleGuard } from './components/RoleGuard'
import { Login } from './pages/Login'
import { Projects } from './pages/Projects'
import { Documents } from './pages/Documents'

export type Role = 'student' | 'supervisor' | 'hod' | 'admin'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <RoleGuard>
            <Dashboard />
          </RoleGuard>
        }
      >
        <Route index element={<Navigate to="/projects" replace />} />
        <Route path="projects" element={<Projects />} />
        <Route path="documents" element={<Documents />} />
      </Route>
    </Routes>
  )
}
