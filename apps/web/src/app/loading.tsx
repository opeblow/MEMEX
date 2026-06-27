export default function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-white/10 border-t-white/30" />
        <p className="text-sm text-white/30">Loading</p>
      </div>
    </div>
  );
}
