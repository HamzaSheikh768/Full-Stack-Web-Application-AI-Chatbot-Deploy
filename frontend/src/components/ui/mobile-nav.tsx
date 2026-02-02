'use client';

import * as React from 'react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Menu } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { ThemeToggle } from '@/components/ui/theme-toggle';

export function MobileNav() {
  const router = useRouter();
  const [open, setOpen] = React.useState(false);

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-6 w-6" />
          <span className="sr-only">Toggle menu</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[300px] sm:w-[400px]">
        <div className="flex flex-col space-y-4 mt-8">
          <ThemeToggle showText={true} />

          {/* Public navigation items */}
          <Link href={'/' as any}>
            <Button variant="outline" className="w-full justify-start">
              Home
            </Button>
          </Link>
          <Link href={'/dashboard' as any}>
            <Button variant="outline" className="w-full justify-start">
              Dashboard
            </Button>
          </Link>
          <Link href={'/tasks' as any}>
            <Button variant="outline" className="w-full justify-start">
              Tasks
            </Button>
          </Link>
          <Link href={'/chat' as any}>
            <Button variant="outline" className="w-full justify-start">
              AI Chat
            </Button>
          </Link>
        </div>
      </SheetContent>
    </Sheet>
  );
}