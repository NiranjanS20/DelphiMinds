'use client'

import { Header } from '@/components/Header'
import { Hero } from '@/components/Hero'
import { FeatureTiles } from '@/components/FeatureTiles'
import { SkillGraphPreview } from '@/components/SkillGraphSimple'
import { ChatDrawer } from '@/components/ChatDrawer'
import { Footer } from '@/components/FooterSimple'

export default function HomePage() {
  return (
    <main className="min-h-screen relative">
      <Header />
      <Hero />
      <FeatureTiles />
      <SkillGraphPreview />
      <Footer />
      <ChatDrawer />
    </main>
  )
}