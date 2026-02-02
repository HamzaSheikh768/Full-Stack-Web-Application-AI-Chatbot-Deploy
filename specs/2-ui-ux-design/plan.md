# Todo App – Development Plan (s.plan.md)
Execution roadmap for 4-page Todo App (Landing, Dashboard, Tasks, AI Chat)
Built with: Next.js 16 (App Router), TypeScript, Tailwind CSS, dark/light mode
Goal: Modern, minimal, AI-centric UI with smooth animations & responsiveness

## Technical Context

- **Frontend Framework**: Next.js 16 with App Router
- **Styling**: Tailwind CSS with custom extensions
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Charts**: Recharts or CSS-based conic gradients
- **Responsive Design**: Mobile-first approach with breakpoints at 640px and 1024px
- **Theme System**: Dark-first with light mode support using localStorage persistence

### Resolved Unknowns:
- Authentication backend integration: Using existing Better Auth system
- API endpoints for task management: Defined in contracts/frontend-backend-contracts.md
- AI chat backend integration: WebSocket connection to existing chat endpoints

## Constitution Check

Based on `.specify/memory/constitution.md`, this plan adheres to:

- **Modularity**: Components will be organized in reusable modules
- **Maintainability**: Clean code practices with proper documentation
- **Testability**: Components will be designed with testing in mind
- **Performance**: Optimized for fast loading and smooth animations
- **Accessibility**: Proper semantic HTML and ARIA attributes
- **Security**: Secure handling of user data and authentication

## Gates

✅ **Architecture Gate**: Plan follows Next.js App Router patterns and Tailwind CSS best practices
✅ **Integration Gate**: Plan accounts for necessary API integrations
✅ **Security Gate**: Authentication and data handling considerations included

## Phase 0: Research & Resolution of Unknowns

### Research Tasks

1. **Authentication Integration Research**
   - Task: Research how to integrate with existing auth system
   - Current state: Need to understand existing auth endpoints
   - Solution: Coordinate with backend team to document auth API

2. **API Contract Understanding**
   - Task: Map out required API endpoints for task management
   - Current state: Endpoints not clearly defined in frontend context
   - Solution: Create mock API contracts based on requirements

3. **AI Chat Integration Patterns**
   - Task: Research best practices for AI chat interface implementation
   - Current state: AI backend integration specifics unknown
   - Solution: Design interface based on standard chat patterns

## Phase 1: Design & Contracts

### Data Model (data-model.md)

```
User:
  - id: string
  - name: string
  - email: string
  - themePreference: 'dark'|'light'
  - createdAt: timestamp
  - updatedAt: timestamp

Task:
  - id: string
  - userId: string (foreign key)
  - title: string
  - description: string
  - completed: boolean
  - priority: 'high'|'medium'|'low'
  - createdAt: timestamp
  - updatedAt: timestamp

Conversation:
  - id: string
  - userId: string (foreign key)
  - title: string
  - createdAt: timestamp
  - updatedAt: timestamp

Message:
  - id: string
  - conversationId: string (foreign key)
  - userId: string (foreign key)
  - role: 'user'|'assistant'
  - content: string
  - createdAt: timestamp
```

### API Contracts (contracts/frontend-backend-contracts.md)

```
Authentication:
  POST /api/auth/login
    Request: {email: string, password: string}
    Response: {token: string, user: User}
  POST /api/auth/register
    Request: {name: string, email: string, password: string}
    Response: {token: string, user: User}
  GET /api/auth/me
    Headers: Authorization: Bearer {token}
    Response: {user: User}

Tasks:
  GET /api/tasks
    Headers: Authorization: Bearer {token}
    Response: {tasks: Task[]}
  POST /api/tasks
    Headers: Authorization: Bearer {token}
    Request: {title: string, description?: string, priority?: string}
    Response: {task: Task}
  PUT /api/tasks/{id}
    Headers: Authorization: Bearer {token}
    Request: {title?: string, description?: string, completed?: boolean, priority?: string}
    Response: {task: Task}
  DELETE /api/tasks/{id}
    Headers: Authorization: Bearer {token}
    Response: {success: boolean}

Dashboard:
  GET /api/dashboard/stats
    Headers: Authorization: Bearer {token}
    Response: {stats: {total: number, completed: number, pending: number, high: number, medium: number, low: number}}

Chat:
  POST /api/chat
    Headers: Authorization: Bearer {token}
    Request: {message: string, conversationId?: string}
    Response: {response: string, conversationId: string}
```

### Quickstart Guide (quickstart.md)

```
# Todo App Frontend Quickstart

## Prerequisites
- Node.js 18+
- npm or yarn

## Setup
1. Clone the repository
2. Run `npm install` to install dependencies
3. Copy `.env.example` to `.env.local` and add your environment variables
4. Run `npm run dev` to start the development server

## Available Scripts
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run linter
- `npm run test`: Run tests

## Folder Structure
- `/app`: Next.js App Router pages
- `/components`: Reusable React components
- `/lib`: Utility functions and constants
- `/styles`: Global styles and Tailwind configuration
- `/hooks`: Custom React hooks
```

## Phase 1: Implementation Plan

### 1. Project Setup Phase (Day 1–2)
- Install dependencies:
  - `framer-motion` (for smooth page/hero animations)
  - `lucide-react` (icons: sun, moon, etc.)
  - `clsx` / `tailwind-merge` (conditional classes)
  - `recharts` (for donut chart on dashboard)
- Set up Tailwind config:
  - Extend colors (dark: #000000 bg, #1E3A8A accent, etc.)
  - Custom animations (fadeInUp, glow, scaleGlow)
  - Dark mode: class strategy (dark prefix)
- Create folder structure:
  ```
  /app
    / (landing)
    /dashboard
    /tasks
    /ai-chat
    /auth
      /signin
      /signup
  /components
    /ui (Button, Card, Input, etc.)
    /layout (Navbar, Sidebar, Footer, ThemeToggle)
    /hero
    /chat
    /dashboard
    /tasks
  /lib (utils, theme context, api client)
  /hooks (custom hooks)
  /styles (globals, animations)
  ```

### 2. Global Components & Theme Phase (Day 2–4)
- ThemeProvider + ThemeToggle (sun/moon icon, persist in localStorage)
- Navbar: transparent, sticky, backdrop-blur-md, glass effect (backdrop-blur-lg + bg-black/10 dark:bg-black/30)
  - On scroll → subtle shadow/overlay
  - Right: Theme toggle + Profile dropdown (after login)
- Sidebar: fixed left (desktop), drawer on mobile
  - Dark blue/black bg
- Footer: minimal (TASKAPP left, "Smart Task Management" right)
- Global animations:
  - Page wrapper: motion.div with initial={opacity:0, y:8} animate={opacity:1, y:0}
  - Hover: group-hover:scale-102 + shadow/glow
- Responsive utils: mobile (<640px), tablet (640–1024), desktop (>1024)

### 3. Authentication Phase (Day 4–6)
- Pages: /auth/signin & /auth/signup
  - Split layout:
    Left: clean form (rounded inputs, blue focus glow, error shake)
    Right: bold heading + motivational text + gradient/illustration bg
- After login → redirect to /dashboard
- Profile dropdown in navbar: name, email, logout, setting

### 4. Landing Page Phase (Day 6–8)
- Full min-h-screen hero
  - Animated subtle grid background (CSS keyframes: slow moving lines, opacity 0.05–0.08)
    → Option: background with radial-gradient + animated @keyframes moveGrid
  - Content: perfectly centered (flex flex-col items-center justify-center)
  - Heading: text-6xl md:text-7xl lg:text-8xl font-bold/semi-bold, fadeInUp + slide up
  - Subheading: text-xl light gray
  - CTA button: big, gradient border (blue-cyan), hover glow + scale-105
- Other sections: card grid (radius 12–16px)
  - Hover: border animate to accent color + icon rotate/glow
  - No dashboard preview

### 5. Dashboard Page Phase (Day 8–10)
- Padding: px-4 md:px-6 lg:px-8 py-6
- Task Distribution section:
  - Use conic-gradient() donut chart (lightweight, no heavy lib) OR Recharts donut
  - Animated fill (CSS or framer-motion)
  - Hover tooltip: count + %
  - Colors: High (#991b1b–blue mix), Medium (#1d4ed8), Low (#6b7280)
- Fade-in sections with staggerChildren

### 6. Tasks Page Phase (Day 10–12)
- Heading: font-semibold tracking-wide + animated underline (after pseudo element scaleX)
- Task cards: grid or flex, gap-4–6
  - Hover: shadow-lg + border-glow (ring-2 ring-blue-500/30)
  - Add task form: slide-up fade animation
- Drag & drop support (optional later with @dnd-kit)

### 7. AI Chat Page Phase (Day 12–14)
- No navbar → full sidebar + main chat
- Sidebar: fixed, chat history list (hover bg-accent/20)
- Main: message bubbles
  - AI: subtle glow bg + border
  - User: right-aligned, flat
- Typing animation: three bouncing dots
- Input: bottom fixed, rounded, blue focus glow

### 8. Polish & Responsiveness Phase (Day 14–16)
- Mobile fixes:
  - Sidebar → slide-in drawer (hamburger trigger)
  - Navbar: icons only (hide text)
  - Cards → single column
  - Hero text size auto-scale
- Test dark/light toggle smoothness (300ms transition)
- Accessibility: aria-labels, keyboard nav, contrast check
- Performance: lazy load charts/animations

### 9. Final Checks & Integration
- Test all pages/auth flows
- Lighthouse score >90 (perf, accessibility)
- Integrate with backend APIs
- Deploy: Vercel (auto dark mode works great)

## Risk Assessment

- **High Risk**: API integration timeline uncertainty
- **Medium Risk**: AI chat functionality complexity
- **Low Risk**: UI animations performance impact

## Success Metrics

- All pages load in <3 seconds
- Mobile-responsive design validated on all screen sizes
- 90%+ Lighthouse performance score
- Smooth animations without jank
- Proper accessibility scoring