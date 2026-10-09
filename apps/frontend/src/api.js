const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error(`Health check error: ${res.status}`);
    return await res.json();
  } catch (error) {
    return { status: 'offline', database: 'error', redis: 'error', error: error.message };
  }
}

export async function fetchTasks() {
  const res = await fetch(`${API_BASE_URL}/api/tasks`);
  if (!res.ok) {
    throw new Error(`Failed to fetch tasks: ${res.statusText}`);
  }
  return await res.json();
}

export async function createTask(data) {
  const res = await fetch(`${API_BASE_URL}/api/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    throw new Error(`Failed to create task: ${res.statusText}`);
  }
  return await res.json();
}

export async function deleteTask(taskId) {
  const res = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
    method: 'DELETE',
  });
  if (!res.ok) {
    throw new Error(`Failed to delete task: ${res.statusText}`);
  }
  return true;
}
