import { Activity, HeartPulse, Syringe, Baby, Microscope, Brain, Bone, Eye, Stethoscope, Scissors } from "lucide-react";
import { ScrollReveal } from "./ScrollReveal";

export default function Specialties() {
  const specialties = [
    { 
      name: "Radiología", 
      icon: Activity, 
      desc: "Imágenes diagnósticas",
      products: ["Resonadores", "Tomógrafos", "Rayos X Digital"] 
    },
    { 
      name: "Cardiología", 
      icon: HeartPulse, 
      desc: "Cuidado cardiovascular",
      products: ["Ecógrafos", "Monitores", "Desfibriladores"] 
    },
    { 
      name: "Anestesia", 
      icon: Syringe, 
      desc: "Quirófano moderno",
      products: ["Máquinas de Anestesia", "Monitores de Gases"] 
    },
    { 
      name: "Ginecología", 
      icon: Baby, 
      desc: "Atención maternal",
      products: ["Ecógrafos 4D", "Doppler Fetal", "Mesas Ginecológicas"] 
    },
    { 
      name: "Laboratorio", 
      icon: Microscope, 
      desc: "Análisis preciso",
      products: ["Analizadores", "Microscopios", "Centrífugas"] 
    },
    { 
      name: "Neurología", 
      icon: Brain, 
      desc: "Estudios avanzados",
      products: ["Electroencefalógrafos", "Sistemas EMG", "Mapeo Cerebral"] 
    },
    { 
      name: "Traumatología", 
      icon: Bone, 
      desc: "Recuperación física",
      products: ["Densitómetros", "Fluoroscopia", "Sierras Quirúrgicas"] 
    },
    { 
      name: "Oftalmología", 
      icon: Eye, 
      desc: "Visión perfecta",
      products: ["OCT", "Lámparas de Hendidura", "Láseres Quirúrgicos"] 
    },
    { 
      name: "Medicina General", 
      icon: Stethoscope, 
      desc: "Consulta integral",
      products: ["Ecógrafos Portátiles", "Sistemas de Diagnóstico"] 
    },
    { 
      name: "Quirófano", 
      icon: Scissors, 
      desc: "Equipamiento quirúrgico",
      products: ["Lámparas Cialíticas", "Mesas Quirúrgicas", "Electrobisturí"] 
    }
  ];

  return (
    <section className="py-24 bg-white" id="equipos">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <ScrollReveal>
          <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
            <div className="max-w-2xl">
              <h2 className="text-3xl md:text-5xl font-syncopate font-bold text-primary mb-4">
                Nuestras Especialidades
              </h2>
              <div className="w-24 h-1 bg-accent rounded-full mb-6" />
              <p className="text-gray-600 text-lg leading-relaxed font-light">
                Proporcionamos equipamiento de primera línea para cada área de su centro médico. Todo lo que necesita para ofrecer el mejor cuidado.
              </p>
            </div>
            <button className="bg-white border border-gray-200 hover:bg-gray-50 text-primary font-syncopate font-bold text-[10px] tracking-widest px-8 py-4 rounded-md transition-all duration-300 cursor-pointer whitespace-nowrap shadow-sm">
              VER CATÁLOGO COMPLETO
            </button>
          </div>
        </ScrollReveal>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {specialties.map((item, index) => {
            const Icon = item.icon;
            return (
              <ScrollReveal key={index} delay={index * 0.05}>
                <div 
                  className="group relative h-56 bg-gray-50 border border-transparent rounded-2xl overflow-hidden hover:bg-white hover:border-gray-100 hover:shadow-[0_20px_50px_rgba(53,46,135,0.08)] transition-all duration-500 cursor-pointer flex flex-col justify-center items-center text-center p-6"
                >
                  {/* Default State */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center transition-all duration-500 opacity-100 group-hover:opacity-0 group-hover:scale-95 p-4">
                    <div className="w-14 h-14 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-4 text-primary group-hover:scale-110 transition-transform duration-500">
                      <Icon className="w-7 h-7" />
                    </div>
                    <h3 className="font-syncopate font-bold text-sm text-primary tracking-wide">{item.name}</h3>
                    <p className="text-[10px] text-gray-400 mt-2 uppercase tracking-widest">{item.desc}</p>
                  </div>
                  
                  {/* Hover Reveal State */}
                  <div className="absolute inset-0 bg-primary translate-y-full group-hover:translate-y-0 transition-transform duration-500 flex flex-col items-center justify-center p-6">
                    <h3 className="font-syncopate font-bold text-sm text-white mb-4 tracking-widest uppercase">{item.name}</h3>
                    <ul className="text-xs text-white/70 space-y-3 text-center w-full">
                      {item.products.map((prod, pIdx) => (
                        <li key={pIdx} className="border-b border-white/10 pb-2 last:border-0 truncate w-full px-2">
                          {prod}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </ScrollReveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
