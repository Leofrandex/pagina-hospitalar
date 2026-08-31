import Header from "@/components/Header";
import Hero from "@/components/Hero";
import TrustMarquee from "@/components/TrustMarquee";
import ValueProps from "@/components/ValueProps";
import Specialties from "@/components/Specialties";
import CaseStudies from "@/components/CaseStudies";
import BlogTeaser from "@/components/BlogTeaser";
import ContactCTA from "@/components/ContactCTA";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <Header />
      <Hero />
      <TrustMarquee />
      <ValueProps />
      <Specialties />
      <CaseStudies />
      <BlogTeaser />
      <ContactCTA />
      <Footer />
    </main>
  );
}
