import { cn } from '@/lib/utils';

interface ResponsiveContainerProps {
  children: React.ReactNode;
  className?: string;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
}

export const ResponsiveContainer = ({
  children,
  className = '',
  maxWidth = '2xl'
}: ResponsiveContainerProps) => {
  const maxWidthClass = `max-w-screen-${maxWidth === 'full' ? 'none' : maxWidth}`;

  return (
    <div className={cn(
      "w-full mx-auto px-4 sm:px-6 lg:px-8",
      maxWidthClass,
      className
    )}>
      {children}
    </div>
  );
};

interface ResponsiveGridProps {
  children: React.ReactNode;
  cols?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
  };
  gap?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

export const ResponsiveGrid = ({
  children,
  cols = { sm: 1, md: 2, lg: 3, xl: 4 },
  gap = 'md',
  className = ''
}: ResponsiveGridProps) => {
  const gapClass = {
    sm: 'gap-4',
    md: 'gap-6',
    lg: 'gap-8',
    xl: 'gap-12'
  }[gap];

  const colClasses = [
    cols.sm ? `grid-cols-${cols.sm}` : 'grid-cols-1',
    cols.md ? `md:grid-cols-${cols.md}` : 'md:grid-cols-2',
    cols.lg ? `lg:grid-cols-${cols.lg}` : 'lg:grid-cols-3',
    cols.xl ? `xl:grid-cols-${cols.xl}` : 'xl:grid-cols-4',
  ].join(' ');

  return (
    <div className={cn(
      "grid",
      gapClass,
      colClasses,
      className
    )}>
      {children}
    </div>
  );
};