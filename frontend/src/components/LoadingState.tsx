export function LoadingState() {
  return (
    <div className="max-w-3xl mx-auto p-8 space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="bg-white rounded-xl p-6 shadow-sm animate-pulse">
          <div className="h-6 bg-slate-200 rounded w-1/3 mb-4" />
          <div className="h-10 bg-slate-200 rounded w-1/2" />
        </div>
      ))}
    </div>
  );
}
