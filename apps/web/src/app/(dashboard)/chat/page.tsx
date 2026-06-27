"use client";

import dynamic from "next/dynamic";
import { useUIStore } from "@/lib/stores/ui-store";

const AIChat = dynamic(
  () => import("@/components/chat/ai-chat").then((m) => m.AIChat),
  { ssr: false },
);

export default function ChatPage() {
  const activeProjectId = useUIStore((s) => s.activeProjectId);
  const projectId = activeProjectId || "default";

  return (
    <div className="h-[calc(100vh-4rem)]">
      <AIChat projectId={projectId} />
    </div>
  );
}
