'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Moon, Sun, Menu, LogIn, User, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger, SheetHeader, SheetTitle } from '@/components/ui/sheet';
import { useAuth } from '@/contexts/AuthContext';
import { useTheme } from '@/lib/theme';

const Navbar = () => {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const { isAuthenticated, user, logout } = useAuth();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const navigationLinks = [
    { name: 'Dashboard', href: '/dashboard' as const },
    { name: 'Tasks', href: '/tasks' as const },
    { name: 'AI Chat', href: '/chat' as const },
  ];

  const isActive = (href: string) => pathname === href;

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const handleLogout = () => {
    logout();
  };

  // User is authenticated if user exists and not loading

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b bg-white/80 dark:bg-black/80 backdrop-blur-sm border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4 max-w-screen-xl">
        <div className="flex h-[72px] items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <Link
              href="/"
              className="text-2xl font-bold text-blue-600 dark:text-blue-400"
              aria-label="TASKAPP Home"
            >
              TASKAPP
            </Link>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center space-x-8" aria-label="Main navigation">
            {navigationLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`text-sm font-medium transition-all duration-300 hover:text-blue-600 dark:hover:text-blue-400 hover:translate-x-1 ${
                  isActive(link.href)
                    ? 'text-blue-600 dark:text-blue-400'
                    : 'text-gray-600 dark:text-gray-300'
                }`}
                aria-current={isActive(link.href) ? "page" : undefined}
              >
                {link.name}
              </Link>
            ))}
          </nav>

          {/* Right-aligned container for auth and theme toggle */}
          <div className="flex items-center space-x-4">
            {/* Auth Buttons */}
            {!isAuthenticated ? (
              <div className="flex items-center space-x-2">
                <Link href="/auth/login">
                  <Button variant="outline" size="sm" className="flex items-center">
                    <LogIn className="h-4 w-4 mr-2" />
                    Login
                  </Button>
                </Link>
                <Link href="/auth/signup">
                  <Button size="sm" className="flex items-center">
                    <User className="h-4 w-4 mr-2" />
                    Sign Up
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600 dark:text-gray-300 hidden sm:block">
                  {user?.email?.split('@')[0]}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </div>
            )}

            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="h-8 w-8"
            >
              {mounted && theme === 'dark' ? (
                <Sun className="h-5 w-5 text-yellow-500" aria-hidden="true" />
              ) : (
                <Moon className="h-5 w-5 text-gray-600" aria-hidden="true" />
              )}
            </Button>

            {/* Mobile Menu */}
            <Sheet>
              <SheetTrigger asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  className="md:hidden h-8 w-8"
                  aria-label="Open menu"
                >
                  <Menu className="h-5 w-5" aria-hidden="true" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[300px] bg-white dark:bg-gray-900">
                <SheetHeader>
                  <SheetTitle>Navigation Menu</SheetTitle>
                </SheetHeader>
                <div className="flex flex-col space-y-6 mt-6">
                  {navigationLinks.map((link) => (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={`text-lg font-medium ${
                        isActive(link.href)
                          ? 'text-blue-600 dark:text-blue-400'
                          : 'text-gray-600 dark:text-gray-300'
                      }`}
                      aria-current={isActive(link.href) ? "page" : undefined}
                    >
                      {link.name}
                    </Link>
                  ))}

                  {/* Mobile Auth Section */}
                  {!isAuthenticated ? (
                    <div className="space-y-3 pt-4">
                      <Link href="/auth/login">
                        <Button variant="outline" className="w-full justify-start">
                          <LogIn className="h-4 w-4 mr-2" />
                          Login
                        </Button>
                      </Link>
                      <Link href="/auth/signup">
                        <Button className="w-full justify-start">
                          <User className="h-4 w-4 mr-2" />
                          Sign Up
                        </Button>
                      </Link>
                    </div>
                  ) : (
                    <div className="pt-4">
                      <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
                        Signed in as: {user?.email?.split('@')[0]}
                      </p>
                      <Button
                        variant="outline"
                        className="w-full justify-start"
                        onClick={handleLogout}
                      >
                        <LogOut className="h-4 w-4 mr-2" />
                        Logout
                      </Button>
                    </div>
                  )}

                  <Button
                    variant="outline"
                    onClick={toggleTheme}
                    className="mt-4 w-full justify-center"
                    aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
                  >
                    {theme === 'dark' ? 'Switch to Light' : 'Switch to Dark'}
                  </Button>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;