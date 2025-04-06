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
          <h2 className="text-3xl sm:text-5xl font-bold mb-1">Sobre</h2>
          <p className="text-lg mt-5 w-4/5">A PlanetAI é uma inteligência artificial que utiliza análise de sentimento para identificar e classificar notícias relacionadas ao meio ambiente. A ferramenta avalia automaticamente o conteúdo das notícias e as categoriza em "Positiva", "Negativa" ou "Irrelevante", proporcionando aos usuários uma visão clara e objetiva sobre as tendências e impactos ambientais. </p>
          
          <div className="w-full h-0.5 bg-gradient-to-r from-transparent via-slate-200/50 to-transparent my-10 rounded-xl"></div>

          <h2 className="text-3xl sm:text-5xl font-bold mb-1">Como funciona ?</h2>
          <p className="text-lg mt-5 w-4/5">Recuperamos as últimas notícias voltadas ao <b className="text-blue-400">Meio Ambiente</b>, a partir delas o modelo neural irá começar a analisar e com base em seu treinamento irá classificar se a notícia trata-se de um assunto <b className="text-blue-400">Positivo, Negativo ou Irrelevante</b> caso não seja voltado para o meio ambiente.</p>

          <a href="/classify" className="block bg-rose-500 hover:bg-rose-600 mytransition scale w-fit text-center px-12 rounded py-2 mt-10 font-bold text-2xl cursor-pointer uppercase">Classificar</a>
        </div>
      </section>
    </>
  )
}
