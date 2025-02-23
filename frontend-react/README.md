# Romanian Learning App - Frontend 🎨

## Quick Start 🚀

```bash
# Start everything
docker compose up

# Just frontend
docker compose up frontend
```

## Main Features 🌟

- Learn Romanian words
- Make word groups
- Import vocabulary files
- Track your progress

## Parts That Help You 🤝

- **Word Groups**: Make and manage word lists
- **Import Tool**: Add words from files
- **Progress View**: See how you're doing

## Testing 🧪

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch
```

## Need Help? 🆘

1. Check the health page: http://localhost:5173/health
2. Look at the logs: `docker compose logs frontend`
3. Ask for help in our chat

## Project Structure
```
src/
├── components/
│   ├── ui/          # Reusable UI components
│   ├── groups/      # Word group components
│   ├── words/       # Word management
│   └── study/       # Study activities
├── hooks/           # Custom React hooks
├── lib/             # Utilities
├── pages/           # Route components
└── types/           # TypeScript types
```

## Core Technologies
- React 18 with TypeScript
- Vite for building
- Tailwind CSS + shadcn/ui
- React Query for data
- React Router for navigation
- i18next for translations
- Jest + React Testing Library

## Available Scripts
- `npm run dev` - Start development
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Check code style

## Error Handling
```typescript
import { ErrorHandler } from '@/lib/errors';

try {
  // Your code
} catch (error) {
  ErrorHandler.handleError(error);
}
```

## Translations
```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  return <h1>{t('hello')}</h1>;
}
```

## Common Components

### CustomCard
```typescript
// Basic card
<CustomCard
  title="Title"
  description="Description"
  to="/link"
/>

// Word card
<CustomCard
  title="Word"
  description="Translation"
  pronunciation="Guide"
  to="/words/1"
/>
```

### Other UI Components
- Badge - For status and tags
- Button - Action buttons
- Dialog - Modal windows
- Toast - Notifications

## Contributing
1. Fork the repo
2. Create a branch
3. Make changes
4. Submit pull request

## Backend Integration
- API at `http://localhost:5000`
- Swagger docs at `/docs`
- CORS enabled
- Health checks active

