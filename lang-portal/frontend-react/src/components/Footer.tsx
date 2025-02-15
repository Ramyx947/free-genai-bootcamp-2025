
import { Link } from 'react-router-dom';

export const Footer = () => {
  const footerLinks = [
    { href: '/terms', label: 'Terms & Conditions' },
    { href: '/privacy', label: 'Privacy Policy' },
    { href: '/support', label: 'Help & Support' },
    { href: '/feedback', label: 'Feedback' },
    { href: '/about', label: 'About' },
  ];

  return (
    <footer className="bg-background border-t border-border py-8 mt-auto" role="contentinfo">
      <div className="container mx-auto px-4">
        <nav 
          aria-label="Footer navigation" 
          className="flex flex-wrap justify-center gap-6"
        >
          {footerLinks.map((link) => (
            <Link
              key={link.href}
              to={link.href}
              className="text-muted-foreground hover:text-foreground transition-colors duration-200 
                focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
                rounded-md px-2 py-1"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <p className="text-center text-sm text-muted-foreground mt-6">
          © {new Date().getFullYear()} Lumina. All rights reserved.
        </p>
      </div>
    </footer>
  );
};
