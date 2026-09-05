import { NavLink, Navigate, Route, Routes } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { MeetingRoom } from './pages/MeetingRoom';
import { History } from './pages/History';

const navigation = [
  { label: 'Dashboard', to: '/' },
  { label: 'History', to: '/history' },
];

function Shell() {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <NavLink className="text-xl font-bold text-indigo-600" to="/">MeetAI</NavLink>
          <nav className="flex gap-5 text-sm text-slate-600">
            {navigation.map((item) => <NavLink key={item.to} to={item.to}>{item.label}</NavLink>)}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-10">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/history" element={<History />} />
          <Route path="/meetings/:meetingId" element={<MeetingRoom />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/*" element={<Shell />} />
      </Routes>
    </BrowserRouter>
  );
}

