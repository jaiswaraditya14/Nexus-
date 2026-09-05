import { Link } from 'react-router-dom';

export function Login() {
  return <AuthPlaceholder title="Login" prompt="Authentication UI will be implemented on Day 3." link="/register" linkLabel="Create an account" />;
}

function AuthPlaceholder({ title, prompt, link, linkLabel }: { title: string; prompt: string; link: string; linkLabel: string }) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-6">
      <section className="w-full max-w-md rounded-xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
        <p className="mb-2 text-sm font-semibold text-indigo-600">MeetAI</p>
        <h1 className="text-2xl font-bold text-slate-900">{title}</h1>
        <p className="mt-4 text-slate-600">{prompt}</p>
        <Link className="mt-6 inline-block text-sm font-medium text-indigo-600" to={link}>{linkLabel} →</Link>
      </section>
    </main>
  );
}

