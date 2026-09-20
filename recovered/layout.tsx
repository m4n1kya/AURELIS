import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AURELIS | Financial Affordability Intelligence',
  description: 'Premium AI financial decision engine.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang=\"en\">
      <body className=\"antialiased min-h-screen selection:bg-[var(--accent-primary)] selection:text-black\">
        {children}
      </body>
    </html>
  );
}

