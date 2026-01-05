import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

type Document = {
  id: number
  title: string
  path: string
  mime_type: string
}

export function Documents() {
  const { data, isLoading } = useQuery({ queryKey: ['documents'], queryFn: async () => (await api.get('/documents/1')).data as Document[] })

  if (isLoading) return <div>Loading documents…</div>

  return (
    <div>
      <h2>Documents</h2>
      <ul>
        {data?.map((d) => (
          <li key={d.id}>
            {d.title} <small>{d.mime_type}</small> <code>{d.path}</code>
          </li>
        ))}
      </ul>
    </div>
  )
}
