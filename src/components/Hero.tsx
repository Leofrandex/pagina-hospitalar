"use client";

import { ArrowRight, ShieldCheck, Cpu, HeartPulse, Clock } from "lucide-react";
import { ScrollReveal } from "./ScrollReveal";

const floatingStats = [
  {
    icon: ShieldCheck,
    value: "+180",
    label: "Instituciones abastecidas",
    pos: "top-[12%] right-[6%]",
    delay: "0s",
  },
  {
    icon: Cpu,
    value: "99.8%",
    label: "Uptime garantizado",
    pos: "top-[55%] right-[2%]",
    delay: "1.2s",
  },
  {
    icon: HeartPulse,
    value: "+40",
    label: "Años de experiencia",
    pos: "top-[30%] left-[2%]",
    delay: "0.6s",
  },
  {
    icon: Clock,
    value: "24/7",
    label: "Soporte técnico",
    pos: "top-[68%] left-[4%]",
    delay: "1.8s",
  },
];

export default function Hero() {
  return (
    <section className="relative w-full min-h-[92vh] flex items-center justify-center overflow-hidden bg-[#f8fafc]">
      {/* ── Dot Grid Background ── */}
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `radial-gradient(circle, #352E87 1px, transparent 1px)`,
          backgroundSize: "28px 28px",
          opacity: 0.065,
        }}
      />

      {/* ── Radial fade mask over dot grid ── */}
      <div
        className="absolute inset-0 z-0"
        style={{
          background:
            "radial-gradient(ellipse 80% 70% at 50% 50%, transparent 30%, #f8fafc 75%)",
        }}
      />

      {/* ── Atmospheric Glow Orbs ── */}
      {/* Primary blue orb — top left */}
      <div
        className="absolute z-0 rounded-full pointer-events-none"
        style={{
          width: "520px",
          height: "520px",
          top: "-100px",
          left: "-120px",
          background:
            "radial-gradient(circle, rgba(53,46,135,0.13) 0%, transparent 70%)",
          filter: "blur(40px)",
        }}
      />
      {/* Accent green orb — bottom right */}
      <div
        className="absolute z-0 rounded-full pointer-events-none"
        style={{
          width: "480px",
          height: "480px",
          bottom: "-80px",
          right: "-100px",
          background:
            "radial-gradient(circle, rgba(0,150,57,0.10) 0%, transparent 70%)",
          filter: "blur(40px)",
        }}
      />
      {/* CTA orange orb — center bottom */}
      <div
        className="absolute z-0 rounded-full pointer-events-none"
        style={{
          width: "360px",
          height: "360px",
          bottom: "-60px",
          left: "50%",
          transform: "translateX(-50%)",
          background:
            "radial-gradient(circle, rgba(242,106,54,0.07) 0%, transparent 70%)",
          filter: "blur(50px)",
        }}
      />

      {/* ── Floating Stats Cards ── */}
      {floatingStats.map(({ icon: Icon, value, label, pos, delay }) => (
        <div
          key={label}
          className={`absolute hidden xl:flex ${pos} z-20 items-center gap-3 bg-white/80 backdrop-blur-md border border-white/60 rounded-2xl px-4 py-3 shadow-lg shadow-primary/5`}
          style={{
            animation: `heroFloat 4s ease-in-out infinite`,
            animationDelay: delay,
          }}
        >
          <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-primary/8">
            <Icon className="w-5 h-5 text-primary" strokeWidth={1.5} />
          </div>
          <div>
            <p className="text-sm font-syncopate font-bold text-primary leading-none mb-0.5">
              {value}
            </p>
            <p className="text-[11px] text-gray-500 font-light leading-none">
              {label}
            </p>
          </div>
        </div>
      ))}

      {/* ── Centered Content ── */}
      <div className="relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* Badge — narrow container */}
        <div className="max-w-4xl mx-auto text-center">
          <ScrollReveal delay={0.1}>
            <span className="inline-flex items-center gap-2 text-primary font-syncopate font-bold tracking-[0.2em] text-xs mb-8 uppercase border border-primary/20 bg-primary/5 px-5 py-2.5 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-accent inline-block" />
              Excelencia en Tecnología Médica
              <span className="w-1.5 h-1.5 rounded-full bg-accent inline-block" />
            </span>
          </ScrollReveal>
        </div>

        {/* H1 — full max-w-7xl width so whitespace-nowrap never clips */}
        <div className="w-full text-center">
          <ScrollReveal delay={0.2}>
            <h1
              className="font-syncopate font-bold text-primary uppercase tracking-tight mb-8"
              style={{ fontSize: "clamp(1.2rem, 3.8vw, 3.8rem)", lineHeight: "1.1", wordBreak: "keep-all" }}
            >
              Unimos tecnología y vida
            </h1>
          </ScrollReveal>
        </div>

        {/* Subheading + CTAs — narrow container */}
        <div className="max-w-4xl mx-auto text-center">
          <ScrollReveal delay={0.3}>
            <p className="text-lg md:text-xl text-primary/60 mb-12 max-w-2xl mx-auto font-light tracking-wide leading-relaxed">
              Equipamiento médico de clase mundial para instituciones que exigen
              la más alta excelencia operativa e innovación tecnológica en
              Venezuela.
            </p>
          </ScrollReveal>

          {/* CTAs */}
          <ScrollReveal delay={0.4}>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <a href="#contacto" className="group flex items-center gap-2 bg-cta text-white font-syncopate font-bold text-sm tracking-widest px-10 py-5 rounded-md hover:bg-[#d95b2d] hover:shadow-2xl hover:shadow-cta/40 hover:-translate-y-1 transition-all duration-300 w-full sm:w-auto justify-center cursor-pointer">
                SOLICITAR ASESORÍA
                <ArrowRight className="w-5 h-5 ml-1 transition-transform duration-300 group-hover:translate-x-1" />
              </a>
            </div>
          </ScrollReveal>

          {/* Bottom divider hint */}
          <ScrollReveal delay={0.55}>
            <div className="mt-16 flex items-center justify-center gap-3 opacity-30">
              <div className="h-px w-16 bg-primary/40" />
              <div className="w-1.5 h-1.5 rounded-full bg-primary/40" />
              <div className="h-px w-16 bg-primary/40" />
            </div>
          </ScrollReveal>
        </div>
      </div>

      {/* ── Float keyframes injected inline ── */}
      <style>{`
        @keyframes heroFloat {
          0%, 100% { transform: translateY(0px); }
          50%       { transform: translateY(-10px); }
        }
      `}</style>
    </section>
  );
}
