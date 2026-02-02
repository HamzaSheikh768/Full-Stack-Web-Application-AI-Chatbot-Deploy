'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const router = useRouter();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
      router.push('/dashboard'); // Redirect to dashboard after login
      router.refresh(); // Refresh to update UI
    } catch (err: any) {
      setError(err.message || 'Failed to login. Please check your credentials.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md bg-card border border-border rounded-2xl">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-center text-foreground">Welcome Back</CardTitle>
        <CardDescription className="text-center text-muted-foreground">
          Enter your credentials to access your account
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <div className="p-3 bg-destructive/10 border border-destructive text-destructive rounded-lg text-sm animate-shake">
              {error}
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="email" className="text-foreground">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
              className="rounded-lg border border-input bg-background px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:ring-1 hover:ring-blue-300"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password" className="text-foreground">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              className="rounded-lg border border-input bg-background px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 hover:ring-1 hover:ring-blue-300"
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col">
          <Button
            type="submit"
            className="w-full rounded-lg bg-blue-600 hover:bg-blue-700 text-white py-6 text-base transition-all duration-200 hover:scale-105 hover:ring-2 hover:ring-blue-500/30"
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </Button>

          <div className="mt-4 text-center text-sm text-muted-foreground">
            Don't have an account?{' '}
            <Link
              href="/auth/signup"
              className="font-semibold text-blue-600 hover:underline hover:text-blue-700 transition-colors"
            >
              Sign up
            </Link>
          </div>
        </CardFooter>
      </form>
    </Card>
  );
}