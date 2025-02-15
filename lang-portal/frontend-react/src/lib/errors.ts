
import { toast } from "@/components/ui/use-toast";
import i18n from './i18n';

export type ErrorCode = 
  | 'GENERIC_ERROR'
  | 'NETWORK_ERROR'
  | 'NOT_FOUND'
  | 'UNAUTHORIZED'
  | 'VALIDATION_ERROR'
  | 'SERVER_ERROR';

export interface AppError {
  code: ErrorCode;
  message: string;
  details?: Record<string, any>;
}

export const errorMessages: Record<ErrorCode, { en: string; ro: string }> = {
  GENERIC_ERROR: {
    en: 'An unexpected error occurred',
    ro: 'A apărut o eroare neașteptată'
  },
  NETWORK_ERROR: {
    en: 'Unable to connect to the server',
    ro: 'Nu s-a putut conecta la server'
  },
  NOT_FOUND: {
    en: 'The requested resource was not found',
    ro: 'Resursa solicitată nu a fost găsită'
  },
  UNAUTHORIZED: {
    en: 'You are not authorized to perform this action',
    ro: 'Nu sunteți autorizat să efectuați această acțiune'
  },
  VALIDATION_ERROR: {
    en: 'Please check your input and try again',
    ro: 'Vă rugăm să verificați datele introduse și să încercați din nou'
  },
  SERVER_ERROR: {
    en: 'Server error occurred. Please try again later',
    ro: 'A apărut o eroare de server. Vă rugăm să încercați mai târziu'
  }
};

export class ErrorHandler {
  static getErrorMessage(error: AppError | Error | unknown): string {
    if (error instanceof Error) {
      return error.message;
    }
    
    if (this.isAppError(error)) {
      const currentLanguage = i18n.language as 'en' | 'ro';
      return errorMessages[error.code][currentLanguage] || errorMessages.GENERIC_ERROR[currentLanguage];
    }

    return errorMessages.GENERIC_ERROR[i18n.language as 'en' | 'ro'];
  }

  static isAppError(error: unknown): error is AppError {
    return (
      typeof error === 'object' &&
      error !== null &&
      'code' in error &&
      typeof (error as AppError).code === 'string'
    );
  }

  static handleError(error: AppError | Error | unknown) {
    const message = this.getErrorMessage(error);
    
    toast({
      variant: "destructive",
      title: i18n.language === 'en' ? 'Error' : 'Eroare',
      description: message,
    });

    console.error('[Error Handler]:', error);
  }

  static createError(code: ErrorCode, details?: Record<string, any>): AppError {
    return {
      code,
      message: this.getErrorMessage({ code, message: '', details }),
      details
    };
  }
}
