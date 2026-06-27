"use client";

import { useEffect } from "react";

type Modifier = "ctrl" | "meta" | "alt" | "shift";

interface Shortcut {
  key: string;
  modifiers?: Modifier[];
  handler: (e: KeyboardEvent) => void;
  preventDefault?: boolean;
}

export function useKeyboardShortcut(shortcuts: Shortcut[]) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      for (const shortcut of shortcuts) {
        const modifiers = shortcut.modifiers ?? [];
        const mods = {
          ctrl: e.ctrlKey,
          meta: e.metaKey,
          alt: e.altKey,
          shift: e.shiftKey,
        };

        if (e.key.toLowerCase() !== shortcut.key.toLowerCase()) continue;

        const allModsMatch = modifiers.every((m) => mods[m]);
        const noExtraMods = true;

        if (allModsMatch && noExtraMods) {
          if (shortcut.preventDefault) {
            e.preventDefault();
          }
          shortcut.handler(e);
          return;
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [shortcuts]);
}
