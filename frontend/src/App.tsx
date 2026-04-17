import { HashRouter, BrowserRouter, Routes, Route } from 'react-router-dom';
import { InputPage } from './pages/InputPage';
import { ResultPage } from './pages/ResultPage';

const IS_DEMO = import.meta.env.VITE_DEMO_MODE === 'true';
const Router = IS_DEMO ? HashRouter : BrowserRouter;

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<InputPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </Router>
  );
}
