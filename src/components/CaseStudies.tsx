"use client";
import { ChevronLeft, ChevronRight, Quote, Star, StarHalf } from "lucide-react";
import { useEffect, useRef, useState, useCallback } from "react";
import { ScrollReveal } from "./ScrollReveal";
import { BrandShape } from "./BrandShape";

const cases = [
  {
    id: 1,
    clinic: "Clínica Santa Sofía",
    person: "Lic. Charlo Andrade",
    role: "Gerente Administración",
    quote: "Mantenemos relaciones con la empresa Hospitalar desde el 2018 demostrando alto grado de responsabilidad con las obligaciones contraídas.",
    rating: 5
  },
  {
    id: 2,
    clinic: "Hospital de Clínicas Caracas",
    person: "Samir Camacho",
    role: "Director de Cadena de Suministros",
    quote: "Hemos mantenido buena relación comercial con Hospitalar, es una empresa seria y cumplida con las entregas de los equipos laser de alta tecnología, asesoría y servicio técnico por lo que nos permitimos recomendarla ampliamente.",
    rating: 5
  },
  {
    id: 3,
    clinic: "Hospital de Clínicas Caracas",
    person: "Ing. Carmen Barrios",
    role: "Directora de Cadena de Suministros",
    quote: "Mantenemos relaciones comerciales con Hospitalar desde el 2013, pudiendo dar fe que los servicios prestados ha sido de nuestra entera satisfacción.",
    rating: 4.5
  },
  {
    id: 4,
    clinic: "Unimel Venezuela",
    person: "Dr. Victor Ollarves",
    role: "Médico Estético",
    quote: "Hospitalar es una empresa confiable de muchos años de experiencia y trayectoria, siempre atenta a responderte y resolver cualquier eventualidad. Además representan grandes marcas del mercado.",
    rating: 5
  },
  {
    id: 5,
    clinic: "Clínica Edelmira Araujo",
    person: "Dra. Paola Bravo",
    role: "Radiólogo",
    quote: "Hospitalar atendió todas mis dudas, con un trato amable y una garantía en los equipos con precios inigualables.",
    rating: 4.5
  },
  {
    id: 6,
    clinic: "Medicina Estética",
    person: "Dra. Cristina Premerl",
    role: "Médico Estético",
    quote: "Mi experiencia con Hospitalar estos 14 años ha sido excelente... ofrecen un servicio técnico que jamás me ha dejado mal y un equipo de ventas responsable no solo durante la venta sino también la post venta.",
    rating: 5
  },
  {
    id: 7,
    clinic: "Clínica Santa Sofía",
    person: "Dra. Gusberly Zambrano",
    role: "Gerente Administración",
    quote: "Estamos muy agradecidos con el equipo de Hospitalar, la atención y dedicación han sido super buenas. Mis compañeras y yo estamos felices utilizando el Eva Colpo.",
    rating: 5
  },
  {
    id: 8,
    clinic: "Clínica Nueva Caracas",
    person: "Dra. Gisela",
    role: "Especialista",
    quote: "La experiencia que nos brindó Hospitalar fue excelente en cuanto a la calidad de atención... Es una empresa trasparente que ademas ofrece diferentes opciones que se adaptan a la necesidad de cada cliente.",
    rating: 4.5
  }
];

const renderStars = (rating: number) => {
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    if (i <= Math.floor(rating)) {
      stars.push(<Star key={i} className="w-4 h-4 fill-cta text-cta" />);
    } else if (i === Math.ceil(rating) && !Number.isInteger(rating)) {
      stars.push(<StarHalf key={i} className="w-4 h-4 fill-cta text-cta" />);
    } else {
      stars.push(<Star key={i} className="w-4 h-4 text-gray-200" />);
    }
  }
  return <div className="flex gap-1 mb-4">{stars}</div>;
};

export default function CaseStudies() {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  const scrollLeft = useCallback(() => {
    if (scrollRef.current) {
      const card = scrollRef.current.firstElementChild as HTMLElement;
      if (!card) return;
      const gap = 24; 
      scrollRef.current.scrollBy({ left: -(card.clientWidth + gap), behavior: 'smooth' });
    }
  }, []);

  const scrollRight = useCallback(() => {
    if (scrollRef.current) {
      const card = scrollRef.current.firstElementChild as HTMLElement;
      const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current;
      if (!card) return;
      const gap = 24; 
      
      if (Math.ceil(scrollLeft + clientWidth) >= scrollWidth - 10) {
        scrollRef.current.scrollTo({ left: 0, behavior: 'smooth' });
      } else {
        scrollRef.current.scrollBy({ left: card.clientWidth + gap, behavior: 'smooth' });
      }
    }
  }, []);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (!isHovered) {
      timer = setInterval(() => {
        scrollRight();
      }, 4000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isHovered, scrollRight]);

  return (
    <section className="py-24 bg-gray-50 relative overflow-hidden" id="casos">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ScrollReveal>
          <div className="flex flex-col md:flex-row justify-between items-end mb-12 gap-6">
            <div className="max-w-2xl">
              <h2 className="text-3xl md:text-5xl font-syncopate font-bold text-primary mb-4">
                Casos de Éxito
              </h2>
              <div className="w-24 h-1 bg-cta rounded-full mb-6" />
              <p className="text-gray-600 text-lg leading-relaxed font-light">
                Descubra por qué las principales instituciones de salud de Venezuela confían en nosotros para equipar sus áreas más críticas.
              </p>
            </div>
            
            <div className="hidden md:flex items-center gap-3">
              <button 
                onClick={scrollLeft}
                className="p-3 rounded-full bg-white border border-gray-200 text-primary hover:bg-primary hover:text-white transition-all duration-300 cursor-pointer shadow-sm"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <button 
                onClick={scrollRight}
                className="p-3 rounded-full bg-white border border-gray-200 text-primary hover:bg-primary hover:text-white transition-all duration-300 cursor-pointer shadow-sm"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </ScrollReveal>

        {/* Carousel Container */}
        <div 
          ref={scrollRef}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          onTouchStart={() => setIsHovered(true)}
          onTouchEnd={() => setIsHovered(false)}
          className="flex overflow-x-auto snap-x snap-mandatory scrollbar-hide hide-scrollbar -mx-4 px-4 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8 gap-6 pt-4 pb-12"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {cases.map((cs) => (
            <div key={cs.id} className="w-[85vw] md:w-[400px] flex-shrink-0 snap-center">
              <div className="bg-white rounded-2xl border border-gray-100 border-t-4 border-t-cta shadow-[0_10px_30px_rgba(53,46,135,0.03)] p-8 relative overflow-hidden h-[460px] md:h-[420px] flex flex-col transition-transform duration-300 hover:-translate-y-2 group">
                <Quote className="w-16 h-16 text-cta/10 absolute top-6 right-6 transition-transform duration-500 group-hover:scale-110" />
                
                {/* Forma 1 Branding Detail */}
                <BrandShape className="absolute -bottom-8 -right-8 w-40 h-40 text-primary/5 transition-transform duration-500 group-hover:scale-110" />
                <BrandShape className="absolute -top-12 -left-12 w-32 h-32 text-cta/5 rotate-180 transition-transform duration-500 group-hover:scale-110" />

                <div className="relative z-10 flex flex-col flex-grow">
                  <span className="inline-block self-start bg-cta/10 text-cta font-syncopate font-bold text-[10px] tracking-widest px-3 py-1 rounded-full mb-4 uppercase whitespace-normal">
                    {cs.clinic}
                  </span>
                  
                  {renderStars(cs.rating)}
                  
                  <blockquote className="text-sm md:text-base font-light text-gray-700 leading-relaxed mb-6 flex-grow whitespace-normal">
                    "{cs.quote}"
                  </blockquote>
                  
                  <div className="flex items-center gap-3 mt-auto pt-4 border-t border-gray-50">
                    <div className="w-8 h-1 bg-cta rounded-full flex-shrink-0" />
                    <div className="min-w-0">
                      <h4 className="font-syncopate font-bold text-primary text-xs tracking-wide truncate">{cs.person}</h4>
                      <p className="text-gray-400 font-light text-xs mt-0.5 truncate">{cs.role}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {/* Mobile Controls */}
        <div className="flex justify-center items-center gap-4 mt-2 md:hidden">
            <button 
              onClick={scrollLeft}
              className="p-3 rounded-full bg-white border border-gray-200 text-primary active:bg-primary active:text-white transition-colors"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button 
              onClick={scrollRight}
              className="p-3 rounded-full bg-white border border-gray-200 text-primary active:bg-primary active:text-white transition-colors"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
        </div>
      </div>
    </section>
  );
}
