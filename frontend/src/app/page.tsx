"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { CheckCircle, Calendar, Flag, Tag, Zap, Clock, Users, BarChart3 } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { PageTransition } from "@/components/layout/PageTransition";

export default function HomePage() {
  const { isAuthenticated, isLoading } = useAuth();

  return (
    <PageTransition className="min-h-screen bg-background">
      {/* Hero Section with animated grid background */}
      <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
        {/* Animated grid background with light gray lines */}
        <div className="absolute inset-0 z-0 bg-[#000000] [mask-image:radial-gradient(ellipse_at_center,white,transparent)]">
          <div className="absolute inset-0 bg-[linear-gradient(to_right,#d1d5db_1px,transparent_1px),linear-gradient(to_bottom,#d1d5db_1px,transparent_1px)] bg-[size:24px_24px] [mask-image:radial-gradient(ellipse_at_center,black_50%,transparent)] animate-grid-move"></div>
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col items-center justify-center text-center px-4 max-w-4xl w-full">
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold font-sans mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-300">
            Manage Tasks Smarter with AI
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-2xl">
            Experience the future of task management with intelligent automation and AI-powered insights
          </p>
          <div className="flex flex-col sm:flex-row gap-4 fade-in-up">
            {isLoading ? (
              <Button size="lg" disabled className="bg-blue-600 text-white text-base sm:text-lg px-8 py-4 rounded-lg text-lg">
                Loading...
              </Button>
            ) : isAuthenticated ? (
              <Link href="/dashboard">
                <Button size="lg" className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white px-8 py-4 rounded-lg text-lg hover-glow btn-hover-scale">
                  Go to Dashboard
                </Button>
              </Link>
            ) : (
              <Link href="/auth/signup">
                <Button size="lg" className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white px-8 py-4 rounded-lg text-lg hover-glow btn-hover-scale">
                  Get Started — Free
                </Button>
              </Link>
            )}
            <Link href="/#features">
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white/10 px-8 py-4 rounded-lg text-lg btn-hover-scale">
                Learn More
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section - Updated with proper styling */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 fade-in-up">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16 text-white fade-in-up">Powerful Features</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            <Card className="bg-gray-900 border border-gray-700 rounded-2xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up rounded-16px">
              <div className="p-3 rounded-full bg-blue-900/50 mb-4 inline-block">
                <CheckCircle className="h-6 w-6 text-blue-400" />
              </div>
              <CardHeader className="p-0">
                <CardTitle className="text-lg text-white">Smart Task Management</CardTitle>
                <CardDescription className="text-sm text-gray-400">Organize and prioritize your tasks with ease</CardDescription>
              </CardHeader>
              <CardContent className="p-0 pt-2">
                <p className="text-gray-300">Create, update, and manage tasks with intuitive controls and smart defaults.</p>
              </CardContent>
            </Card>

            <Card className="bg-gray-900 border border-gray-700 rounded-2xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up rounded-16px">
              <div className="p-3 rounded-full bg-blue-900/50 mb-4 inline-block">
                <Calendar className="h-6 w-6 text-blue-400" />
              </div>
              <CardHeader className="p-0">
                <CardTitle className="text-lg text-white">Due Dates & Reminders</CardTitle>
                <CardDescription className="text-sm text-gray-400">Never miss a deadline again</CardDescription>
              </CardHeader>
              <CardContent className="p-0 pt-2">
                <p className="text-gray-300">Set due dates and receive timely reminders to stay on track with your goals.</p>
              </CardContent>
            </Card>

            <Card className="bg-gray-900 border border-gray-700 rounded-2xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up rounded-16px">
              <div className="p-3 rounded-full bg-blue-900/50 mb-4 inline-block">
                <Flag className="h-6 w-6 text-blue-400" />
              </div>
              <CardHeader className="p-0">
                <CardTitle className="text-lg text-white">Priority Levels</CardTitle>
                <CardDescription className="text-sm text-gray-400">Focus on what matters most</CardDescription>
              </CardHeader>
              <CardContent className="p-0 pt-2">
                <p className="text-gray-300">Assign priority levels to tasks and tackle the most important items first.</p>
              </CardContent>
            </Card>

            <Card className="bg-gray-900 border border-gray-700 rounded-2xl p-6 hover:shadow-lg hover-lift transition-all duration-300 cursor-pointer fade-in-up rounded-16px">
              <div className="p-3 rounded-full bg-blue-900/50 mb-4 inline-block">
                <Tag className="h-6 w-6 text-blue-400" />
              </div>
              <CardHeader className="p-0">
                <CardTitle className="text-lg text-white">Tag Organization</CardTitle>
                <CardDescription className="text-sm text-gray-400">Categorize and filter your tasks</CardDescription>
              </CardHeader>
              <CardContent className="p-0 pt-2">
                <p className="text-gray-300">Use tags to organize tasks by project, context, or any custom category.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16 text-white">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-gray-800 mb-4">
                <span className="text-2xl font-bold text-white">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">Create</h3>
              <p className="text-gray-400">Add tasks with details, due dates, and priorities</p>
            </div>
            <div className="text-center">
              <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-gray-800 mb-4">
                <span className="text-2xl font-bold text-white">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">Organize</h3>
              <p className="text-gray-400">Categorize and prioritize your tasks</p>
            </div>
            <div className="text-center">
              <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-gray-800 mb-4">
                <span className="text-2xl font-bold text-white">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">Track</h3>
              <p className="text-gray-400">Monitor progress and get insights</p>
            </div>
            <div className="text-center">
              <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-gray-800 mb-4">
                <span className="text-2xl font-bold text-white">4</span>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-white">Achieve</h3>
              <p className="text-gray-400">Complete tasks and reach your goals</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold mb-6 text-white">Ready to Transform Your Productivity?</h2>
          <p className="text-lg text-gray-400 mb-10 max-w-2xl mx-auto">
            Join thousands of users who have revolutionized their task management with TASKAPP.
          </p>
          {isLoading ? (
            <Button size="lg" disabled className="bg-gradient-to-r from-blue-600 to-cyan-500 text-white text-lg px-8 py-4 rounded-lg">
              Loading...
            </Button>
          ) : isAuthenticated ? (
            <Link href="/dashboard">
              <Button size="lg" className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white text-lg px-8 py-4 rounded-lg hover-glow btn-hover-scale">
                Go to Dashboard
              </Button>
            </Link>
          ) : (
            <Link href="/auth/signup">
              <Button size="lg" className="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-700 hover:to-cyan-600 text-white text-lg px-8 py-4 rounded-lg hover-glow btn-hover-scale">
                Start Free Trial
              </Button>
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-400">
          <p>TASKAPP • Smart Task Management • Powered by AI</p>
        </div>
      </footer>
    </PageTransition>
  );
}