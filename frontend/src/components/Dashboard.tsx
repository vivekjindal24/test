import { Link, Outlet, useNavigate } from 'react-router-dom'
import { Role } from '../App'

export function Dashboard() {
  const navigate = useNavigate()
  const role = (localStorage.getItem('role') as Role) || 'student'

  const links = [
    { to: '/projects', label: 'Projects' },
    { to: '/documents', label: 'Documents' }
  ]

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">Research</div>
        <div className="role">{role.toUpperCase()}</div>
        <nav>
          {links.map((l) => (
            <Link key={l.to} to={l.to} className="nav-link">
              {l.label}
            </Link>
          ))}
        </nav>
        <button
          className="secondary"
          onClick={() => {
            localStorage.clear()
            navigate('/login')
          }}
        >
          Logout
        </button>
      </aside>
      <main>
        <header className="page-header">
          <h1>Research Lifecycle</h1>
          <p>Milestones, meetings, manuscripts, publications, and notifications.</p>
        </header>
        <section className="content">
          <Outlet />
        </section>
      </main>
    </div>
  )
}
