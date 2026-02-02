import { motion } from 'framer-motion';

// Page transition variants
export const pageVariants = {
  initial: { opacity: 0, y: 8 },
  in: { opacity: 1, y: 0 },
  out: { opacity: 0, y: -8 },
};

export const pageTransition = {
  duration: 0.4,
  ease: 'easeInOut',
};

// Fade in up animation
export const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: { duration: 0.4, ease: 'easeInOut' },
};

// Stagger children animations
export const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

export const child = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.3, ease: 'easeInOut' } },
};

// Card hover animation
export const cardHover = {
  rest: {
    y: 0,
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
  },
  hover: {
    y: -6,
    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04), 0 0 0 2px rgba(37, 99, 235, 0.3)'
  },
};

// Button hover animation
export const buttonHover = {
  rest: { scale: 1 },
  hover: { scale: 1.05 },
};

// Scale glow animation
export const scaleGlow = {
  rest: {
    scale: 1,
    boxShadow: '0 0 0 0 rgba(37, 99, 235, 0)'
  },
  hover: {
    scale: 1.02,
    boxShadow: '0 0 10px 2px rgba(37, 99, 235, 0.3)',
    transition: { duration: 0.2, ease: 'easeInOut' }
  },
};

// Motion components with default animations
export const MotionDiv = motion.div;
export const MotionSection = motion.section;
export const MotionHeader = motion.header;
export const MotionButton = motion.button;
export const MotionCard = motion.div;