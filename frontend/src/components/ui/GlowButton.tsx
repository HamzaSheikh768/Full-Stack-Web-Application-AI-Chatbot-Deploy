import { Button, ButtonProps } from '@/components/ui/button';
import { motion } from 'framer-motion';

interface GlowButtonProps extends ButtonProps {
  glowIntensity?: 'sm' | 'md' | 'lg';
}

export const GlowButton = ({
  children,
  glowIntensity = 'md',
  className = '',
  ...props
}: GlowButtonProps) => {
  const glowClass = {
    sm: 'hover:shadow-[0_0_8px_2px_rgba(37,99,235,0.3)]',
    md: 'hover:shadow-[0_0_10px_2px_rgba(37,99,235,0.3)]',
    lg: 'hover:shadow-[0_0_15px_3px_rgba(37,99,235,0.3)]'
  }[glowIntensity];

  return (
    <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
      <Button
        className={`${className} transition-all duration-200 ease-in-out ${glowClass}`}
        {...props}
      >
        {children}
      </Button>
    </motion.div>
  );
};