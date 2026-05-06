'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface NavItem {
  href: string;
  label: string;
  icon: string;
}

interface NavSection {
  title: string;
  items: NavItem[];
}

const NAV: NavSection[] = [
  {
    title: 'Overview',
    items: [{ href: '/', label: 'Dashboard', icon: '🏠' }],
  },
  {
    title: 'Farmers',
    items: [
      { href: '/farmers', label: 'All Farmers', icon: '👨‍🌾' },
    ],
  },
  {
    title: 'Operations',
    items: [
      { href: '/collection', label: 'Milk Collection', icon: '🥛' },
      { href: '/quality', label: 'Quality Tests', icon: '🔬' },
    ],
  },
  {
    title: 'Finance',
    items: [
      { href: '/finance', label: 'Payout Batches', icon: '💰' },
      { href: '/payouts', label: 'Farmer Payouts', icon: '💳' },
    ],
  },
  {
    title: 'Integrations',
    items: [
      { href: '/integrations/mpesa', label: 'MPESA', icon: '📱' },
      { href: '/integrations/sms', label: 'SMS', icon: '💬' },
    ],
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  function isActive(href: string) {
    if (href === '/') return pathname === '/';
    return pathname.startsWith(href);
  }

  return (
    <aside className="w-60 bg-white border-r border-gray-200 flex flex-col h-screen shadow-sm shrink-0">
      {/* Brand */}
      <div className="px-5 py-4 border-b border-gray-200">
        <span className="text-xl font-bold text-green-700">🐄 mDairy ERP</span>
        <p className="text-xs text-gray-400 mt-0.5">Dairy Management System</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-5">
        {NAV.map((section) => (
          <div key={section.title}>
            <p className="px-2 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">
              {section.title}
            </p>
            <ul className="space-y-0.5">
              {section.items.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive(item.href)
                        ? 'bg-green-50 text-green-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <span className="text-base">{item.icon}</span>
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="px-5 py-3 border-t border-gray-200 text-xs text-gray-400">
        mDairy ERP v1.0.0
      </div>
    </aside>
  );
}
