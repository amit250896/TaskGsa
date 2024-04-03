import React, { useState } from 'react';

function TodoList() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  const addTodo = () => {
    if (newTodo.trim() !== '') {
      setTodos([...todos, newTodo]);
      setNewTodo('');
    }
  };

  const deleteTodo = (index) => {
    const updatedTodos = [...todos];
    updatedTodos.splice(index, 1);
    setTodos(updatedTodos);
  };

  const updateTodo = (index, updatedText) => {
    const updatedTodos = [...todos];
    updatedTodos[index] = updatedText;
    setTodos(updatedTodos);
  };

  return (
    <div>
      <h3>To Do List</h3>
      <ul>
        {todos.map((todo, index) => (
          <li key={index}>
            {todo}
            <button onClick={() => deleteTodo(index)}>Delete</button>
            <button onClick={() => {
              const updatedText = prompt('Enter updated text:', todo);
              if (updatedText !== null) {
                updateTodo(index, updatedText);
              }
            }}>Update</button>
          </li>
        ))}
      </ul>
      <div>
        <input
          type="text"
          placeholder="Add new todo"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
        />
        <button onClick={addTodo}>Add</button>
      </div>
    </div>
  );
}

export default TodoList;

