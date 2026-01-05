import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

type Project = {
  id: number
  title: string
  description?: string
  status: string
}

export function Projects() {
  const { data, isLoading } = useQuery({ queryKey: ['projects'], queryFn: async () => (await api.get('/projects')).data as Project[] })

  if (isLoading) return <div>Loading projects…</div>

  return (
    <div>
      <h2>Projects</h2>
      <div className="grid">
        {data?.map((p) => (
          <article key={p.id} className="card">
            <h3>{p.title}</h3>
            <p>{p.description}</p>
            <span className="tag">{p.status}</span>
          </article>
        ))}
      </div>
    </div>
  )
}
