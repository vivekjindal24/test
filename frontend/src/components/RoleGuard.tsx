import { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { Role } from '../App'

const allowedRoles: Role[] = ['student', 'supervisor', 'hod', 'admin']

export function RoleGuard({ children }: { children: ReactNode }) {
  const location = useLocation()
  const role = (localStorage.getItem('role') as Role) || 'student'
  const token = localStorage.getItem('access_token')

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />
  }
  if (!allowedRoles.includes(role)) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}
