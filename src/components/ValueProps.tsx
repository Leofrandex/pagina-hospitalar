import { ShieldCheck, Globe, Cpu, GraduationCap, Lightbulb } from "lucide-react";
import { ScrollReveal } from "./ScrollReveal";
import { BrandShape } from "./BrandShape";

export default function ValueProps() {
  return (
    <section className="py-24 bg-[#f8fafc] relative overflow-hidden" id="soporte">
      {/* Subtle Dot Pattern Background */}
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `radial-gradient(circle, #352E87 1px, transparent 1px)`,
          backgroundSize: "32px 32px",
          opacity: 0.04,
        }}
      />
      {/* Faint Glows to add life */}
      <div className="absolute top-20 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[100px] pointer-events-none z-0 text-transparent" />
      <div className="absolute bottom-10 left-10 w-[400px] h-[400px] bg-accent/5 rounded-full blur-[100px] pointer-events-none z-0 text-transparent" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <ScrollReveal>
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-syncopate font-bold text-primary mb-6">
              El Estándar Hospitalar
            </h2>
            <div className="w-24 h-1 bg-accent mx-auto rounded-full mb-8" />
            <p className="text-gray-600 max-w-3xl mx-auto text-lg leading-relaxed font-light">
              Desde 1982 Hospitalar trabaja de la mano con las mejores marcas de fabricantes a nivel internacional, que se encuentran a la vanguardia del desarrollo tecnológico con resultados clínicos comprobados. Nuestra propuesta de valor trasciende la venta de equipos. Entregamos soluciones integrales que garantizan la continuidad operativa.
            </p>
          </div>
        </ScrollReveal>

        {/* Top Grid: Primary Features (3 Cards) */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Card 1: Soporte (Blue) */}
          <ScrollReveal delay={0.1} className="h-full" overflowHidden={false}>
            <div className="group bg-white/70 backdrop-blur-sm p-10 rounded-2xl border border-gray-100/50 hover:bg-white hover:shadow-[0_30px_60px_rgba(53,46,135,0.1)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden h-full z-10 flex flex-col items-start">
              <BrandShape className="absolute -top-4 -right-4 w-40 h-40 text-primary/5 -z-10 group-hover:text-primary/10 transition-all duration-500 group-hover:scale-110 rotate-90" />
              
              <div className="w-16 h-16 bg-white shadow-sm border border-gray-100 rounded-2xl flex items-center justify-center mb-8 group-hover:bg-primary group-hover:text-white text-primary transition-all duration-500">
                <ShieldCheck className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-syncopate font-bold text-primary mb-4 uppercase text-left w-full">
                Soporte técnico
              </h3>
              <p className="text-gray-600 leading-relaxed font-light text-left flex-1">
                Personal técnico local, repuestos garantizados y un tiempo de respuesta inmediato para evitar que su equipo se detenga.
              </p>
            </div>
          </ScrollReveal>

          {/* Card 2: Respaldo (Orange) */}
          <ScrollReveal delay={0.2} className="h-full" overflowHidden={false}>
            <div className="group bg-white/70 backdrop-blur-sm p-10 rounded-2xl border border-gray-100/50 hover:bg-white hover:shadow-[0_30px_60px_rgba(242,106,54,0.1)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden h-full z-10 flex flex-col items-start">
              <BrandShape className="absolute -top-4 -right-4 w-40 h-40 text-cta/5 -z-10 group-hover:text-cta/10 transition-all duration-500 group-hover:scale-110 -scale-x-100" />
              
              <div className="w-16 h-16 bg-white shadow-sm border border-gray-100 rounded-2xl flex items-center justify-center mb-8 group-hover:bg-cta group-hover:text-white text-cta transition-all duration-500">
                <Globe className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-syncopate font-bold text-primary mb-4 uppercase text-left w-full">
                Respaldo Global
              </h3>
              <p className="text-gray-600 leading-relaxed font-light text-left flex-1">
                Partners oficiales de las marcas médicas más robustas y confiables a nivel mundial, proveyendo calidad del primer mundo a todos nuestros clientes.
              </p>
            </div>
          </ScrollReveal>

          {/* Card 3: Tecnologia (Green) */}
          <ScrollReveal delay={0.3} className="h-full" overflowHidden={false}>
            <div className="group bg-white/70 backdrop-blur-sm p-10 rounded-2xl border border-gray-100/50 hover:bg-white hover:shadow-[0_30px_60px_rgba(0,150,57,0.1)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden h-full z-10 flex flex-col items-start">
              <BrandShape className="absolute -top-4 -right-4 w-40 h-40 text-accent/5 -z-10 group-hover:text-accent/10 transition-all duration-500 group-hover:scale-110 rotate-180" />

              <div className="w-16 h-16 bg-white shadow-sm border border-gray-100 rounded-2xl flex items-center justify-center mb-8 group-hover:bg-accent group-hover:text-white text-accent transition-all duration-500">
                <Cpu className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-syncopate font-bold text-primary mb-4 uppercase text-left w-full">
                Excelencia Tecnológica
              </h3>
              <p className="text-gray-600 leading-relaxed font-light text-left flex-1">
                Impulsamos la modernización de su institución con equipos de vanguardia en automatización e imagenología.
              </p>
            </div>
          </ScrollReveal>
        </div>

        {/* Visual Separator element per user request */}
        <ScrollReveal delay={0.4}>
          <div className="flex items-center justify-center gap-4 py-14 opacity-50">
            <div className="h-[2px] w-12 md:w-32 bg-gradient-to-r from-transparent to-primary/40 rounded-full" />
            <div className="flex gap-3">
              <div className="w-2 h-2 rounded-full bg-primary/20" />
              <div className="w-2 h-2 rounded-full bg-accent/60" />
              <div className="w-2 h-2 rounded-full bg-primary/20" />
            </div>
            <div className="h-[2px] w-12 md:w-32 bg-gradient-to-l from-transparent to-primary/40 rounded-full" />
          </div>
        </ScrollReveal>

        {/* Bottom Grid: Secondary Features (2 Cards) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Card 4: Educacion continua (Indigo) */}
          <ScrollReveal delay={0.5} className="h-full w-full" overflowHidden={false}>
            <div className="group bg-white/70 backdrop-blur-sm p-8 md:p-10 rounded-2xl border border-gray-100/50 hover:bg-white hover:shadow-[0_30px_60px_rgba(79,70,229,0.1)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden h-full z-10 flex flex-col md:flex-row gap-6 items-start w-full">
              <BrandShape className="absolute -top-4 -right-4 w-40 h-40 text-indigo-500/5 -z-10 group-hover:text-indigo-500/10 transition-all duration-500 group-hover:scale-110 rotate-45" />

              <div className="w-14 h-14 bg-white shadow-sm border border-gray-100 rounded-2xl flex items-center justify-center shrink-0 group-hover:bg-indigo-500 group-hover:text-white text-indigo-500 transition-all duration-500">
                <GraduationCap className="w-7 h-7" />
              </div>
              <div className="flex flex-col flex-1 justify-center min-h-[4rem]">
                <h3 className="text-xl font-syncopate font-bold text-primary mb-3 uppercase text-left">
                  Educación continua
                </h3>
                <p className="text-gray-600 leading-relaxed font-light text-left">
                  Ofrecemos a nuestros clientes cursos especializados en el uso de nuestras tecnologías.
                </p>
              </div>
            </div>
          </ScrollReveal>

          {/* Card 5: Proyectos Especiales (Sky) */}
          <ScrollReveal delay={0.6} className="h-full w-full" overflowHidden={false}>
            <div className="group bg-white/70 backdrop-blur-sm p-8 md:p-10 rounded-2xl border border-gray-100/50 hover:bg-white hover:shadow-[0_30px_60px_rgba(14,165,233,0.1)] hover:-translate-y-2 transition-all duration-500 cursor-pointer relative overflow-hidden h-full z-10 flex flex-col md:flex-row gap-6 items-start w-full">
              <BrandShape className="absolute -top-4 -right-4 w-40 h-40 text-sky-500/5 -z-10 group-hover:text-sky-500/10 transition-all duration-500 group-hover:scale-110 -rotate-45" />

              <div className="w-14 h-14 bg-white shadow-sm border border-gray-100 rounded-2xl flex items-center justify-center shrink-0 group-hover:bg-sky-500 group-hover:text-white text-sky-500 transition-all duration-500">
                <Lightbulb className="w-7 h-7" />
              </div>
              <div className="flex flex-col flex-1 justify-center min-h-[4rem]">
                <h3 className="text-xl font-syncopate font-bold text-primary mb-3 uppercase text-left">
                  Proyectos especiales
                </h3>
                <p className="text-gray-600 leading-relaxed font-light text-left">
                  ¿Quiere iniciar su propio Centro de Salud o tiene alguna idea innovadora? Pregunte por nuestro asesoramiento.
                </p>
              </div>
            </div>
          </ScrollReveal>

        </div>
      </div>
    </section>
  );
}

