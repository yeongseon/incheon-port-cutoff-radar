import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { InputPage } from './pages/InputPage';
import { ResultPage } from './pages/ResultPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<InputPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}
