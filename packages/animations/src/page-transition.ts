import type { Variants } from "framer-motion";

export const pageTransition: Variants = {
  initial: {
    opacity: 0,
    y: 20,
    filter: "blur(4px)",
  },
  animate: {
    opacity: 1,
    y: 0,
    filter: "blur(0px)",
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.4,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.98,
    filter: "blur(4px)",
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.2,
    },
  },
};
