
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      dashboard: 'Dashboard',
      studyActivities: 'Study Activities',
      words: 'Words',
      wordGroups: 'Word Groups',
      sessions: 'Sessions',
      settings: 'Settings',
      launch: 'Launch',
      view: 'View',
      loading: 'Loading...',
      error: 'An error occurred',
      retry: 'Retry',
      home: 'Home',
      // Settings page translations
      appearanceAndLanguage: 'Appearance & Language',
      darkMode: 'Dark Mode',
      darkModeDescription: 'Switch between light and dark theme',
      romanianLanguage: 'Romanian Language',
      romanianLanguageDescription: 'Preferred language across the site',
      leftHandedMode: 'Left-handed Mode',
      leftHandedModeDescription: 'Enable for left-handed use',
      resetHistory: 'Reset History',
      resetHistoryDescription: 'This action will clear all your learning history and progress. This cannot be undone.',
      areYouSure: 'Are you absolutely sure?',
      resetConfirmation: 'This action cannot be undone. This will permanently delete your learning history and reset all progress.',
      typeToConfirm: 'Type "reset me" to confirm:',
      cancel: 'Cancel',
      reset: 'Reset',
      resetComplete: 'Reset Complete',
      resetSuccessful: 'Your history has been cleared successfully.',
    },
  },
  ro: {
    translation: {
      dashboard: 'Panou de Control',
      studyActivities: 'Activități de Studiu',
      words: 'Cuvinte',
      wordGroups: 'Grupuri de Cuvinte',
      sessions: 'Sesiuni',
      settings: 'Setări',
      launch: 'Lansare',
      view: 'Vizualizare',
      loading: 'Se încarcă...',
      error: 'A apărut o eroare',
      retry: 'Reîncearcă',
      home: 'Acasă',
      // Settings page translations
      appearanceAndLanguage: 'Aspect și Limbă',
      darkMode: 'Mod Întunecat',
      darkModeDescription: 'Schimba între tema luminoasă și întunecată',
      romanianLanguage: 'Limba Română',
      romanianLanguageDescription: 'Limba preferată pentru întregul site',
      leftHandedMode: 'Mod Stângaci',
      leftHandedModeDescription: 'Activați pentru utilizare stângace',
      resetHistory: 'Resetare Istoric',
      resetHistoryDescription: 'Această acțiune va șterge tot istoricul și progresul învățării. Această acțiune nu poate fi anulată.',
      areYouSure: 'Sunteți absolut sigur?',
      resetConfirmation: 'Această acțiune nu poate fi anulată. Aceasta va șterge permanent istoricul învățării și va reseta tot progresul.',
      typeToConfirm: 'Tastați "reset me" pentru confirmare:',
      cancel: 'Anulare',
      reset: 'Resetare',
      resetComplete: 'Resetare Completă',
      resetSuccessful: 'Istoricul tău a fost șters cu succes.',
    },
  },
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
