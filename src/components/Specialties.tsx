import {
  Scan,
  HeartPulse,
  Syringe,
  Flower2,
  Bone,
  Scissors,
  Sparkles,
  Wand2,
  Slice,
  Stethoscope,
  Baby,
  Ear,
  Droplets,
} from "lucide-react";
import { ScrollReveal } from "./ScrollReveal";

const specialties = [
  {
    name: "Radiología",
    icon: Scan,
    desc: "Imágenes diagnósticas",
    products: ["Rayos X Digital", "Tomógrafos", "Resonadores", "Arcos en C"],
  },
  {
    name: "Cardiología",
    icon: HeartPulse,
    desc: "Cuidado cardiovascular",
    products: ["Ecógrafos Cardiológicos", "Monitores Multiparámetro", "Desfibriladores", "Electrocardiógrafos"],
  },
  {
    name: "Anestesia",
    icon: Syringe,
    desc: "Quirófano moderno",
    products: ["Máquinas de Anestesia", "Monitores de Gases", "Ventiladores", "Vaporizadores"],
  },
  {
    name: "Ginecología",
    icon: Flower2,
    desc: "Atención maternal",
    products: ["Ecógrafos 4D", "Doppler Fetal", "Mesas Ginecológicas", "Colposcopios"],
  },
  {
    name: "Traumatología",
    icon: Bone,
    desc: "Recuperación física",
    products: ["Densitómetros Óseos", "Arcos en C", "Sierras Quirúrgicas", "Motores Ortopédicos"],
  },
  {
    name: "Quirófano",
    icon: Scissors,
    desc: "Equipamiento quirúrgico",
    products: ["Lámparas Cialíticas", "Mesas Quirúrgicas", "Electrobisturíes", "Torres de Laparoscopia"],
  },
  {
    name: "Medicina Estética",
    icon: Sparkles,
    desc: "Tecnología no invasiva",
    products: ["Láseres Estéticos", "Radiofrecuencia Corporal", "Hydrafacial", "Depilación Láser"],
  },
  {
    name: "Cirugía Plástica",
    icon: Wand2,
    desc: "Precisión reconstructiva",
    products: ["Láseres CO₂ Fraccionados", "Equipos de Liposucción", "Electrobisturíes", "Lámparas Quirúrgicas"],
  },
  {
    name: "Cirugía General",
    icon: Slice,
    desc: "Mínima invasión",
    products: ["Torres de Laparoscopia", "Electrobisturíes", "Insufladores", "Instrumental Quirúrgico"],
  },
  {
    name: "Gastroenterología",
    icon: Stethoscope,
    desc: "Endoscopía digestiva",
    products: ["Videoendoscopios", "Videocolonoscopios", "Torres de Endoscopia", "Lavadoras de Endoscopios"],
  },
  {
    name: "Neonatología",
    icon: Baby,
    desc: "Cuidado del recién nacido",
    products: ["Incubadoras", "Cunas Térmicas", "Ventiladores Neonatales", "Lámparas de Fototerapia"],
  },
  {
    name: "ORL",
    icon: Ear,
    desc: "Otorrinolaringología",
    products: ["Videonasofibroscopios", "Unidades ORL", "Audiómetros", "Implantes Cocleares"],
  },
  {
    name: "Urología",
    icon: Droplets,
    desc: "Diagnóstico y tratamiento",
    products: ["Ecógrafos Urológicos", "Litotriptores", "Resectoscopios", "Cistoscopios"],
  },
];

export default function Specialties() {
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

        {/* Flex en vez de grid: la lista es impar y así la última fila queda centrada. */}
        <div className="flex flex-wrap justify-center gap-4">
          {specialties.map((item, index) => {
            const Icon = item.icon;
            return (
              <div
                key={item.name}
                className="w-full sm:w-[calc(50%-0.5rem)] lg:w-[calc(25%-0.75rem)]"
              >
                <ScrollReveal delay={(index % 4) * 0.05}>
                  <div className="group relative h-64 bg-gray-50 border border-transparent rounded-2xl overflow-hidden hover:bg-white hover:border-gray-100 hover:shadow-[0_20px_50px_rgba(53,46,135,0.08)] transition-all duration-500 cursor-pointer flex flex-col justify-center items-center text-center p-6">
                    {/* Estado por defecto */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center transition-all duration-500 opacity-100 group-hover:opacity-0 group-hover:scale-95 px-3 py-4">
                      <div className="w-14 h-14 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-4 text-primary group-hover:scale-110 transition-transform duration-500">
                        <Icon className="w-7 h-7" />
                      </div>
                      <h3 className="font-syncopate font-bold text-[12px] xl:text-sm text-primary tracking-tight xl:tracking-wide whitespace-nowrap">{item.name}</h3>
                      <p className="text-[10px] text-gray-400 mt-2 uppercase tracking-widest">{item.desc}</p>
                    </div>

                    {/* Revelado al hover: los cuatro productos de la especialidad */}
                    <div className="absolute inset-0 bg-primary translate-y-full group-hover:translate-y-0 transition-transform duration-500 flex flex-col items-center justify-center px-6 py-7">
                      <h3 className="font-syncopate font-bold text-[10px] xl:text-[11px] text-white mb-4 tracking-wider uppercase whitespace-nowrap">
                        {item.name}
                      </h3>
                      <ul className="text-[11px] text-white/70 w-full text-center leading-snug">
                        {item.products.map((prod) => (
                          <li
                            key={prod}
                            className="border-b border-white/10 py-2 last:border-0 last:pb-0 first:pt-0 px-1"
                          >
                            {prod}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </ScrollReveal>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
