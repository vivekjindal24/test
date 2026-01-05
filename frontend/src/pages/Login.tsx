import { FormEvent, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import api from '../api/client'
import { Role } from '../App'

export function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<Role>('student')
  const from = (location.state as any)?.from?.pathname || '/'

  async function submit(e: FormEvent) {
    e.preventDefault()
    try {
      const res = await api.post('/auth/token', new URLSearchParams({ username: email, password }))
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('role', role)
      navigate(from, { replace: true })
    } catch (err) {
      alert('Login failed')
    }
  }

  return (
    <div className="auth">
      <form onSubmit={submit}>
        <h2>Sign in</h2>
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <label>Role (demo)</label>
        <select value={role} onChange={(e) => setRole(e.target.value as Role)}>
          <option value="student">Student</option>
          <option value="supervisor">Supervisor</option>
          <option value="hod">HOD</option>
          <option value="admin">Admin</option>
        </select>
        <button type="submit">Login</button>
      </form>
    </div>
  )
}
