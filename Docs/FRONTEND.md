# AutoPFT Frontend Architecture 🎨

## 🏗️ Overview

The AutoPFT frontend is built with **React 19** and **TypeScript**, designed to provide an intuitive, responsive, and performant user experience for healthcare professionals. The application follows modern React patterns with a focus on accessibility, performance, and maintainability.

## 🛠️ Technology Stack

### Core Technologies
- **React 19**: Latest React with concurrent features and improved performance
- **TypeScript**: Full type safety and enhanced developer experience
- **Vite**: Fast build tool with hot module replacement (HMR)
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **Shadcn/ui**: High-quality, accessible component library

### State Management
- **React Hooks**: `useState`, `useEffect`, `useCallback`, `useMemo`
- **Custom Hooks**: Business logic encapsulation and reusability
- **Context API**: Global state management where needed
- **Local Storage**: Persistent data storage for user preferences

### Routing & Navigation
- **React Router**: Client-side routing with nested routes
- **Protected Routes**: Role-based access control
- **Breadcrumb Navigation**: Clear user location awareness
- **Mobile Navigation**: Responsive navigation patterns

## 📁 Project Structure

```
client/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── custom/          # Application-specific components
│   │   │   ├── AlertModal.tsx
│   │   │   ├── ChatBox.tsx
│   │   │   ├── CustomAccordion.tsx
│   │   │   ├── CustomDrawerContent.tsx
│   │   │   ├── GeneralChatBox.tsx
│   │   │   ├── ReportInteractionPanel.tsx
│   │   │   ├── ReportProgressStepper.tsx
│   │   │   ├── ReportSelector.tsx
│   │   │   └── UploadSuccessModal.tsx
│   │   ├── ui/             # Base UI components (Shadcn/ui)
│   │   │   ├── alert-dialog.tsx
│   │   │   ├── avatar.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── chart.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── drawer.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   └── ... (other UI components)
│   │   ├── app-sidebar.tsx
│   │   ├── chart-area-interactive.tsx
│   │   ├── data-table.tsx
│   │   ├── mode-toggle.tsx
│   │   ├── nav-documents.tsx
│   │   ├── nav-main.tsx
│   │   ├── nav-projects.tsx
│   │   ├── nav-secondary.tsx
│   │   ├── nav-user.tsx
│   │   ├── section-cards.tsx
│   │   ├── site-header.tsx
│   │   ├── team-switcher.tsx
│   │   └── theme-provider.tsx
│   ├── pages/               # Page-level components
│   │   ├── ChatBotPage.tsx
│   │   ├── Dashboard.tsx
│   │   ├── GenerateReportPage.tsx
│   │   ├── NotFound.tsx
│   │   ├── PageContainer.tsx
│   │   ├── Prices.tsx
│   │   ├── ReportDetails.tsx
│   │   ├── Reports.tsx
│   │   └── Settings.tsx
│   ├── hooks/               # Custom React hooks
│   │   ├── use-mobile.ts
│   │   ├── useGeneralChat.ts
│   │   ├── useGetReport.ts
│   │   ├── useInterpretChat.ts
│   │   ├── usePftUpload.ts
│   │   ├── useReportProgress.ts
│   │   └── useReportSettings.ts
│   ├── services/            # API service functions
│   │   ├── generalChat.ts
│   │   ├── interpretReport.ts
│   │   ├── pdfService.ts
│   │   └── pftService.ts
│   ├── lib/                 # Utility libraries
│   │   └── utils.ts
│   ├── assets/              # Static assets
│   │   ├── images/
│   │   │   └── korle-bu.png
│   │   └── react.svg
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   ├── index.css            # Global styles
│   ├── herlpers.ts          # Helper functions
│   └── vite-env.d.ts        # Vite type definitions
├── public/                  # Public static assets
│   └── vite.svg
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite build configuration
├── eslint.config.js         # ESLint configuration
├── components.json          # Shadcn/ui configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── Dockerfile               # Production Docker configuration
├── Dockerfile.dev           # Development Docker configuration
└── nginx.conf               # Nginx configuration
```

## 🎨 Design System

### Color Palette
- **Primary**: Healthcare-focused blues and greens
- **Secondary**: Supporting colors for UI elements
- **Accent**: Highlight colors for important actions
- **Neutral**: Grays for text and borders
- **Semantic**: Success, warning, error, and info colors

### Typography
- **Font Family**: System fonts with fallbacks
- **Font Sizes**: Consistent scale (xs, sm, base, lg, xl, 2xl, 3xl)
- **Font Weights**: Regular (400), Medium (500), Semibold (600), Bold (700)
- **Line Heights**: Optimized for readability

### Spacing & Layout
- **Grid System**: 12-column responsive grid
- **Spacing Scale**: Consistent spacing using Tailwind's scale
- **Breakpoints**: Mobile-first responsive design
- **Container**: Max-width containers for content

### Component Variants
- **Button Variants**: Primary, secondary, outline, ghost, destructive
- **Input Variants**: Default, error, success, disabled
- **Card Variants**: Default, elevated, outlined
- **Alert Variants**: Info, success, warning, error

## 🔧 Key Components

### 1. Custom Components

#### AlertModal.tsx
```typescript
interface AlertModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  actions?: React.ReactNode;
}
```
- **Purpose**: Display important messages to users
- **Features**: Different alert types, customizable actions
- **Accessibility**: ARIA labels, keyboard navigation

#### ChatBox.tsx
```typescript
interface ChatBoxProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}
```
- **Purpose**: Interactive chat interface for medical queries
- **Features**: Real-time messaging, typing indicators
- **Integration**: WebSocket for live updates

#### ReportProgressStepper.tsx
```typescript
interface ReportProgressStepperProps {
  currentStep: number;
  totalSteps: number;
  steps: Step[];
  onStepClick?: (step: number) => void;
}
```
- **Purpose**: Visual progress tracking for PFT processing
- **Features**: Step-by-step progress, clickable steps
- **States**: Active, completed, pending, error

### 2. UI Components (Shadcn/ui)

#### Button Component
```typescript
import { Button } from "@/components/ui/button";

<Button variant="default" size="lg" disabled={isLoading}>
  {isLoading ? "Processing..." : "Generate Report"}
</Button>
```

#### Card Component
```typescript
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

<Card>
  <CardHeader>
    <CardTitle>PFT Report</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Report content goes here...</p>
  </CardContent>
</Card>
```

#### Dialog Component
```typescript
import { Dialog, DialogTrigger, DialogContent } from "@/components/ui/dialog";

<Dialog>
  <DialogTrigger>Open Report</DialogTrigger>
  <DialogContent>
    <h2>Report Details</h2>
    {/* Report content */}
  </DialogContent>
</Dialog>
```

## 🎣 Custom Hooks

### useGeneralChat.ts
```typescript
export const useGeneralChat = () => {
  const [messages, setMessages] = useState<GeneralChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (text: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await sendGeneralChat(text);
      setMessages(prev => [...prev, response]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { messages, sendMessage, isLoading, error };
};
```

### usePftUpload.ts
```typescript
export const usePftUpload = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const uploadFile = useCallback(async (file: File, demographics: PatientDemographics) => {
    setIsUploading(true);
    setUploadError(null);
    
    try {
      const result = await uploadPftFile(file, demographics);
      return result;
    } catch (err) {
      setUploadError(err.message);
      throw err;
    } finally {
      setIsUploading(false);
    }
  }, []);

  return { uploadFile, uploadProgress, isUploading, uploadError };
};
```

### useReportProgress.ts
```typescript
export const useReportProgress = (requestId: string) => {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');
  const [estimatedTime, setEstimatedTime] = useState<number | null>(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/pft/ws/${requestId}`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setProgress(data.progress);
      setCurrentStep(data.current_step);
      setEstimatedTime(data.estimated_completion);
    };

    return () => ws.close();
  }, [requestId]);

  return { progress, currentStep, estimatedTime };
};
```

## 🚀 Performance Optimizations

### 1. Code Splitting
```typescript
// Lazy load pages for better initial load time
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports = lazy(() => import('./pages/Reports'));
const ChatBot = lazy(() => import('./pages/ChatBotPage'));

// Suspense wrapper for loading states
<Suspense fallback={<LoadingSpinner />}>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/reports" element={<Reports />} />
    <Route path="/chat" element={<ChatBot />} />
  </Routes>
</Suspense>
```

### 2. Memoization
```typescript
// Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return complexCalculation(data);
}, [data]);

// Memoize callback functions
const handleSubmit = useCallback((formData: FormData) => {
  submitForm(formData);
}, []);
```

### 3. Virtual Scrolling
```typescript
// For large lists of reports
import { FixedSizeList as List } from 'react-window';

const ReportList = ({ reports }: { reports: Report[] }) => (
  <List
    height={600}
    itemCount={reports.length}
    itemSize={100}
    itemData={reports}
  >
    {({ index, style, data }) => (
      <div style={style}>
        <ReportItem report={data[index]} />
      </div>
    )}
  </List>
);
```

### 4. Image Optimization
```typescript
// Lazy load images
import { LazyLoadImage } from 'react-lazy-load-image-component';

<LazyLoadImage
  src={imageUrl}
  alt={altText}
  effect="blur"
  placeholder={<ImagePlaceholder />}
/>
```

## 📱 Responsive Design

### Mobile-First Approach
```css
/* Base styles for mobile */
.container {
  padding: 1rem;
  max-width: 100%;
}

/* Tablet breakpoint */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
    max-width: 768px;
  }
}

/* Desktop breakpoint */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    max-width: 1024px;
  }
}
```

### Responsive Grid
```typescript
// Responsive grid columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => (
    <Card key={item.id}>
      <CardContent>{item.content}</CardContent>
    </Card>
  ))}
</div>
```

### Touch-Friendly Interactions
```typescript
// Larger touch targets on mobile
<Button 
  className="min-h-[44px] min-w-[44px] md:min-h-[40px] md:min-w-[40px]"
  onClick={handleClick}
>
  Click me
</Button>
```

## ♿ Accessibility Features

### ARIA Labels
```typescript
// Proper labeling for screen readers
<Button
  aria-label="Generate pulmonary function test report"
  aria-describedby="report-description"
  onClick={generateReport}
>
  Generate Report
</Button>
<div id="report-description" className="sr-only">
  Click to generate a comprehensive PFT report
</div>
```

### Keyboard Navigation
```typescript
// Keyboard event handling
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleClick();
  }
};

<div
  role="button"
  tabIndex={0}
  onKeyDown={handleKeyDown}
  onClick={handleClick}
>
  Clickable element
</div>
```

### Color Contrast
```css
/* Ensure sufficient color contrast */
.text-primary {
  color: #1e40af; /* WCAG AA compliant */
}

.text-secondary {
  color: #6b7280; /* WCAG AA compliant */
}
```

## 🧪 Testing Strategy

### Component Testing
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { PFTUploadForm } from './PFTUploadForm';

describe('PFTUploadForm', () => {
  test('renders form fields', () => {
    render(<PFTUploadForm />);
    
    expect(screen.getByLabelText(/patient id/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/age/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/gender/i)).toBeInTheDocument();
  });

  test('validates required fields', () => {
    render(<PFTUploadForm />);
    
    fireEvent.click(screen.getByText(/submit/i));
    
    expect(screen.getByText(/patient id is required/i)).toBeInTheDocument();
  });
});
```

### Hook Testing
```typescript
import { renderHook, act } from '@testing-library/react';
import { useGeneralChat } from './useGeneralChat';

describe('useGeneralChat', () => {
  test('sends message successfully', async () => {
    const { result } = renderHook(() => useGeneralChat());
    
    await act(async () => {
      await result.current.sendMessage('Hello');
    });
    
    expect(result.current.messages).toHaveLength(1);
    expect(result.current.isLoading).toBe(false);
  });
});
```

### Integration Testing
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { App } from './App';

describe('App Integration', () => {
  test('navigates between pages', async () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    
    // Navigate to reports page
    fireEvent.click(screen.getByText(/reports/i));
    
    await waitFor(() => {
      expect(screen.getByText(/reports/i)).toBeInTheDocument();
    });
  });
});
```

## 🚀 Build & Deployment

### Development Build
```bash
# Install dependencies
yarn install

# Start development server
yarn dev

# Build for development
yarn build:dev
```

### Production Build
```bash
# Build optimized production bundle
yarn build

# Preview production build
yarn preview

# Analyze bundle size
yarn analyze
```

### Docker Build
```dockerfile
# Multi-stage build for production
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 📊 Performance Monitoring

### Core Web Vitals
- **Largest Contentful Paint (LCP)**: Target <2.5s
- **First Input Delay (FID)**: Target <100ms
- **Cumulative Layout Shift (CLS)**: Target <0.1

### Bundle Analysis
```bash
# Analyze bundle size
yarn build --analyze

# Check for duplicate dependencies
yarn dedupe

# Optimize imports
yarn tree-shake
```

### Real User Monitoring
```typescript
// Performance monitoring
const reportWebVitals = (metric: any) => {
  console.log(metric);
  // Send to analytics service
};

// Report Core Web Vitals
reportWebVitals(webVitals);
```

---

**The AutoPFT frontend demonstrates modern React development practices with a focus on performance, accessibility, and user experience. The component-based architecture ensures maintainability and reusability while providing a smooth, responsive interface for healthcare professionals.**