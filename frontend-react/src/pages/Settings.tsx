
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { useToast } from "@/components/ui/use-toast";
import { Settings2, Moon, Languages, PanelLeftOpen, X } from "lucide-react";
import { useTranslation } from "react-i18next";

const Settings = () => {
  const [resetConfirmation, setResetConfirmation] = useState("");
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isLeftHanded, setIsLeftHanded] = useState(document.documentElement.dataset.handedness === 'left');
  const { i18n, t } = useTranslation();
  const { toast } = useToast();

  // Initialize language state from i18n
  const [isRomanian, setIsRomanian] = useState(i18n.language === "ro");

  // Effect to sync language state with i18n
  useEffect(() => {
    setIsRomanian(i18n.language === "ro");
  }, [i18n.language]);

  const handleReset = () => {
    if (resetConfirmation === "reset me") {
      toast({
        title: t('resetComplete'),
        description: t('resetSuccessful'),
      });
      setResetConfirmation("");
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    document.documentElement.classList.toggle("dark");
  };

  const toggleHandedness = () => {
    const newIsLeftHanded = !isLeftHanded;
    setIsLeftHanded(newIsLeftHanded);
    document.documentElement.dataset.handedness = newIsLeftHanded ? 'left' : 'right';
  };

  const toggleLanguage = () => {
    const newLang = isRomanian ? "en" : "ro";
    setIsRomanian(!isRomanian);
    i18n.changeLanguage(newLang);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight" tabIndex={0}>{t('settings')}</h1>
        <Settings2 className="h-6 w-6 text-muted-foreground" aria-hidden="true" />
      </div>
      
      <div className="grid gap-6" role="main">
        <Card>
          <CardHeader>
            <CardTitle>{t('appearanceAndLanguage')}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label htmlFor="dark-mode-toggle">{t('darkMode')}</Label>
                <p className="text-sm text-muted-foreground" id="dark-mode-description">
                  {t('darkModeDescription')}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <Moon className="h-4 w-4" aria-hidden="true" />
                <Switch
                  id="dark-mode-toggle"
                  checked={isDarkMode}
                  onCheckedChange={toggleDarkMode}
                  aria-describedby="dark-mode-description"
                />
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label htmlFor="language-toggle">{t('romanianLanguage')}</Label>
                <p className="text-sm text-muted-foreground" id="language-description">
                  {t('romanianLanguageDescription')}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <Languages className="h-4 w-4" aria-hidden="true" />
                <Switch
                  id="language-toggle"
                  checked={isRomanian}
                  onCheckedChange={toggleLanguage}
                  aria-describedby="language-description"
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label htmlFor="handedness-toggle">{t('leftHandedMode')}</Label>
                <p className="text-sm text-muted-foreground" id="handedness-description">
                  {t('leftHandedModeDescription')}
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <PanelLeftOpen className="h-4 w-4" aria-hidden="true" />
                <Switch
                  id="handedness-toggle"
                  checked={isLeftHanded}
                  onCheckedChange={toggleHandedness}
                  aria-describedby="handedness-description"
                />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t('resetHistory')}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground" id="reset-description">
              {t('resetHistoryDescription')}
            </p>
            
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button 
                  variant="destructive"
                  aria-describedby="reset-description"
                >
                  {t('resetHistory')}
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <div className="flex justify-end">
                  <AlertDialogCancel className="p-2 h-auto absolute right-2 top-2 hover:bg-muted rounded-sm" aria-label="Close">
                    <X className="h-4 w-4" />
                  </AlertDialogCancel>
                </div>
                <AlertDialogHeader>
                  <AlertDialogTitle>{t('areYouSure')}</AlertDialogTitle>
                  <AlertDialogDescription>
                    {t('resetConfirmation')}
                    <div className="mt-4">
                      <Label htmlFor="confirmation">
                        {t('typeToConfirm')}
                      </Label>
                      <Input
                        id="confirmation"
                        value={resetConfirmation}
                        onChange={(e) => setResetConfirmation(e.target.value)}
                        className="mt-2"
                        aria-required="true"
                        aria-invalid={resetConfirmation !== "reset me"}
                      />
                    </div>
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>{t('cancel')}</AlertDialogCancel>
                  <AlertDialogAction
                    onClick={handleReset}
                    disabled={resetConfirmation !== "reset me"}
                    aria-disabled={resetConfirmation !== "reset me"}
                  >
                    {t('reset')}
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Settings;
