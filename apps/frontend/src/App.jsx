import React, { useState, useEffect } from 'react'
import { fetchHealth, fetchTasks, createTask, deleteTask } from './api'

export default function App() {
  const [health, setHealth] = useState({ status: 'checking', database: 'unknown', redis: 'unknown' })
  const [tasks, setTasks] = useState([])
  const [expandedTaskId, setExpandedTaskId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  // Stan formularza nowego zadania
  const [title, setTitle] = useState('')
  const [taskType, setTaskType] = useState('data_processing')
  const [payload, setPayload] = useState('')

  const loadData = async () => {
    try {
      const [healthData, tasksData] = await Promise.all([
        fetchHealth(),
        fetchTasks().catch(() => ({ tasks: [] })),
      ])
      setHealth(healthData)
      if (tasksData && tasksData.tasks) {
        setTasks(tasksData.tasks)
      }
    } catch (err) {
      console.error('Error fetching data:', err)
    }
  }

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 2500)
    return () => clearInterval(interval)
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!title.trim()) return

    setLoading(true)
    setErrorMsg('')
    try {
      await createTask({
        title: title.trim(),
        task_type: taskType,
        payload: payload.trim() || null,
      })
      setTitle('')
      setPayload('')
      await loadData()
    } catch (err) {
      setErrorMsg(err.message || 'Nie udało się utworzyć zadania')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (taskId) => {
    try {
      await deleteTask(taskId)
      await loadData()
    } catch (err) {
      alert(`Błąd usuwania zadania: ${err.message}`)
    }
  }

  const getDotClass = (status) => {
    if (status === 'ok' || status === 'healthy') return 'dot dot-ok'
    if (status === 'degraded' || status === 'unavailable') return 'dot dot-warn'
    return 'dot dot-err'
  }

  return (
    <div className="container">
      <header>
        <div>
          <h1>Task Microservices Platform</h1>
          <p className="subtitle">Przykładowy system mikrousług: Web UI + REST API + Asynchroniczny Worker</p>
        </div>
        <div className="health-bar">
          <div className="health-badge" title={`API: ${health.status}`}>
            <span className={getDotClass(health.status)}></span>
            API: {health.status}
          </div>
          <div className="health-badge" title={`DB: ${health.database}`}>
            <span className={getDotClass(health.database)}></span>
            Baza: {health.database}
          </div>
          <div className="health-badge" title={`Redis: ${health.redis}`}>
            <span className={getDotClass(health.redis)}></span>
            Redis: {health.redis}
          </div>
        </div>
      </header>

      <div className="grid">
        {/* Kolumna formularza dodawania zadania */}
        <div className="card">
          <h2 className="card-title">Zleć nowe zadanie</h2>
          {errorMsg && (
            <div style={{ color: '#fca5a5', marginBottom: '1rem', fontSize: '0.85rem' }}>
              ⚠️ {errorMsg}
            </div>
          )}
          <form onSubmit={handleSubmit}>
            <label>
              Tytuł zadania:
              <input
                type="text"
                placeholder="np. Analiza sprzedaży Q3"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </label>

            <label>
              Typ zadania:
              <select value={taskType} onChange={(e) => setTaskType(e.target.value)}>
                <option value="data_processing">Przetwarzanie danych (Data Processing)</option>
                <option value="report_generation">Generowanie raportu (Report Generation)</option>
                <option value="image_optimization">Optymalizacja zasobów (Resource Optimization)</option>
              </select>
            </label>

            <label>
              Parametry / Payload (opcjonalnie):
              <textarea
                rows="3"
                placeholder="Wpisz parametry lub 'fail' aby przetestować obsługę błędów..."
                value={payload}
                onChange={(e) => setPayload(e.target.value)}
              />
            </label>

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Wysyłanie...' : 'Dodaj zadanie do kolejki'}
            </button>
          </form>
        </div>

        {/* Kolumna listy zadań */}
        <div className="card">
          <div className="task-list-header">
            <h2 className="card-title" style={{ margin: 0 }}>
              Zadania w systemie ({tasks.length})
            </h2>
            <button
              onClick={loadData}
              style={{ background: '#334155', color: '#f8fafc', padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
            >
              Odśwież
            </button>
          </div>

          {tasks.length === 0 ? (
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', textAlign: 'center', padding: '2rem 0' }}>
              Brak zadań w systemie. Użyj formularza obok, aby zlecić pierwsze zadanie.
            </p>
          ) : (
            <table className="task-table">
              <thead>
                <tr>
                  <th>Tytuł / Typ</th>
                  <th>Status & Postęp</th>
                  <th>Utworzono</th>
                  <th>Akcje</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map((task) => (
                  <React.Fragment key={task.id}>
                    <tr>
                      <td>
                        <strong>{task.title}</strong>
                        <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>{task.task_type}</div>
                      </td>
                      <td>
                        <span className={`status-badge status-${task.status}`}>{task.status}</span>
                        {task.status === 'RUNNING' && (
                          <div className="progress-container">
                            <div className="progress-bar" style={{ width: `${task.progress}%` }}></div>
                          </div>
                        )}
                        {task.status === 'RUNNING' && (
                          <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{task.progress}%</span>
                        )}
                      </td>
                      <td style={{ color: '#94a3b8' }}>
                        {new Date(task.created_at).toLocaleTimeString()}
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button
                            type="button"
                            onClick={() => setExpandedTaskId(expandedTaskId === task.id ? null : task.id)}
                            style={{
                              background: '#334155',
                              color: '#cbd5e1',
                              padding: '0.3rem 0.5rem',
                              fontSize: '0.75rem',
                            }}
                          >
                            {expandedTaskId === task.id ? 'Ukryj' : 'Szczegóły'}
                          </button>
                          <button
                            type="button"
                            className="btn-danger"
                            onClick={() => handleDelete(task.id)}
                            title="Usuń zadanie"
                          >
                            Usuń
                          </button>
                        </div>
                      </td>
                    </tr>
                    {expandedTaskId === task.id && (
                      <tr>
                        <td colSpan="4" style={{ padding: '0 0.5rem 1rem 0.5rem' }}>
                          {task.error ? (
                            <div className="details-box details-error">
                              <strong>Błąd:</strong> {task.error}
                            </div>
                          ) : task.result ? (
                            <div className="details-box">
                              <strong>Rezultat:</strong>
                              <br />
                              {task.result}
                            </div>
                          ) : (
                            <div className="details-box" style={{ color: '#94a3b8' }}>
                              Zadanie oczekuje na przetworzenie przez workera...
                            </div>
                          )}
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
