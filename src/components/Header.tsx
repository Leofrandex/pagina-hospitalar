import Image from "next/image";
import Link from "next/link";
import { ChevronDown, Menu } from "lucide-react";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full bg-white/85 backdrop-blur-lg border-b border-gray-100 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex-shrink-0 flex items-center">
            <Link href="/">
              <Image 
                src="/Logo-Nuevo.png" 
                alt="Hospitalar Venezuela Logo" 
                width={180} 
                height={50} 
                className="object-contain h-auto w-auto max-h-12"
                priority
              />
            </Link>
          </div>

          {/* Desktop Right Side (Nav + CTA) */}
          <div className="hidden md:flex items-center gap-8 lg:gap-12">
            {/* Desktop Navigation */}
            <nav className="flex space-x-8 items-center text-[15px]">
              <a href="#soporte" className="text-primary font-medium hover:text-accent transition-colors duration-200 cursor-pointer">
                Acerca de
              </a>
              <a href="#equipos" className="text-primary font-medium hover:text-accent transition-colors duration-200 cursor-pointer">
                Equipos
              </a>
              <a href="#casos" className="text-primary font-medium hover:text-accent transition-colors duration-200 cursor-pointer">
                Casos de éxito
              </a>
            </nav>

            {/* CTA Button */}
            <div className="flex items-center">
              <a href="#contacto" className="bg-cta text-white font-syncopate font-bold text-xs md:text-sm tracking-wider px-6 py-3 rounded-lg hover:bg-[#d95b2d] hover:shadow-lg hover:shadow-cta/30 hover:-translate-y-0.5 transition-all duration-300 cursor-pointer block">
                Solicitar Asesoría
              </a>
            </div>
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button className="text-primary hover:text-accent transition-colors cursor-pointer p-2">
              <Menu className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
