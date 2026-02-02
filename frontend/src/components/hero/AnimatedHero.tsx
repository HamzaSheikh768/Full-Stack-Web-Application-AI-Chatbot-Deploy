'use client';

import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import Link from 'next/link';

const AnimatedHero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Dark Mode Background with Animated Grid */}
      <div className="absolute inset-0 bg-black dark:block hidden">
        {/* Static Grid Lines - Pure black background with white grid lines at 10% opacity */}
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px)
            `,
            backgroundSize: '60px 60px'
          }}
        ></div>

        {/* Animated Vertical Lines - 3 lines at 30%, 50%, 70% positions */}
        <div
          className="absolute top-0 h-full w-0.5 bg-gradient-to-b from-transparent via-gray-400 to-transparent"
          style={{
            left: '30%',
            animation: 'moveLine7 7s linear infinite',
            filter: 'blur(1px)'
          }}
        ></div>
        <div
          className="absolute top-0 h-full w-0.5 bg-gradient-to-b from-transparent via-gray-400 to-transparent"
          style={{
            left: '50%',
            animation: 'moveLine8 8s linear infinite',
            animationDelay: '2s',
            filter: 'blur(1px)'
          }}
        ></div>
        <div
          className="absolute top-0 h-full w-0.5 bg-gradient-to-b from-transparent via-gray-400 to-transparent"
          style={{
            left: '70%',
            animation: 'moveLine9 9s linear infinite',
            animationDelay: '4s',
            filter: 'blur(1px)'
          }}
        ></div>

        {/* Gradient Overlays */}
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-transparent to-transparent"></div>
        <div className="absolute inset-0 bg-gradient-to-l from-gray-500/5 via-transparent to-transparent"></div>
      </div>

      {/* Light Mode Background - Simple white background with no animations */}
      <div className="absolute inset-0 bg-white light:block dark:hidden"></div>

      {/* Animation Keyframes */}
      <style jsx>{`
        @keyframes moveLine7 {
          0% {
            top: -20%;
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            top: 100%;
            opacity: 0;
          }
        }

        @keyframes moveLine8 {
          0% {
            top: -20%;
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            top: 100%;
            opacity: 0;
          }
        }

        @keyframes moveLine9 {
          0% {
            top: -20%;
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            top: 100%;
            opacity: 0;
          }
        }
      `}</style>

      {/* Theme Toggle Button */}
      <div className="absolute top-4 right-4 z-20">
        <ThemeToggle />
      </div>

      {/* Content */}
      <div className="relative z-10 text-center max-w-5xl px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-6 leading-tight text-white dark:text-white text-gray-900 light:text-gray-900">
          Master Your Day with <span className="text-blue-400 dark:text-blue-400 text-blue-600 light:text-blue-600">Intelligent Task Automation</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-300 dark:text-gray-300 text-gray-600 light:text-gray-600 mb-8 max-w-2xl mx-auto">
          Create, automate, and track tasks effortlessly. Built for professionals who value clarity and time.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link href="/dashboard">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white dark:text-white text-gray-900 light:text-gray-900 text-base sm:text-lg px-6 py-3 sm:px-8 sm:py-4 rounded-lg btn-hover-scale">
              Get Started — Free
            </Button>
          </Link>
          <Link href="#features">
            <Button size="lg" variant="outline" className="text-white dark:text-white text-gray-900 light:text-gray-900 border-white/30 dark:border-gray-600 border-gray-300 light:border-gray-300 text-base sm:text-lg px-6 py-3 sm:px-8 sm:py-4 rounded-lg btn-hover-scale">
              See how it works
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default AnimatedHero;