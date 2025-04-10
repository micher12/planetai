"use client";
import BackToTop from "@/components/BackToTop";
import Header from "@/components/Header";
import { motion, useInView } from "motion/react";
import Image from "next/image";
import { useRef } from "react";

export default function Home() {

  const ref1 = useRef(null);
  const ref2 = useRef(null);
  const ref3 = useRef(null);
  const inView1 = useInView(ref1, {once: true, amount: 0.2});
  const inView2 = useInView(ref2, {once: true, amount: 0.2});
  const inView3 = useInView(ref3, {once: true, amount: 0.2});

  return(
    <>
      <Header />
      <main className="min-h-screen text-white home relative z-10" >
        <div className={`container-xl h-screen flex items-center justify-center`}>

          <h2 className="text-5xl sm:text-6xl font-black font-montserrat text-center fadeIn">Seja bem vindo a PlanetAI!</h2>
     
        </div>
      </main>
      <section id="sobre" className="bg-slate-900 text-white py-24">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            
            <motion.div 
            initial={{opacity: 0, filter: "blur(10px)", y: 50}}
            animate={ inView1 ? {opacity: 1, filter: "blur(0)", y: 0} : {opacity: 0, filter: "blur(10px)", y: 50} }
            transition={{
                duration: 0.6,
            }}
            ref={ref1}
            className="bg-slate-800/70 backdrop-blur-sm rounded-2xl p-8 shadow-xl mb-16">
                <h2 className="text-4xl md:text-6xl font-extrabold mb-12 bg-clip-text text-transparent bg-gradient-to-r from-rose-400 to-pink-600 flex items-center gap-3">Sobre a PlanetAI <Image src={"/planet.png"} width={50} height={50} alt="Logo" /></h2>
                <p className="text-lg md:text-xl leading-relaxed text-slate-200">
                    A <span className="text-rose-500 font-semibold">PlanetAI</span> é uma inteligência artificial desenvolvida para analisar o conteúdo de notícias relacionadas ao meio ambiente. A ferramenta avalia automaticamente cada notícia e a classifica como Positiva, Negativa ou Irrelevante, oferecendo ao usuário uma visão clara sobre os temas e acontecimentos que impactam o planeta.
                </p>
            </motion.div>

            <div className="w-full h-[2px] rounded-full my-16 bg-gradient-to-r from-transparent via-slate-200/50 to-transparent"></div>
            
            <motion.div 
            initial={{opacity: 0, filter: "blur(10px)", y: 50}}
            animate={ inView2 ? {opacity: 1, filter: "blur(0)", y: 0} : {opacity: 0, filter: "blur(10px)", y: 50} }
            transition={{
                duration: .6,
            }}
            ref={ref2}
            className="bg-slate-800/70 backdrop-blur-sm rounded-2xl p-8 shadow-xl mb-16">
                <h2 className="text-4xl md:text-6xl font-extrabold mb-12 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-600">Como funciona?</h2>
                <p className="text-lg md:text-xl leading-relaxed text-slate-200 mb-12">
                    Buscamos as últimas notícias sobre o <span className="text-blue-400 font-semibold">meio ambiente.</span> A partir dessas informações, nosso sistema utiliza um modelo treinado para analisar o conteúdo e determinar se a notícia trata de algo positivo, negativo ou, caso não esteja relacionada ao tema ambiental, é considerada irrelevante.
                </p>
                <a href="/classify" className="block w-full sm:w-fit text-center sm:text-left bg-gradient-to-r from-rose-500 to-pink-600 text-white font-bold text-md sm:text-xl md:text-2xl uppercase px-6 sm:px-12 py-4 rounded-xl shadow-lg hover:shadow-rose-500/25 hover:scale-[1.02] mytransition">
                    Classificar
                </a>

            </motion.div>

            <div className="w-full h-[2px] my-16 bg-gradient-to-r from-transparent via-slate-200/50 to-transparent"></div>
            
            <motion.div 
            initial={{opacity: 0, filter: "blur(10px)", y: 50}}
            animate={ inView3 ? {opacity: 1, filter: "blur(0)", y: 0} : {opacity: 0, filter: "blur(10px)", y: 50} }
            transition={{
                duration: .6,
            }}
            ref={ref3}
            className="bg-slate-800/70 rounded-2xl p-8 shadow-xl mb-16">
                <h2 className="text-4xl md:text-6xl font-extrabold mb-12 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-teal-600">Notícias já analisadas</h2>
                <p className="text-lg md:text-xl leading-relaxed text-slate-200 mb-12">
                    Acesse nossa base de dados com várias de notícias já avaliadas pela PlanetAI. Você poderá acompanhar como as questões ambientais têm evoluído ao longo do tempo, entendendo com mais clareza os acontecimentos que moldam o futuro do nosso planeta.
                </p>
                <a href="/results" className="block w-full text-center sm:text-left sm:w-fit bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-bold text-md sm:text-xl uppercase px-6 sm:px-12 py-4 rounded-lg shadow-lg hover:shadow-blue-500/25 hover:scale-[1.02] mytransition">
                    Ver Histórico Completo
                </a>

            </motion.div>

          </div>
        </div>
      </section>
      <BackToTop />
    </>
  )
}
