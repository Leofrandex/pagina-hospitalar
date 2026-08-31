import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, Globe, MapPin, Phone, Mail, MessageCircle } from "lucide-react";
import { sedes } from "@/data/sedes";

export default function Footer() {
  return (
    <footer className="bg-[#1a174c] text-gray-300 py-16 border-t border-white/5 relative z-10 w-full overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
          {/* Logo & Bio */}
          <div className="flex flex-col items-start h-full justify-start">
            <div className="bg-white/90 px-4 py-2 rounded-lg mb-6">
              <Image 
                src="/Logo-Nuevo.png" 
                alt="Hospitalar Venezuela Logo" 
                width={140} 
                height={40} 
                className="object-contain"
              />
            </div>
            <p className="font-light text-sm leading-relaxed text-gray-400 mb-6">
              Vanguardia tecnológica en equipamiento médico. Desarrollando proyectos y soluciones integrales de salud a nivel nacional.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-accent text-white hover:-translate-y-1 transition-all duration-300">
                <Globe className="w-4 h-4" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-[#0077b5] text-white hover:-translate-y-1 transition-all duration-300">
                <MapPin className="w-4 h-4" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-[#1877F2] text-white hover:-translate-y-1 transition-all duration-300">
                <Phone className="w-4 h-4" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center hover:bg-[#FF0000] text-white hover:-translate-y-1 transition-all duration-300">
                <Mail className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Links: Dirección */}
          <div className="flex flex-col h-full justify-start">
            <h4 className="font-syncopate font-bold text-white text-sm mb-6 uppercase tracking-wider flex items-center gap-2">
              <MapPin className="w-4 h-4 text-accent" /> Sedes
            </h4>
            <ul className="space-y-6 text-sm font-light text-gray-400">
              {sedes.map((sede) => (
                <li key={sede.ciudad}>
                  <strong className="text-white block mb-1">{sede.ciudad}:</strong>
                  <span className="block mb-3">{sede.direccion}</span>
                  <a
                    href={sede.maps}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-4 py-2 font-syncopate text-[9px] font-bold uppercase tracking-widest text-white transition-all duration-300 hover:border-accent/40 hover:bg-accent hover:-translate-y-0.5"
                  >
                    <MapPin className="w-3.5 h-3.5" />
                    Cómo llegar
                    <ArrowUpRight className="w-3 h-3" />
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Links: Teléfonos */}
          <div className="flex flex-col h-full justify-start">
            <h4 className="font-syncopate font-bold text-white text-sm mb-6 uppercase tracking-wider flex items-center gap-2">
              <Phone className="w-4 h-4 text-accent" /> Contactos
            </h4>
            <ul className="space-y-4 text-sm font-light text-gray-400">
              <li><strong className="text-white">Celular:</strong> +58 424 1941573</li>
              <li><strong className="text-white">Oficinas Caracas:</strong><br /> +58 212-2804934</li>
              <li><strong className="text-white">Oficinas Barquisimeto:</strong><br /> +58 251-2524093</li>
              <li><strong className="text-white">Oficinas Maturín:</strong><br /> +58 424-1941573</li>
              <li className="pt-2">
                <strong className="text-white block mb-1 flex items-center gap-2"><Mail className="w-4 h-4" /> Email:</strong>
                <a href="mailto:contigo@hospitalarve.com" className="hover:text-accent transition-colors">contigo@hospitalarve.com</a>
              </li>
            </ul>
          </div>

          {/* Empresa / Links Extras */}
          <div className="flex flex-col h-full justify-between gap-6">
            <div>
              <h4 className="font-syncopate font-bold text-white text-sm mb-6 uppercase tracking-wider">Empresa</h4>
              <ul className="space-y-2 text-sm font-light text-gray-400">
                <li><Link href="#" className="hover:text-accent transition-colors">Nosotros</Link></li>
                <li><Link href="#" className="hover:text-accent transition-colors">Servicio Técnico</Link></li>
                <li><Link href="#" className="hover:text-accent transition-colors">Casos de Éxito</Link></li>
                <li><Link href="/blog" className="hover:text-accent transition-colors">Novedades y Noticias</Link></li>
              </ul>
            </div>
            
            <div className="bg-[#128C7E]/10 rounded-2xl p-6 border border-[#25D366]/20 mt-auto">
              <h4 className="font-syncopate font-bold text-white text-sm mb-2 flex items-center gap-2">
                <MessageCircle className="w-4 h-4 text-[#25D366]" /> Atención Inmediata
              </h4>
              <p className="text-xs font-light text-gray-300 mb-4">Asistencia rápida para emergencias técnicas vía chat.</p>
              <a href="https://wa.me/584241941573" target="_blank" rel="noopener noreferrer" className="w-full bg-[#25D366] hover:bg-[#128C7E] text-white font-syncopate text-xs font-bold py-3 px-4 rounded transition-colors whitespace-nowrap flex items-center justify-center gap-2">
                <MessageCircle className="w-4 h-4" />
                Escribir al WhatsApp
              </a>
            </div>
          </div>
        </div>

        {/* Copyright bar */}
        <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs font-light text-gray-500">
            &copy; {new Date().getFullYear()} Hospitalar Venezuela. Todos los derechos reservados.
          </p>
          <div className="flex gap-6 text-xs font-light text-gray-500">
            <a href="#" className="hover:text-white transition-colors">Políticas de Privacidad</a>
            <a href="#" className="hover:text-white transition-colors">Términos Legales</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
