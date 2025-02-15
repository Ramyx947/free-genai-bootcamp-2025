# Lumina - Romanian Language Learning App

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
   - [Core Functionality](#core-functionality)
   - [Learning Tools](#learning-tools)
3. [Technical Stack](#technical-stack)
   - [Core Technologies](#core-technologies)
   - [Key Components](#key-components)
4. [Project Structure](#project-structure)
5. [Getting Started](#getting-started)
6. [Available Scripts](#available-scripts)
7. [Component Library](#component-library)
8. [Contributing](#contributing)
9. [License](#license)
10. [Running Tests](#running-tests)
11. [Error Handling System](#error-handling-system)
12. [Translations](#translations)
13. [Settings](#settings)
14. [Reusable Components](#reusable-components)

[↑ Back to Top](#table-of-contents)
## Overview

Lumina is a comprehensive language learning platform designed to help users master Romanian through interactive exercises, vocabulary management, and progress tracking.

## Features

### Core Functionality
- **Dashboard**: Progress overview and quick access to learning activities
- **Word Management**: Create and organize vocabulary with custom groups
- **Study Activities**: Interactive exercises for vocabulary, reading, and grammar
- **Progress Tracking**: Detailed session history and performance metrics
- **Customizable Settings**: Language preferences, themes, and accessibility options

### Learning Tools
- Vocabulary practice with pronunciation
- Custom word groups for organized learning
- Interactive study sessions
- Progress tracking and statistics
- Multi-language interface (EN/RO)

## Technical Stack

### Core Technologies
- **Framework**: React 18 with Vite
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: React Query
- **Routing**: React Router
- **Internationalization**: i18next
- **Testing**: Jest + React Testing Library

### Key Components

#### CustomCard
```tsx
import { CustomCard } from "@/components/ui/custom-card";

// Basic usage
<CustomCard
  title="Card Title"
  description="Card description"
  to="/optional-link"
>
  {/* Optional children content */}
</CustomCard>

// Word card with pronunciation
<CustomCard
  title="Word"
  description="Translation"
  pronunciation="Pronunciation guide"
  to="/words/1"
/>
```

#### Error Handling
```typescript
import { ErrorHandler } from '@/lib/errors';

try {
  // Your code
} catch (error) {
  ErrorHandler.handleError(error);
}
```

#### Translations
```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  return <h1>{t('hello')}</h1>;
}
```

## Project Structure

```
src/
├── components/
│   ├── ui/          # Reusable UI components
│   ├── groups/      # Word group related components
│   ├── words/       # Word management components
│   └── study/       # Study activity components
├── hooks/           # Custom React hooks
├── lib/             # Utilities and configurations
├── pages/           # Route components
├── types/           # TypeScript definitions
└── test/            # Test utilities
```

## Getting Started

1. **Installation**
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

2. **Environment Setup**
```bash
# Copy example env file
cp .env.example .env

# Configure environment variables
VITE_API_URL=your_api_url
```

3. **Running Tests**
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- src/components/__tests__/YourComponent.test.tsx
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm test` - Run tests

## Component Library

### UI Components
- **Badge**: Status indicators and tags
- **Button**: Action buttons with variants
- **CustomCard**: Versatile card layouts
- **CustomBreadcrumb**: Navigation breadcrumbs
- **Dialog**: Modal dialogs and forms
- **Toast**: Notification system

### Features
- Consistent styling across light/dark themes
- Interactive hover and focus states
- Accessibility-first design
- Responsive layouts
- Gamification elements

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Running Tests

To run the tests:

```bash
# Run all tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- src/pages/__tests__/StudyActivities.test.tsx
```

The project uses Jest and React Testing Library for testing. Test files are located next to their components with the naming pattern `*.test.tsx`.


**Run locally**

If you want to work locally using your own IDE, you can clone this repo and push changes.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

The application will be available at `http://localhost:8080`.

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS
- i18next for translations
- ErrorHandler for centralized error management

### Error Handling System

The project includes a centralized error handling system located in `src/lib/errors.ts`. This system provides:

- Typed error codes
- Multilingual error messages (EN/RO)
- Consistent error handling across the application
- Toast notifications for errors

Example usage:

```typescript
import { ErrorHandler } from '@/lib/errors';

// Handle a caught error
try {
  // Your code
} catch (error) {
  ErrorHandler.handleError(error);
}

// Create and handle a specific error
const error = ErrorHandler.createError('VALIDATION_ERROR', {
  field: 'email',
  value: 'invalid-email'
});
ErrorHandler.handleError(error);
```

### Translations (i18next)

The application uses i18next for internationalization support. Translation files are located in `src/lib/i18n.ts`.

Example usage in components:

```typescript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();
  
  return <h1>{t('hello')}</h1>;
}
```

To add new translations:
1. Add your translation key and text in `src/lib/i18n.ts`
2. Use the key in your components with the `t()` function

### Settings

The application includes several configurable settings:

- **Dark Mode**: Toggle between light and dark themes
- **Language**: Switch between English and Romanian
- **Left-handed Mode**: Adjust UI for left-handed users
- **History Reset**: Option to reset user learning history


## Reusable Components

The project includes several reusable components designed for consistency and maintainability:

### CustomCard Component
Located in `src/components/ui/custom-card.tsx`

A versatile card component with consistent styling for both light and dark themes.

```tsx
import { CustomCard } from "@/components/ui/custom-card";

// Basic usage
<CustomCard
  title="Card Title"
  description="Card description"
  to="/optional-link"
>
  {/* Optional children content */}
</CustomCard>

// With pronunciation (for word cards)
<CustomCard
  title="Word"
  description="Translation"
  pronunciation="Pronunciation guide"
  to="/words/1"
/>

// With footer
<CustomCard
  title="Card Title"
  footer={<div>Footer content</div>}
/>
```

Features:
- Consistent styling across light/dark themes
- Interactive hover effects
- Full card clickable area when `to` prop is provided
- Supports custom content via children
- Gamification effects in dark mode

### Other Components
- **Badge**: `src/components/ui/badge.tsx` - For tags and status indicators
- **Button**: `src/components/ui/button.tsx` - Consistent button styling
- **CustomBreadcrumb**: `src/components/ui/custom-breadcrumb.tsx` - Navigation breadcrumbs