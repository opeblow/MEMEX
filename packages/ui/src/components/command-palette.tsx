"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Search } from "lucide-react";
import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";
import { cn } from "../lib/cn";

interface CommandItem {
  id: string;
  label: string;
  description?: string;
  icon?: ReactNode;
  onSelect: () => void;
  shortcut?: string;
}

interface CommandPaletteProps {
  open: boolean;
  onClose: () => void;
  items: CommandItem[];
  placeholder?: string;
}

export function CommandPalette({
  open,
  onClose,
  items,
  placeholder = "Search memories, actions, and more...",
}: CommandPaletteProps) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const filtered = query
    ? items.filter(
        (item) =>
          item.label.toLowerCase().includes(query.toLowerCase()) ||
          item.description?.toLowerCase().includes(query.toLowerCase()),
      )
    : items;

  useEffect(() => {
    if (open) {
      inputRef.current?.focus();
      setSelectedIndex(0);
    }
  }, [open]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((i) => Math.min(i + 1, filtered.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((i) => Math.max(i - 1, 0));
      } else if (e.key === "Enter" && filtered[selectedIndex]) {
        filtered[selectedIndex].onSelect();
        onClose();
      } else if (e.key === "Escape") {
        onClose();
      }
    },
    [filtered, selectedIndex, onClose],
  );

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: -10 }}
            transition={{ type: "tween", ease: [0.16, 1, 0.3, 1], duration: 0.2 }}
            className="fixed left-[50%] top-[15%] z-50 w-full max-w-xl translate-x-[-50%]"
          >
            <div className="overflow-hidden rounded-xl border border-white/10 bg-[#0A0A0A] shadow-2xl">
              <div className="flex items-center gap-3 border-b border-white/5 px-4 py-3">
                <Search className="h-4 w-4 text-white/30" />
                <input
                  ref={inputRef}
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setSelectedIndex(0);
                  }}
                  onKeyDown={handleKeyDown}
                  placeholder={placeholder}
                  className="flex-1 bg-transparent text-sm text-white outline-none placeholder:text-white/20"
                />
              </div>
              <div className="max-h-72 overflow-y-auto p-2">
                {filtered.length === 0 && (
                  <p className="p-4 text-center text-sm text-white/30">No results found</p>
                )}
                {filtered.map((item, index) => (
                  <button
                    type="button"
                    key={item.id}
                    onClick={() => {
                      item.onSelect();
                      onClose();
                    }}
                    onMouseEnter={() => setSelectedIndex(index)}
                    className={cn(
                      "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition-colors",
                      index === selectedIndex
                        ? "bg-white/10 text-white"
                        : "text-white/60 hover:text-white",
                    )}
                  >
                    {item.icon && (
                      <span className="flex h-5 w-5 items-center justify-center">{item.icon}</span>
                    )}
                    <div className="flex-1">
                      <p className="text-sm font-medium">{item.label}</p>
                      {item.description && (
                        <p className="text-xs text-white/30">{item.description}</p>
                      )}
                    </div>
                    {item.shortcut && (
                      <kbd className="hidden rounded border border-white/5 bg-white/5 px-1.5 py-0.5 text-[10px] text-white/30 sm:inline-block">
                        {item.shortcut}
                      </kbd>
                    )}
                  </button>
                ))}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
