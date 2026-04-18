const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoListEl = document.getElementById('todo-list');

let todos = [];

function renderTodos() {
  // Clear existing list
  todoListEl.innerHTML = '';
  // Render each todo item
  todos.forEach(todo => {
    const li = document.createElement('li');
    li.className = 'todo-item';
    if (todo.completed) li.classList.add('completed');
    li.dataset.id = todo.id;
    li.innerHTML = `
        <span class="todo-text">${todo.text}</span>
        <button class="complete-btn">${todo.completed ? 'Undo' : 'Complete'}</button>
        <button class="delete-btn">Delete</button>
      `;
    // Attach event listeners for complete and delete actions
    li.querySelector('.complete-btn').addEventListener('click', () => toggleComplete(todo.id));
    li.querySelector('.delete-btn').addEventListener('click', () => deleteTodo(todo.id));
    todoListEl.appendChild(li);
  });
}

function addTodo(text) {
  const id = Date.now();
  todos.push({ id, text, completed: false });
  renderTodos();
}

function toggleComplete(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    renderTodos();
  }
}

function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);
  renderTodos();
}

function handleFormSubmit(event) {
  event.preventDefault();
  const text = todoInput.value.trim();
  if (text) {
    addTodo(text);
    todoInput.value = '';
  }
}

if (todoForm) {
  todoForm.addEventListener('submit', handleFormSubmit);
}

// Expose for later tasks
window.todos = todos;
window.renderTodos = renderTodos;
window.addTodo = addTodo;
window.toggleComplete = toggleComplete;
window.deleteTodo = deleteTodo;

// Initial render for any pre‑loaded todos
renderTodos();
