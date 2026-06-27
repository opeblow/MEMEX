import type { Variants } from "framer-motion";

export const emergeVariant: Variants = {
  hidden: {
    opacity: 0,
    y: 10,
    scale: 0.96,
    filter: "blur(2px)",
  },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    filter: "blur(0px)",
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.5,
    },
  },
};

export const dissolveVariant: Variants = {
  hidden: {
    opacity: 1,
    scale: 1,
    filter: "blur(0px)",
  },
  visible: {
    opacity: 0,
    scale: 0.96,
    filter: "blur(4px)",
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.3,
    },
  },
};

export const materializeVariant: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.9,
    filter: "blur(8px) brightness(1.5)",
  },
  visible: {
    opacity: 1,
    scale: 1,
    filter: "blur(0px) brightness(1)",
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.6,
    },
  },
};

export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

export const staggerItem: Variants = {
  hidden: {
    opacity: 0,
    y: 12,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.4,
    },
  },
};

export const scrollReveal: Variants = {
  hidden: {
    opacity: 0,
    y: 40,
    scale: 0.95,
  },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.8,
    },
  },
};

export const letterAssemble: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.5,
    filter: "blur(10px)",
    y: 20,
  },
  visible: {
    opacity: 1,
    scale: 1,
    filter: "blur(0px)",
    y: 0,
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.6,
    },
  },
};

export const clipReveal: Variants = {
  hidden: {
    clipPath: "inset(0 0 100% 0)",
  },
  visible: {
    clipPath: "inset(0 0 0% 0)",
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 1.2,
    },
  },
};

export const scaleIn: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.8,
    filter: "blur(4px)",
  },
  visible: {
    opacity: 1,
    scale: 1,
    filter: "blur(0px)",
    transition: {
      type: "tween",
      ease: [0.16, 1, 0.3, 1],
      duration: 0.7,
    },
  },
};
