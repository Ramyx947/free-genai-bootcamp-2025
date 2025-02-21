
import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';
import { Button } from './ui/button';
import { useTranslation } from 'react-i18next';
import { ErrorHandler } from '@/lib/errors';
import { Alert, AlertDescription, AlertTitle } from './ui/alert';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      const message = ErrorHandler.getErrorMessage(this.state.error);
      
      return (
        <div className="min-h-screen flex items-center justify-center bg-background">
          <Alert variant="destructive" className="max-w-md">
            <AlertTriangle className="h-6 w-6" />
            <AlertTitle>Something went wrong</AlertTitle>
            <AlertDescription>{message}</AlertDescription>
            <Button
              onClick={() => window.location.reload()}
              variant="secondary"
              className="mt-4 w-full"
            >
              Refresh Page
            </Button>
          </Alert>
        </div>
      );
    }

    return this.props.children;
  }
}
