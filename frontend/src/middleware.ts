import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Continue to the requested route
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};