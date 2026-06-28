"use client";

import { ChatSkeleton } from "@/components/ui/loading-skeleton";
import { useUIStore } from "@/lib/stores/ui-store";
import dynamic from "next/dynamic";

const AIChat = dynamic(() => import("@/components/chat/ai-chat").then((m) => m.AIChat), {
  ssr: false,
  loading: () => <ChatSkeleton />,
});

export default function ChatPage() {
  const activeProjectId = useUIStore((s) => s.activeProjectId);
  const projectId = activeProjectId || "default";

  return (
    <div className="h-[calc(100vh-4rem)]">
      <AIChat projectId={projectId} />
    </div>
  );
}
