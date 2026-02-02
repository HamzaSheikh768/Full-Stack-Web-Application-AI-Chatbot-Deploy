import SignupForm from '@/components/auth/SignupForm';

export default function SignupPage() {
  return (
    <div className="min-h-screen flex bg-background">
      {/* Left side - Motivational content */}
      <div className="hidden md:flex w-1/2 bg-gradient-to-br from-blue-900 via-purple-900 to-gray-900 text-white p-12 flex-col justify-center">
        <div className="max-w-md">
          <h1 className="text-4xl font-bold mb-6">Join TASKAPP Today</h1>
          <p className="text-xl text-gray-200 mb-8">
            Transform your productivity with our AI-powered task management platform. Start your journey to better organization.
          </p>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="bg-blue-500 rounded-full p-2 mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-lg">AI-powered task management</p>
            </div>
            <div className="flex items-start">
              <div className="bg-blue-500 rounded-full p-2 mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-lg">Real-time collaboration</p>
            </div>
            <div className="flex items-start">
              <div className="bg-blue-500 rounded-full p-2 mr-4">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <p className="text-lg">Secure & private</p>
            </div>
          </div>
        </div>
      </div>

      {/* Right side - Signup Form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-4 md:p-12">
        <div className="w-full max-w-md">
          <div className="text-center md:hidden mb-8">
            <h1 className="text-3xl font-bold text-foreground">Create Account</h1>
            <p className="text-muted-foreground">Join us today</p>
          </div>
          <SignupForm />
        </div>
      </div>
    </div>
  );
}