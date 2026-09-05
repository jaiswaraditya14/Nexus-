import { Link } from 'react-router-dom';

export function Register() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-6">
      <section className="w-full max-w-md rounded-xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
        <p className="mb-2 text-sm font-semibold text-indigo-600">MeetAI</p>
        <h1 className="text-2xl font-bold text-slate-900">Register</h1>
        <p className="mt-4 text-slate-600">Account creation UI will be implemented on Day 3.</p>
        <Link className="mt-6 inline-block text-sm font-medium text-indigo-600" to="/login">Back to login →</Link>
      </section>
    </main>
  );
}

