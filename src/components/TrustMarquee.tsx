"use client";
import Image from "next/image";
import { ScrollReveal } from "./ScrollReveal";

const brands = [
  { name: "Siemens", src: "/logos/siemens-logo-diapo-REV-1-400x143.png" },
  { name: "Barco", src: "/logos/Barco-logo-diapo-400x143.png" },
  { name: "Cochlear", src: "/logos/Cochlear-logo-diapo-rev-2-400x143.png" },
  { name: "Deka", src: "/logos/Deka-logo-diapo.png" },
  { name: "Dräger", src: "/logos/Drager-logo-diapo-400x143.png" },
  { name: "Olympus", src: "/logos/Olympud-logo-rev-1-400x143.png" },
  { name: "Sonoscape", src: "/logos/Sonoscape-logo-diapo-400x143.png" },
  { name: "Sony", src: "/logos/Sony-logo-diapo-400x143.png" },
  { name: "Candela", src: "/logos/candela-logo-diapo-400x143.png" },
  { name: "Esaote", src: "/logos/esaote-logo-diapo-400x143.png" },
  { name: "Hydrafacial", src: "/logos/hydrafacial-logo-diapo-400x143.png" },
  { name: "Hyun Laser", src: "/logos/hyun-laser-400x143.png" },
  { name: "Inmode", src: "/logos/inmode-logo-diapo-400x143.png" },
  { name: "Medtronic", src: "/logos/medtronic-logo-diapo-400x143.png" },
  { name: "Mobile ODT", src: "/logos/mobile-odt-logo-diapo-400x143.png" },
];

export default function TrustMarquee() {
  const duplicatedBrands = [...brands, ...brands, ...brands, ...brands];

  return (
    <section className="py-20 bg-blue-950 border-y border-blue-900/50 overflow-hidden">
      <ScrollReveal>
        <div className="max-w-7xl mx-auto px-4 mb-12 text-center">
          <p className="text-xs font-syncopate text-blue-200/60 font-bold tracking-[0.3em] uppercase mb-4">
            Aliados en Tecnología Global
          </p>
          <h2 className="text-2xl md:text-4xl font-syncopate font-bold text-white tracking-tight">
            Marcas reconocidas a nivel mundial
          </h2>
        </div>
      </ScrollReveal>
      
      {/* Marquee Container */}
      <div className="relative flex w-full overflow-hidden py-10">
        <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-blue-950 to-transparent z-10 pointer-events-none" />
        <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-blue-950 to-transparent z-10 pointer-events-none" />
        
        {/* Adjusted speed to 120s for slow premium feel */}
        <div className="flex animate-[marquee_120s_linear_infinite] whitespace-nowrap min-w-max items-center">
          {duplicatedBrands.map((brand, i) => (
            <div key={i} className="mx-12 flex items-center justify-center group opacity-50 hover:opacity-100 transition-opacity duration-500">
              <div className="relative w-40 h-20 md:w-52 md:h-24">
                <Image 
                  src={brand.src} 
                  alt={`${brand.name} logo`} 
                  fill 
                  sizes="(max-w-768px) 160px, 208px"
                  className="object-contain transition-all duration-500" 
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <style jsx global>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
      `}</style>
    </section>
  );
}
