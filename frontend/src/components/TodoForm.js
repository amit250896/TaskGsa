import React, { useState } from 'react';

function TodoForm() {
  const [description, setDescription] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Implement form submission logic here
  };

  return (
    <div>
      <h3>Add Todo</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter todo description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button type="submit">Add Todo</button>
      </form>
    </div>
  );
}

export default TodoForm;
