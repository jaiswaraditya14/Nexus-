import { Link } from 'react-router-dom';

export function Dashboard() {
  return (
    <section>
      <p className="text-sm font-semibold uppercase tracking-wide text-indigo-600">Workspace</p>
      <h1 className="mt-2 text-3xl font-bold text-slate-900">Dashboard</h1>
      <div className="mt-8 rounded-xl border border-dashed border-slate-300 bg-white p-8">
        <h2 className="text-lg font-semibold text-slate-900">Meeting management placeholder</h2>
        <p className="mt-2 text-slate-600">Meeting CRUD and authenticated access will be added in the next implementation phase.</p>
        <Link className="mt-5 inline-block rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white" to="/meetings/foundation-demo">Open room shell</Link>
      </div>
    </section>
  );
}

