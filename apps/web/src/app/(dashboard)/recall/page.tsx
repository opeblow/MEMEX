"use client";

import { motion } from "framer-motion";

export default function RecallPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
    >
      <p className="text-sm text-white/40">Recall UI Phase 2</p>
    </motion.div>
  );
}
