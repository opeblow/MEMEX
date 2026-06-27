import Link from "next/link";
import { Button } from "@memex/ui";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
      <p className="text-6xl font-bold text-white/10">404</p>
      <h1 className="text-2xl font-semibold text-white">Page not found</h1>
      <p className="max-w-sm text-sm text-white/40">
        This memory doesn&apos;t exist. It may have been moved, deleted, or never
        created.
      </p>
      <Link href="/">
        <Button variant="secondary">Return Home</Button>
      </Link>
    </div>
  );
}
