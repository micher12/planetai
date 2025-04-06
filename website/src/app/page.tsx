"use client";
import Header from "@/components/Header";
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {

  const [mobile, setMobile] = useState(false);

  useEffect(()=>{
    function resizing(){
      const width = window.innerWidth
      if(width <= 960){
        setMobile(true);
      }else{
        setMobile(false);
      }
    }

    resizing();

    window.addEventListener('resize', resizing)
    return () => window.removeEventListener('resize', resizing)
  },[])

  return(
    <>
      <Header />
      <main className="min-h-screen text-white home relative z-10" style={{backgroundImage: !mobile ? "url('/background.jpg')" : "url('/backgroundMobile.jpg')", backgroundColor: "#030047"}}>
        <div className={`container-xl h-screen flex items-center justify-center`}>

          <h2 className="text-5xl sm:text-6xl font-black font-montserrat text-center">Seja bem vindo a PlanetAI!</h2>
     
        </div>
      </main>
      <section id="sobre" className=" bg-slate-900 text-white py-12">
        <div className="container">

            <h2 className="text-4xl md:text-6xl font-bold mb-6 text-slate-100">Sobre</h2>
            <p className="text-lg md:text-xl mt-5 md:w-4/5 leading-relaxed text-slate-200">
            A PlanetAI é uma inteligência artificial que utiliza análise de sentimento para identificar e classNameificar notícias relacionadas ao meio ambiente. A ferramenta avalia automaticamente o conteúdo das notícias e as categoriza em "Positiva", "Negativa" ou "Irrelevante", proporcionando aos usuários uma visão clara e objetiva sobre as tendências e impactos ambientais.
            </p>
            

            <div className="w-full pt-0.5 my-2 rounded-xl bg-gradient-to-r from-transparent via-slate-200/50 to-transparent my-16"></div>

            <h2 className="text-4xl md:text-6xl font-bold mb-6 text-slate-100">Como funciona?</h2>
            <p className="text-lg md:text-xl mt-5 md:w-4/5 leading-relaxed text-slate-200">
            Recuperamos as últimas notícias voltadas ao <span className="text-blue-500 font-semibold">Meio Ambiente</span>, a partir delas o modelo neural irá começar a analisar e com base em seu treinamento irá classNameificar se a notícia trata-se de um assunto <span className="text-blue-500 font-semibold">Positivo, Negativo ou Irrelevante</span> caso não seja voltado para o meio ambiente.
            </p>
            

            <a href="/classify" className="inline-block bg-gradient-to-r from-rose-500 to-pink-600 text-white font-bold text-xl md:text-2xl uppercase px-12 py-3 rounded-lg mt-10 mytransition scale hover:shadow-lg">
            Classificar
            </a>
            

            <h2 className="text-4xl md:text-6xl font-bold mb-6 mt-16 text-slate-100">Já classificados:</h2>
            <p className="text-lg md:text-xl mt-5 md:w-4/5 leading-relaxed text-slate-200">
            Explore nossa extensa base de dados de notícias ambientais já analisadas e categorizadas pela PlanetAI. Nosso histórico oferece insights valiosos sobre tendências ambientais globais e regionais, permitindo que você acompanhe a evolução das questões ambientais ao longo do tempo.
            </p>
            
            
            <a href="/results" className="inline-block bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-bold text-xl uppercase px-12 py-3 rounded-lg mt-8 mytransition scale hover:shadow-lg">
            Ver Histórico Completo
            </a>

        </div>
      </section>
    </>
  )
}
