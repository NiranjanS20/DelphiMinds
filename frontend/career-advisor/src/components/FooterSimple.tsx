'use client'

export function Footer() {
  const footerSections = [
    {
      title: 'Platform',
      links: [
        { name: 'Onboard', href: '/onboard' },
        { name: 'Skill Map', href: '/skills' },
        { name: 'Career Paths', href: '/paths' },
        { name: 'Learning Plan', href: '/plan' },
      ],
    },
    {
      title: 'Tools',
      links: [
        { name: 'Interview Lab', href: '/interview' },
        { name: 'Market Pulse', href: '/market' },
        { name: 'Mentors', href: '/mentors' },
        { name: 'Admin Panel', href: '/admin' },
      ],
    },
    {
      title: 'Resources',
      links: [
        { name: 'Documentation', href: '#docs' },
        { name: 'API Guide', href: '#api' },
        { name: 'Tutorials', href: '#tutorials' },
        { name: 'Blog', href: '#blog' },
      ],
    },
    {
      title: 'Company',
      links: [
        { name: 'About Us', href: '#about' },
        { name: 'Privacy Policy', href: '#privacy' },
        { name: 'Terms of Service', href: '#terms' },
        { name: 'Contact', href: '#contact' },
      ],
    },
  ]

  const socialLinks = [
    { name: 'Twitter', href: '#twitter', icon: '🐦' },
    { name: 'LinkedIn', href: '#linkedin', icon: '💼' },
    { name: 'GitHub', href: '#github', icon: '💻' },
    { name: 'Discord', href: '#discord', icon: '💬' },
  ]

  return (
    <footer className="relative bg-gradient-to-t from-slate-900 to-transparent border-t border-white/10">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 via-transparent to-cyan-500/10"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8 mb-12">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <div>
              <a href="/" className="inline-block mb-4">
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  DelphiMinds
                </span>
              </a>
              <p className="text-gray-400 mb-6 max-w-sm leading-relaxed">
                Empowering careers through AI-driven insights, personalized learning paths, 
                and intelligent skill development.
              </p>
              
              {/* Social Links */}
              <div className="flex space-x-4">
                {socialLinks.map((social) => (
                  <a
                    key={social.name}
                    href={social.href}
                    className="p-2 bg-white/5 border border-white/20 rounded-lg text-gray-400 hover:text-white hover:border-white/30 hover:bg-white/10 transition-all duration-200 hover:scale-110 hover:-translate-y-1"
                    title={social.name}
                  >
                    <span className="text-xl">{social.icon}</span>
                  </a>
                ))}
              </div>
            </div>
          </div>

          {/* Footer Links */}
          {footerSections.map((section) => (
            <div key={section.title} className="lg:col-span-1">
              <div>
                <h3 className="text-white font-semibold text-sm uppercase tracking-wider mb-4">
                  {section.title}
                </h3>
                <ul className="space-y-3">
                  {section.links.map((link) => (
                    <li key={link.name}>
                      <a
                        href={link.href}
                        className="text-gray-400 hover:text-white text-sm transition-colors duration-200"
                      >
                        {link.name}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        {/* Newsletter Signup */}
        <div className="bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/20 p-8 mb-12">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-2xl font-bold text-white mb-4">
              Stay ahead of the curve
            </h3>
            <p className="text-gray-400 mb-6">
              Get the latest career insights, skill trends, and AI-powered recommendations delivered to your inbox.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-white/30 transition-all duration-200"
              />
              <button className="px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold rounded-xl shadow-lg hover:shadow-cyan-500/30 hover:scale-105 transition-all duration-200">
                Subscribe
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-white/10">
          <div className="flex items-center space-x-4 mb-4 md:mb-0">
            <p className="text-gray-400 text-sm">
              © 2024 DelphiMinds. All rights reserved.
            </p>
            <div className="flex items-center space-x-1 text-xs text-gray-500">
              <span>Made with</span>
              <span className="text-red-400 animate-pulse">❤️</span>
              <span>by AI</span>
            </div>
          </div>

          <div className="flex items-center space-x-6 text-sm text-gray-400">
            <a href="#privacy" className="hover:text-white transition-colors duration-200">Privacy</a>
            <a href="#terms" className="hover:text-white transition-colors duration-200">Terms</a>
            <a href="#cookies" className="hover:text-white transition-colors duration-200">Cookies</a>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-green-400">All systems operational</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}