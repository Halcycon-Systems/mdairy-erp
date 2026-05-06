/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // Allow connections to the Odoo backend
  async rewrites() {
    const odooUrl = process.env.NEXT_PUBLIC_ODOO_URL ?? 'http://localhost:8069';
    return [
      {
        source: '/odoo/:path*',
        destination: `${odooUrl}/:path*`,
      },
    ];
  },
};

export default nextConfig;
