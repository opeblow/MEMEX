export { motion, AnimatePresence, type Variants, type Transition } from "framer-motion";

export { pageTransition } from "./page-transition";
export {
  emergeVariant,
  dissolveVariant,
  materializeVariant,
  staggerContainer,
  staggerItem,
  scrollReveal,
  letterAssemble,
  clipReveal,
  scaleIn,
} from "./variants";
export { transitionConfig } from "./config";
export { AnimationProvider, useAnimationContext } from "./animation-provider";
