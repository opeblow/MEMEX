import type { Transition } from "framer-motion";

export const transitionConfig: Transition = {
  type: "tween",
  ease: [0.16, 1, 0.3, 1],
  duration: 0.4,
};

export const springConfig: Transition = {
  type: "spring",
  stiffness: 300,
  damping: 30,
};

export const emergeTiming = {
  duration: 0.5,
  ease: [0.16, 1, 0.3, 1],
};

export const dissolveTiming = {
  duration: 0.3,
  ease: [0.16, 1, 0.3, 1],
};

export const hoverTransition: Transition = {
  type: "tween",
  duration: 0.15,
  ease: "easeOut",
};
