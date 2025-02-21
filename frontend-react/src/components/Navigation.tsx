
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import { Menu } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { useIsMobile } from '@/hooks/use-mobile';
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { useState, useEffect } from 'react';
import { Progress } from "@/components/ui/progress";

export const Navigation = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const isMobile = useIsMobile();
  const isRightHanded = document.documentElement.dataset.handedness !== 'left';
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    setLoading(true);
    setProgress(0);
    const timer = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(timer);
          setLoading(false);
          return 100;
        }
        return prev + 2;
      });
    }, 20);

    return () => {
      clearInterval(timer);
    };
  }, [location.pathname]);

  const navItems = [
    { href: '/dashboard', label: t('dashboard') },
    { href: '/study-activities', label: t('studyActivities') },
    { href: '/words', label: t('words') },
    { href: '/groups', label: t('wordGroups') },
    { href: '/sessions', label: t('sessions') },
    { href: '/settings', label: t('settings') },
  ];

  const NavLinks = ({ mobile = false }) => (
    <>
      {navItems.map((item) => {
        const isActive = location.pathname === item.href;
        const LinkComponent = (
          <Link
            to={item.href}
            className={`
              relative text-foreground transition-all duration-300 ease-in-out
              focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
              hover:text-sky-500
              ${mobile 
                ? `py-4 px-6 w-full flex items-center 
                   ${isRightHanded 
                     ? 'text-right justify-end hover:-translate-x-2' 
                     : 'text-left justify-start hover:translate-x-2'}`
                : 'pb-4 px-2 hover:scale-110'} 
              font-bold
              ${isActive ? 'dark:text-white text-black text-2xl' : 'text-base'}
            `}
            role="menuitem"
            tabIndex={0}
            aria-current={isActive ? 'page' : undefined}
            aria-label={`${item.label}${isActive ? ' (current page)' : ''}`}
          >
            {item.label}
            {isActive && (
              <div 
                className={`absolute h-1.5 rounded-t-md bg-gradient-to-r from-[#ea384c] via-[#F97316] to-[#0EA5E9]
                  ${mobile 
                    ? `bottom-0 ${isRightHanded ? 'right-6' : 'left-6'} w-[calc(100%-48px)]` 
                    : 'bottom-0 left-0 w-full'}`}
                aria-hidden="true"
              />
            )}
          </Link>
        );

        return mobile ? (
          <SheetClose key={item.href} asChild>
            {LinkComponent}
          </SheetClose>
        ) : (
          <div key={item.href}>{LinkComponent}</div>
        );
      })}
    </>
  );

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 shadow-lg">
      <nav className="container mx-auto px-4" aria-label="Main navigation">
        <div className="flex h-16 items-center justify-between">
          <Link 
            to="/" 
            className="text-xl font-bold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            aria-label="Go to homepage"
            tabIndex={0}
          >
            <span className="text-[26px]">Lumina</span>
            <span className="text-base"> - Learn Romanian</span>
          </Link>

          {isMobile ? (
            <Sheet open={isOpen} onOpenChange={setIsOpen}>
              <SheetTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="md:hidden"
                  aria-label="Open navigation menu"
                  tabIndex={0}
                >
                  <Menu className="h-6 w-6" />
                  <span className="sr-only">Toggle menu</span>
                </Button>
              </SheetTrigger>
              <SheetContent 
                side={isRightHanded ? "right" : "left"} 
                className="w-full sm:w-[300px] p-0"
                role="dialog"
                aria-label="Navigation menu"
              >
                <SheetHeader className="p-6 border-b">
                  <SheetTitle>Menu</SheetTitle>
                </SheetHeader>
                <nav 
                  className="flex flex-col space-y-1 mt-4"
                  role="menu"
                  aria-label="Mobile navigation"
                >
                  <NavLinks mobile={true} />
                </nav>
              </SheetContent>
            </Sheet>
          ) : (
            <div 
              className="hidden md:flex space-x-8" 
              role="menubar"
              aria-label="Main menu"
            >
              <NavLinks />
            </div>
          )}
        </div>
      </nav>
      {loading && (
        <div className="h-1 w-full bg-gray-100">
          <div
            className="h-full transition-all duration-200 ease-out bg-gradient-to-r from-[#ea384c] via-[#F97316] to-[#0EA5E9]"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </header>
  );
};
