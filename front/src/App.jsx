import { useState } from "react";

function App() {
  const [character, setCharacter] = useState("");
  const [topic, setTopic] = useState("");
  const [result, setResult] = useState("");

  const generate = async () => {
    const response = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ character, topic }),
    });

    const data = await response.json();
    setResult(data.result); // <-- записываем результат
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Генератор сценариев</h1>

      <div>
        <label>Персонаж: </label>
        <input
          value={character}
          onChange={(e) => setCharacter(e.target.value)}
        />
      </div>

      <div>
        <label>Тема: </label>
        <input
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
      </div>

      <button onClick={generate}>Сгенерировать</button>

      <h2>Результат:</h2>
      <pre>{result}</pre>
    </div>
  );
}

export default App;
