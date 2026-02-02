# Widget Components Contract: AI Chat Interface

**Feature**: Chat API, Voice Input & UI Navigation
**Component Type**: Widget Components for Chat Interface
**Framework**: React/Next.js with TypeScript

## 1. Core Widget Components

### 1.1 ChatWidget
**Purpose**: Main chat interface component that encapsulates the entire chat experience
**Props Interface**:
```typescript
interface ChatWidgetProps {
  userId: string;
  initialConversationId?: number;
  onConversationUpdate?: (conversationId: number) => void;
  onTaskUpdate?: () => void;
}
```

**Functionality**:
- Manages conversation state
- Handles message submission
- Integrates with voice input
- Displays conversation history
- Shows tool execution confirmations

### 1.2 VoiceInputWidget
**Purpose**: Voice input component that captures speech and converts to text
**Props Interface**:
```typescript
interface VoiceInputWidgetProps {
  onTranscript: (text: string) => void;
  onError?: (error: string) => void;
  supportedLanguages?: string[];
  defaultLanguage?: string;
}
```

**Functionality**:
- Captures microphone input
- Performs speech-to-text conversion
- Supports multiple languages (en-US, ur-PK)
- Provides visual feedback during recording
- Falls back to text input for unsupported browsers

### 1.3 TaskUpdateNotificationWidget
**Purpose**: Displays notifications when tasks are updated via AI assistant
**Props Interface**:
```typescript
interface TaskUpdateNotificationWidgetProps {
  taskId: number;
  action: 'created' | 'updated' | 'deleted' | 'completed';
  taskTitle: string;
}
```

**Functionality**:
- Shows real-time updates when AI modifies tasks
- Provides visual feedback for user actions
- Integrates with task list component

## 2. UI Navigation Widgets

### 2.1 NavigationBadgeWidget
**Purpose**: Badge indicator for AI Chat feature in navigation
**Props Interface**:
```typescript
interface NavigationBadgeWidgetProps {
  unreadCount?: number;
  isActive?: boolean;
}
```

**Functionality**:
- Shows notification count for unread messages
- Indicates active state when on AI Chat page
- Integrates with navbar and sidebar

### 2.2 QuickChatWidget
**Purpose**: Floating widget for quick access to AI chat from any page
**Props Interface**:
```typescript
interface QuickChatWidgetProps {
  userId: string;
  minimized?: boolean;
  onToggleMinimize?: () => void;
}
```

**Functionality**:
- Provides quick access to AI chat
- Can be minimized/maximized
- Maintains conversation context

## 3. Widget Composition

### 3.1 ChatPageWidget
**Purpose**: Complete page component combining all chat widgets
```typescript
interface ChatPageWidgetProps {
  userId: string;
  conversationId?: number;
}

const ChatPageWidget: React.FC<ChatPageWidgetProps> = ({ userId, conversationId }) => {
  return (
    <div className="chat-container">
      <ChatWidget userId={userId} initialConversationId={conversationId} />
      <TaskUpdateNotificationWidgetContainer userId={userId} />
    </div>
  );
};
```

### 3.2 EnhancedNavbarWidget
**Purpose**: Navbar with integrated AI Chat access
```typescript
interface EnhancedNavbarWidgetProps {
  currentRoute: string;
  unreadChatCount?: number;
}

const EnhancedNavbarWidget: React.FC<EnhancedNavbarWidgetProps> = ({
  currentRoute,
  unreadChatCount
}) => {
  return (
    <nav className="navbar">
      {/* Existing nav items */}
      <NavItem
        href="/chat"
        label="AI Chat"
        isActive={currentRoute === '/chat'}
      >
        <NavigationBadgeWidget unreadCount={unreadChatCount} />
      </NavItem>
    </nav>
  );
};
```

## 4. Widget Communication Protocol

### 4.1 Event Types
```typescript
enum WidgetEventType {
  MESSAGE_SENT = 'message_sent',
  CONVERSATION_UPDATED = 'conversation_updated',
  TASK_CREATED = 'task_created',
  TASK_UPDATED = 'task_updated',
  TASK_DELETED = 'task_deleted',
  VOICE_INPUT_STARTED = 'voice_input_started',
  VOICE_INPUT_ENDED = 'voice_input_ended',
  ERROR_OCCURRED = 'error_occurred'
}
```

### 4.2 Event Payload Structure
```typescript
interface WidgetEventPayload {
  type: WidgetEventType;
  data: any;
  timestamp: Date;
  source: string; // Which widget originated the event
}
```

## 5. Styling & Theming

### 5.1 CSS Classes
All widgets should use the following CSS classes for consistency:
- `.widget-container`: Base container class
- `.widget-header`: Header section of widget
- `.widget-body`: Main content area
- `.widget-footer`: Footer section
- `.voice-input-active`: Applied when voice input is active
- `.task-update-highlight`: Highlight effect for task updates

### 5.2 Responsive Design
Widgets must be responsive and adapt to:
- Mobile (320px - 768px)
- Tablet (768px - 1024px)
- Desktop (1024px+)

## 6. Accessibility Standards

### 6.1 ARIA Attributes
- `role="region"` for main chat areas
- `aria-live="polite"` for updates
- `aria-label` for all interactive elements
- `aria-describedby` for instructions

### 6.2 Keyboard Navigation
- Tab navigation must work for all interactive elements
- Space/Enter to activate buttons
- Escape to close modals/dropdowns

## 7. Integration Points

### 7.1 Backend API Integration
Widgets communicate with backend through:
- `/api/{user_id}/chat` for chat messages
- Standard authentication headers
- Real-time updates via state management

### 7.2 State Management
Widgets use React state/context for:
- Current conversation
- Pending voice transcriptions
- Task update notifications
- UI state (minimized/maximized, etc.)

## 8. Error Handling

### 8.1 Error States
Widgets must handle:
- Network errors
- API rate limits
- Voice recognition failures
- Authentication failures
- Browser compatibility issues

### 8.2 Error Display
- Visual indicators for errors
- User-friendly error messages
- Graceful fallback options