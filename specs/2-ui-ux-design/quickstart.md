# Todo App Frontend Quickstart

## Prerequisites
- Node.js 18+
- npm or yarn
- Access to the backend API (FastAPI server running)

## Setup
1. Clone the repository
2. Navigate to the frontend directory: `cd frontend`
3. Install dependencies: `npm install` or `yarn install`
4. Copy `.env.example` to `.env.local` and add your environment variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000  # Auth URL
   ```
5. Run `npm run dev` to start the development server

## Available Scripts
- `npm run dev`: Start development server on http://localhost:3000
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run linter
- `npm run test`: Run tests
- `npm run prettier`: Format code

## Folder Structure
```
/frontend
├── /app                 # Next.js App Router pages
│   ├── /                # Landing page
│   ├── /dashboard       # Dashboard page
│   ├── /tasks           # Tasks management page
│   ├── /ai-chat         # AI chat interface
│   ├── /auth            # Authentication pages
│   │   ├── /signin
│   │   └── /signup
│   └── /layout.tsx      # Root layout
├── /components          # Reusable React components
│   ├── /ui              # Base UI components (Button, Card, etc.)
│   ├── /layout          # Layout components (Navbar, Sidebar, etc.)
│   ├── /hero            # Landing page components
│   ├── /chat            # Chat interface components
│   ├── /dashboard       # Dashboard components
│   └── /tasks           # Task management components
├── /lib                 # Utility functions and constants
│   ├── /api.ts          # API client and requests
│   ├── /theme.ts        # Theme context and utilities
│   └── /types.ts        # Type definitions
├── /hooks               # Custom React hooks
├── /styles              # Global styles and Tailwind configuration
│   └── /globals.css     # Global styles
├── /public              # Static assets
└── /types               # Global type definitions
```

## Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API base URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Authentication service URL

## Development Workflow
1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes following the component structure
3. Test locally: `npm run dev`
4. Run linter: `npm run lint`
5. Commit changes with conventional commit format
6. Push and create a pull request

## Component Development
- All new UI components should go in `/components/ui`
- Layout components (Navbar, Sidebar) go in `/components/layout`
- Page-specific components go in their respective folders
- Use TypeScript for all components
- Follow Tailwind CSS utility-first approach
- Implement responsive design using Tailwind's responsive prefixes

## Styling Guidelines
- Use the color palette defined in the specification:
  - Dark mode: #000000 background, #E5E7EB text-primary, #1E3A8A accent
  - Light mode: #FFFFFF background, #111827 text-primary, #1E40AF accent
- Apply consistent spacing using Tailwind's spacing scale
- Use the defined animations: 200-300ms transitions, 400ms page transitions
- Implement dark/light mode using the `dark:` prefix

## API Integration
- All API calls should be made through the client in `/lib/api.ts`
- Handle authentication tokens automatically
- Implement proper error handling and loading states
- Follow the API contracts defined in `/contracts/`

## Testing
- Unit tests for utility functions
- Component tests for UI components
- Integration tests for API interactions
- Accessibility testing using automated tools