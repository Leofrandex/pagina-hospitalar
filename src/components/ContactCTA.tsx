"use client";

import { ArrowRight, ArrowLeft, Mail, MapPin, Phone, ShieldCheck, CheckCircle2, ChevronDown } from "lucide-react";
import { ScrollReveal } from "./ScrollReveal";
import { useState } from "react";

export default function ContactCTA() {
  const [step, setStep] = useState(0);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    location: "",
    specialty: "",
    equipment: "",
  });

  const nextStep = () => {
    if (step < 4) setStep(step + 1);
  };
  
  const prevStep = () => {
    if (step > 0) setStep(step - 1);
  };

  const handleChange = (field: keyof typeof formData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert("Requerimiento enviado con éxito");
    // Form submission logic here
    setStep(0);
    setFormData({ name: "", location: "", specialty: "", equipment: "" });
  };

  return (
    <section className="bg-primary text-white relative overflow-hidden" id="contacto">
      {/* Decorative background elements */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-[#2a2468] z-0 hidden lg:block" />
      <div className="absolute -top-32 -left-32 w-96 h-96 bg-accent/20 rounded-full blur-[120px] z-0" />

      <div className="max-w-7xl mx-auto flex flex-col lg:flex-row relative z-10 w-full">
        {/* Left Side: Copy */}
        <div className="w-full lg:w-1/2 py-20 px-4 sm:px-6 lg:px-8 lg:pr-20 flex flex-col justify-center">
          <ScrollReveal>
            <span className="text-accent font-syncopate font-bold tracking-[0.3em] text-[10px] mb-6 uppercase block">
              Proyectemos su Éxito
            </span>
            <h2 className="text-4xl md:text-5xl lg:text-6xl font-syncopate font-bold mb-6 leading-[1.1]">
              ¿Listo para modernizar su clínica?
            </h2>
            <p className="text-gray-300 text-lg leading-relaxed font-light mb-0 max-w-lg">
              Nuestros ingenieros y especialistas B2B están listos para asesorarlo con tecnología médica de vanguardia.
            </p>
          </ScrollReveal>
        </div>

        {/* Right Side: Form Carousel */}
        <div className="w-full lg:w-1/2 py-20 px-4 sm:px-6 lg:px-8 bg-[#2a2468] flex items-center justify-center min-h-[600px]">
          <ScrollReveal delay={0.4} className="w-full">
            <div className="w-full max-w-md mx-auto bg-white rounded-3xl shadow-[0_40px_100px_rgba(0,0,0,0.3)] overflow-hidden text-primary relative min-h-[450px] flex flex-col">
              
              {/* Progress Indicator */}
              <div className="absolute top-0 left-0 w-full h-1.5 bg-gray-100 z-20">
                <div 
                  className="h-full bg-accent transition-all duration-500 ease-out"
                  style={{ width: `${((step + 1) / 5) * 100}%` }}
                />
              </div>

              {/* Form Content */}
              <div className="p-10 md:p-12 flex-1 flex flex-col relative mt-2">
                <form onSubmit={handleSubmit} className="flex flex-col flex-1 h-full justify-between">
                  
                  {/* Step 0: Name */}
                  <div className={`transition-all duration-500 absolute inset-x-10 md:inset-x-12 top-10 ${step === 0 ? 'opacity-100 translate-x-0 z-10' : 'opacity-0 -translate-x-10 pointer-events-none'}`}>
                    <h3 className="text-2xl font-syncopate font-bold mb-3 tracking-tight">Empecemos</h3>
                    <p className="text-gray-500 font-light mb-10 text-sm">Para brindarte la mejor asesoría, nos gustaría conocerte.</p>
                    <label className="block text-xs font-syncopate font-bold tracking-[0.2em] text-gray-400 mb-4 uppercase">¿Cuál es tu nombre?</label>
                    <input 
                      type="text" 
                      value={formData.name}
                      onChange={(e) => handleChange("name", e.target.value)}
                      className="w-full border-b-2 border-gray-100 py-3 focus:outline-none focus:border-accent transition-colors bg-transparent font-light text-xl"
                      placeholder="Ej. Dr. Carlos"
                    />
                  </div>

                  {/* Step 1: Location */}
                  <div className={`transition-all duration-500 absolute inset-x-10 md:inset-x-12 top-10 ${step === 1 ? 'opacity-100 translate-x-0 z-10' : step > 1 ? 'opacity-0 -translate-x-10 pointer-events-none' : 'opacity-0 translate-x-10 pointer-events-none'}`}>
                    <h3 className="text-xl font-syncopate font-bold mb-3 tracking-tight text-accent">¡Hola {formData.name || "Dr."}!</h3>
                    <p className="text-gray-500 font-light mb-10 text-sm">Queremos asegurar cobertura en tu zona.</p>
                    <label className="block text-xs font-syncopate font-bold tracking-[0.2em] text-gray-400 mb-4 uppercase">¿Desde dónde nos contactas?</label>
                    <input 
                      type="text" 
                      value={formData.location}
                      onChange={(e) => handleChange("location", e.target.value)}
                      className="w-full border-b-2 border-gray-100 py-3 focus:outline-none focus:border-accent transition-colors bg-transparent font-light text-xl"
                      placeholder="Ej. Caracas, Venezuela"
                    />
                  </div>

                  {/* Step 2: Specialty */}
                  <div className={`transition-all duration-500 absolute inset-x-10 md:inset-x-12 top-10 ${step === 2 ? 'opacity-100 translate-x-0 z-30' : step > 2 ? 'opacity-0 -translate-x-10 pointer-events-none' : 'opacity-0 translate-x-10 pointer-events-none'}`}>
                    <h3 className="text-2xl font-syncopate font-bold mb-3 tracking-tight text-primary">Tu Especialidad</h3>
                    <p className="text-gray-500 font-light mb-10 text-sm">Selecciona el rubro de tu interés.</p>
                    <label className="block text-xs font-syncopate font-bold tracking-[0.2em] text-gray-400 mb-4 uppercase">Especialidad</label>
                    <div className="relative">
                      {/* Dropdown Header */}
                      <div 
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                        className={`w-full border-2 rounded-xl px-4 py-3 flex items-center justify-between cursor-pointer transition-all duration-300 ${isDropdownOpen || formData.specialty ? 'border-accent bg-accent/5' : 'border-gray-100 hover:border-gray-200 bg-white'}`}
                      >
                        <span className={`font-light text-lg ${formData.specialty ? 'text-accent font-medium' : 'text-gray-400'}`}>
                          {formData.specialty || "Selecciona una opción"}
                        </span>
                        <ChevronDown className={`w-5 h-5 transition-transform duration-300 ${isDropdownOpen ? 'rotate-180 text-accent' : 'text-gray-400'}`} />
                      </div>

                      {/* Dropdown List */}
                      <div className={`absolute top-full left-0 w-full mt-2 bg-white rounded-xl shadow-[0_10px_40px_rgba(0,0,0,0.1)] border border-gray-100 overflow-hidden transition-all duration-300 origin-top z-50 ${isDropdownOpen ? 'opacity-100 scale-y-100 pointer-events-auto' : 'opacity-0 scale-y-95 pointer-events-none'}`}>
                        {["Imagenología", "Cardiología", "Anestesiología", "Otros"].map((spec, index) => (
                          <div
                            key={spec}
                            onClick={() => {
                              handleChange("specialty", spec);
                              setIsDropdownOpen(false);
                            }}
                            className={`px-5 py-3 cursor-pointer transition-colors font-light border-b border-gray-50 last:border-b-0 ${formData.specialty === spec ? 'bg-accent/10 text-accent font-medium' : 'text-gray-600 hover:bg-gray-50 hover:text-accent'}`}
                          >
                            {spec}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Step 3: Equipment */}
                  <div className={`transition-all duration-500 absolute inset-x-10 md:inset-x-12 top-10 ${step === 3 ? 'opacity-100 translate-x-0 z-10' : step > 3 ? 'opacity-0 -translate-x-10 pointer-events-none' : 'opacity-0 translate-x-10 pointer-events-none'}`}>
                    <h3 className="text-2xl font-syncopate font-bold mb-3 tracking-tight text-primary">¿Qué buscas?</h3>
                    <p className="text-gray-500 font-light mb-10 text-sm">Detalla el equipo o solución en la que estás interesado.</p>
                    <textarea 
                      value={formData.equipment}
                      onChange={(e) => handleChange("equipment", e.target.value)}
                      className="w-full border-2 border-gray-100 rounded-xl p-4 focus:outline-none focus:border-accent transition-colors bg-transparent font-light min-h-[120px] resize-none"
                      placeholder="Ej. Un equipo de rayos X portátil..."
                    />
                  </div>

                  {/* Step 4: Review */}
                  <div className={`transition-all duration-500 absolute inset-x-10 md:inset-x-12 top-10 ${step === 4 ? 'opacity-100 translate-x-0 z-10' : 'opacity-0 translate-x-10 pointer-events-none'}`}>
                    <div className="flex items-center gap-3 mb-6">
                      <CheckCircle2 className="w-8 h-8 text-accent" />
                      <h3 className="text-2xl font-syncopate font-bold tracking-tight text-primary">Validación</h3>
                    </div>
                    <div className="space-y-4 bg-gray-50 p-5 rounded-xl border border-gray-100 mb-8">
                      <div>
                        <span className="text-[10px] uppercase font-bold text-gray-400 block mb-1">Nombre y Ubicación</span>
                        <p className="text-sm font-medium">{formData.name || "No definido"} - {formData.location || "No definida"}</p>
                      </div>
                      <div>
                        <span className="text-[10px] uppercase font-bold text-gray-400 block mb-1">Especialidad</span>
                        <p className="text-sm font-medium">{formData.specialty || "No definida"}</p>
                      </div>
                      <div>
                        <span className="text-[10px] uppercase font-bold text-gray-400 block mb-1">Interés</span>
                        <p className="text-sm font-medium line-clamp-2">{formData.equipment || "No definido"}</p>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 font-light text-center">Un especialista se pondrá en contacto pronto.</p>
                  </div>

                  {/* Navigation Buttons (Absolute bottom to stay fixed) */}
                  <div className="absolute bottom-10 left-10 right-10 flex gap-3 z-20">
                    {step > 0 && (
                      <button 
                        type="button" 
                        onClick={prevStep}
                        className="w-14 h-14 flex items-center justify-center bg-gray-50 text-gray-500 rounded-xl hover:bg-gray-100 transition-colors border border-gray-200"
                      >
                        <ArrowLeft className="w-5 h-5" />
                      </button>
                    )}
                    
                    {step < 4 ? (
                      <button 
                        type="button"
                        onClick={nextStep}
                        disabled={
                          (step === 0 && !formData.name) || 
                          (step === 1 && !formData.location)
                        }
                        className="flex-1 flex items-center justify-center gap-3 bg-primary text-white font-syncopate font-bold text-xs tracking-widest h-14 rounded-xl hover:bg-[#1a174c] transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-primary/20"
                      >
                        SIGUIENTE
                        <ArrowRight className="w-4 h-4" />
                      </button>
                    ) : (
                      <button 
                        type="submit"
                        className="flex-1 flex items-center justify-center gap-3 bg-cta text-white font-syncopate font-bold text-xs tracking-widest h-14 rounded-xl hover:bg-[#d95b2d] transition-all shadow-xl shadow-cta/30"
                      >
                        ENVIAR
                        <CheckCircle2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>

                </form>
              </div>

              {/* Secure footer */}
              <div className="bg-gray-50 px-10 py-5 text-center border-t border-gray-100 relative z-30">
                <span className="text-[10px] text-gray-400 font-syncopate font-bold tracking-widest flex justify-center items-center gap-2 uppercase">
                  <ShieldCheck className="w-4 h-4 text-accent" /> Datos Protegidos
                </span>
              </div>
            </div>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
}
