import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface HoverEffectProps {
  children: ReactNode;
  className?: string;
  glowIntensity?: 'sm' | 'md' | 'lg';
  scaleOnHover?: boolean;
  asChild?: boolean;
}

export const HoverEffect = ({
  children,
  className = '',
  glowIntensity = 'md',
  scaleOnHover = true,
  asChild = false
}: HoverEffectProps) => {
  const glowClass = {
    sm: 'hover:shadow-[0_0_8px_2px_rgba(37,99,235,0.3)]',
    md: 'hover:shadow-[0_0_10px_2px_rgba(37,99,235,0.3)]',
    lg: 'hover:shadow-[0_0_15px_3px_rgba(37,99,235,0.3)]'
  }[glowIntensity];

  const Wrapper = asChild ? motion.div : 'div';
  const wrapperProps = asChild ? { whileHover: { scale: scaleOnHover ? 1.02 : 1 } } : {};

  return (
    <Wrapper
      className={cn(
        "transition-all duration-200 ease-in-out cursor-pointer",
        glowClass,
        scaleOnHover ? "hover:scale-[1.02]" : "",
        className
      )}
      {...wrapperProps}
    >
      {children}
    </Wrapper>
  );
};