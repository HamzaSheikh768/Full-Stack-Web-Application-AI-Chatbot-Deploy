# Todo AI Chatbot Frontend

Frontend application for the Todo AI Chatbot using Next.js 16+ with App Router and OpenAI ChatKit SDK.

## Features

- **AI-Powered Chat Interface**: Natural language task management with voice input support
- **Real-time Updates**: Task changes are reflected immediately across UI components
- **Responsive Design**: Mobile-first, tablet, and desktop optimized
- **Secure Authentication**: Better Auth integration for user sessions
- **Voice Commands**: Web Speech API for hands-free task management

## Architecture

The frontend consists of:
- **Next.js 16+** with App Router for page routing and server components
- **OpenAI ChatKit SDK** for the conversational UI
- **Better Auth** for user authentication and session management
- **TypeScript 5+** for type safety
- **Tailwind CSS** for styling with custom dark-themed design
- **Framer Motion** for smooth animations

## Components

### ChatWidget
Located at `src/components/ChatWidget.tsx`, this component provides the main AI chat interface using ChatKit SDK.

Features:
- Conversation history display
- Text input with send button
- Voice input with microphone button
- Loading states and error handling
- Real-time task updates

### VoiceInputWidget
Located at `src/components/VoiceInputWidget.tsx`, this component handles voice recognition using the Web Speech API.

Features:
- Microphone button with listening indicator
- Language support (en-US, ur-PK)
- Error handling for unsupported browsers
- Transcript forwarding to chat API

### TaskUpdateNotificationWidget
Located at `src/components/TaskUpdateNotificationWidget.tsx`, this component provides real-time notifications when tasks are modified via the AI assistant.

Features:
- Toast notifications for task operations
- Custom event handling for real-time updates
- Visual feedback for user actions

## API Integration

### Chat API Client

The chat functionality is integrated through the `chatApi` in `src/lib/api.ts`:

```typescript
import { chatApi } from '@/lib/api';

// Send a message to the AI assistant
const response = await chatApi.sendMessage(userId, message, conversationId);
```

### Voice Recognition Service

The voice input functionality is handled by the service in `src/lib/voice-recognition.ts`:

```typescript
import { startVoiceRecognition, isVoiceRecognitionSupported } from '@/lib/voice-recognition';

if (isVoiceRecognitionSupported()) {
  startVoiceRecognition(
    { lang: 'en-US' },
    (result) => {
      if (result.isFinal) {
        // Handle the recognized text
        setInputValue(result.transcript);
      }
    },
    (error) => {
      // Handle voice recognition errors
      console.error('Voice recognition error:', error);
    }
  );
}
```

## Environment Variables

Create a `.env.local` file in the frontend root with the following variables:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Frontend URL (for auth redirects)
NEXT_PUBLIC_FRONTEND_URL=http://localhost:3000

# Better Auth URL
BETTER_AUTH_URL=http://localhost:8000
```

## Running the Frontend

### Prerequisites
- Node.js 20+
- npm or yarn

### Installation
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables in `.env.local` file

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Visit `http://localhost:3000` in your browser

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── chat/            # AI Chat page
│   │   │   └── page.tsx     # Chat page component
│   │   ├── dashboard/       # Dashboard page
│   │   │   └── page.tsx     # Dashboard component
│   │   ├── tasks/           # Tasks page
│   │   │   └── page.tsx     # Tasks list component
│   │   └── layout.tsx       # Root layout with navigation
│   ├── components/          # Reusable UI components
│   │   ├── ChatWidget.tsx   # Main chat interface with ChatKit
│   │   ├── VoiceInputWidget.tsx # Voice input component
│   │   ├── TaskUpdateNotificationWidget.tsx # Real-time notifications
│   │   └── navigation/      # Navigation components
│   │       └── Navbar.tsx   # Updated navbar with AI Chat button
│   ├── lib/                 # Utilities and API clients
│   │   ├── api.ts          # API client with chat functionality
│   │   └── voice-recognition.ts # Voice recognition service
│   ├── types/               # TypeScript type definitions
│   │   └── chat.ts          # Chat-related types
│   └── styles/              # Global styles
│       └── globals.css      # Tailwind CSS customization
├── public/                  # Static assets
├── package.json            # Dependencies and scripts
├── next.config.ts          # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
└── README.md              # This file
```

## Voice Input Support

The application uses the Web Speech API for voice input. This is supported in:
- Chrome (Desktop & Android)
- Edge
- Safari (with limitations)

For browsers that don't support voice input, the application gracefully falls back to text input only.

## UI Navigation

The application includes seamless navigation between:
- Dashboard (`/dashboard`)
- Tasks (`/tasks`)
- AI Chat (`/chat`)

The AI Chat button is available in both the navbar (on all authenticated pages) and the sidebar (alongside Dashboard and Tasks).

## Real-time Updates

When tasks are modified via the AI assistant:
1. The AI assistant sends updates to the backend
2. The backend processes the MCP tools and updates the database
3. Events are dispatched to update the UI in real-time
4. The Tasks page and Dashboard metrics update without page refresh