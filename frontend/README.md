# SahajAI Frontend

The frontend for **SahajAI** – an AI-powered voice-first assistant that helps Indian citizens discover and navigate government schemes.

## Overview

The SahajAI frontend is a React + Vite application that provides a user-friendly chat interface for interacting with government scheme information. It supports:
- **Multi-language support** (English & Hindi)
- **Voice input/output** (Speech-to-Text & Text-to-Speech)
- **Real-time chat interface**
- **Backend API integration**

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| **React 19.2.0** | UI Framework |
| **Vite 7.2.4** | Build tool & Dev server |
| **JavaScript (ES modules)** | Language |
| **CSS** | Styling |
| **Web Speech API** | Voice features (TTS/STT) |

### Vite Plugins

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

### React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── App.css              # Global app styling
│   ├── main.jsx             # React DOM entry point
│   ├── index.css            # Global styles
│   ├── assets/              # Static assets (images, etc.)
│   │   └── react.svg
│   ├── services/
│   │   └── api.js           # Backend API communication
│   └── utils/
│       ├── tts.js           # Text-to-Speech utility
│       └── stt.js           # Speech-to-Text utility
├── index.html               # HTML entry point
├── package.json             # Dependencies & scripts
├── vite.config.js          # Vite configuration
├── eslint.config.js        # ESLint rules
├── README.md               # This file
└── public/                 # Public static files
```

## Installation & Setup

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Steps

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set environment variables**
   Create a `.env` file in the frontend directory (optional):
   ```env
   VITE_BACKEND_URL=http://localhost:8000
   ```
   If not set, defaults to `/api`

4. **Start development server**
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with HMR |
| `npm run build` | Create production build |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Run ESLint to check code quality |

## Core Features

### 1. Chat Interface

**File**: `src/App.jsx`

The main application component provides:
- Real-time chat messaging
- User and bot message display
- Language selection (English/Hindi)
- Loading states
- Error handling

**Key Features**:
- Maintains chat history in component state
- Sends messages to backend API
- Displays bot responses dynamically
- Graceful error handling with user feedback

### 2. API Service

**File**: `src/services/api.js`

Handles all backend communication:

```javascript
sendChatMessage(message, language = "en")
```

**Parameters**:
- `message` (string): User's chat message
- `language` (string): Language code ("en" or "hi")

**Returns**:
- Promise resolving to `{ answer: "response text" }`

**Backend Endpoint**: `POST /api/chat/`

**Configuration**:
- Backend URL from `VITE_BACKEND_URL` env var
- Falls back to `/api` if not set
- Sends JSON with content-type header

### 3. Text-to-Speech (TTS)

**File**: `src/utils/tts.js`

Converts text responses into spoken audio.

```javascript
import { speakText } from "@/utils/tts.js";

speakText("Hello, how can I help?", "en");  // English
speakText("नमस्ते, मैं आपकी क्या मदद कर सकता हूँ?", "hi");  // Hindi
```

**Features**:
- Supports English (en-IN) and Hindi (hi-IN)
- Configurable playback rate (1.0) and pitch (1.0)
- Cancels previous speech before playing new
- Graceful degradation if browser doesn't support

**Browser Support**: Chrome, Firefox, Safari, Edge

### 4. Speech-to-Text (STT)

**File**: `src/utils/stt.js`

Converts user speech into text for input.

```javascript
import { startSpeechRecognition } from "@/utils/stt.js";

startSpeechRecognition({
  language: "en",
  onResult: (transcript) => console.log("You said:", transcript),
  onError: (error) => console.error("Error:", error),
  onEnd: () => console.log("Recording ended")
});
```

**Parameters**:
- `language` (string): "en" or "hi"
- `onResult` (function): Called with recognized text
- `onError` (function): Called with error object
- `onEnd` (function): Called when recording stops

**Features**:
- Single phrase recognition per session
- Language-specific processing
- Callback-based event handling
- Automatic error handling

**Browser Support**: Chrome, Firefox, Safari (limited), Edge

## State Management

The app uses React hooks for state:

```javascript
const [message, setMessage] = useState("");        // Current input
const [chat, setChat] = useState([]);              // Chat history
const [loading, setLoading] = useState(false);     // Loading state
const [language, setLanguage] = useState("en");    // Selected language
```

## API Integration

### Chat Endpoint

**Method**: POST  
**Endpoint**: `/api/chat/`  
**Request Body**:
```json
{
  "message": "What are government schemes for farmers?",
  "language": "en"
}
```

**Response**:
```json
{
  "answer": "Here are the government schemes for farmers..."
}
```

## Styling

The application uses:
- **Global styles**: `src/index.css` (base styles)
- **App styles**: `src/App.css` (layout and components)
- **Inline styles**: Directly in JSX components

Currently styled with basic CSS. Can be enhanced with:
- CSS Modules
- Tailwind CSS
- Styled Components
- Material-UI / Chakra UI

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_BACKEND_URL` | `/api` | Backend API base URL |

Example `.env`:
```env
VITE_BACKEND_URL=http://localhost:8000
```

## Development Workflow

### 1. Hot Module Replacement (HMR)
Vite provides HMR - changes are reflected instantly without full page reload.

### 2. ESLint
Run linter to check code quality:
```bash
npm run lint
```

### 3. Production Build
Create optimized build:
```bash
npm run build
```

Outputs to `dist/` directory.

### 4. Expanding ESLint Configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## Debugging

### Browser DevTools
1. Open browser DevTools (F12)
2. Check Console tab for logs and errors
3. Network tab shows API calls to backend
4. React DevTools extension helps with component debugging

### Common Issues

**Backend Connection Error**
- Check `VITE_BACKEND_URL` configuration
- Verify backend is running
- Check CORS settings if running on different origin

**Speech Features Not Working**
- Verify browser supports Web Speech API
- Check microphone permissions (for STT)
- Ensure HTTPS (some browsers require it for audio)

**Language Not Changing**
- Verify `language` state is being updated
- Check backend supports the language parameter
- Test with "en" first, then "hi"

## Features Roadmap

- [ ] Voice input button with visual feedback
- [ ] Voice output toggle for responses
- [ ] Message history persistence
- [ ] User authentication
- [ ] Advanced chat features (document upload, image support)
- [ ] Theme support (dark mode)
- [ ] Accessibility improvements (ARIA labels)
- [ ] Offline support (Service Workers)
- [ ] Multi-turn context awareness
- [ ] Rate limiting and usage analytics

## Performance Optimization

### Already Implemented
- Vite's code splitting
- Fast Refresh for dev
- Production minification

### Future Improvements
- Lazy loading components
- Code splitting for heavy utilities
- Image optimization
- Caching strategies
- Bundle size monitoring

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| React | ✅ | ✅ | ✅ | ✅ |
| Vite | ✅ | ✅ | ✅ | ✅ |
| TTS | ✅ | ✅ | ✅ | ✅ |
| STT | ✅ | ✅ | ⚠️ | ✅ |

## Security Considerations

1. **Backend URL**: Use environment variables for URLs
2. **CORS**: Ensure backend allows requests from frontend origin
3. **Input Validation**: Sanitize user inputs before sending to backend
4. **XSS Prevention**: React automatically escapes content
5. **HTTPS**: Use HTTPS in production

## Deployment

### Vite Build
```bash
npm run build
```

Creates optimized `dist/` folder.

### Deployment Options
1. **Vercel**: `vercel deploy`
2. **Netlify**: Connect GitHub repo
3. **AWS S3 + CloudFront**: Upload `dist/` contents
4. **Docker**: Create Dockerfile for containerization
5. **Traditional Server**: Serve `dist/` via nginx/Apache

### Production Environment Setup
1. Set `VITE_BACKEND_URL` to production backend URL
2. Enable HTTPS
3. Configure CORS properly
4. Use Content Security Policy headers
5. Set up error tracking/monitoring

## Contributing

### Code Style
- Follow ESLint rules
- Use functional components with hooks
- Keep components small and focused
- Write meaningful variable names

### Adding Features
1. Create feature branch
2. Make changes in `src/`
3. Test thoroughly
4. Run `npm run lint`
5. Commit and push
6. Create Pull Request

## Troubleshooting

### "Backend error. Please try again"
- Check if backend is running
- Verify `VITE_BACKEND_URL` in browser console
- Check browser Network tab for failed requests
- Review backend logs for error details

### Vite Dev Server Issues
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear vite cache
rm -rf .vite
npm run dev
```

### Speech Recognition Not Working
- Check browser supports Web Speech API
- Grant microphone permission
- Test in Chrome first (best support)
- Ensure no other app is using microphone

## Support & Resources

- [React Documentation](https://react.dev)
- [Vite Guide](https://vitejs.dev)
- [Web Speech API MDN](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Team NewGenesis GitHub](https://github.com/Anshulx007/TeamNewGenesis)

## License

Part of SahajAI project - Team NewGenesis

---

**Last Updated**: January 31, 2026
