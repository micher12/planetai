"use client";

import Alert from "@/components/Alert";
import BackToTop from "@/components/BackToTop";
import Footer from "@/components/Footer";
import Header from "@/components/Header";
import Skeleton from "@/components/Skeleton";
import { faXmark, faExternalLink } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useEffect, useState } from "react";

interface noticia {
    title: string,
    description: string,
    url: string,
    class: string,
    date: string
}

interface popUp{
    title: string,
    description: string,
    url: string,
    class: string,
    date: string,
    current: boolean,
}

export default function Classify(){

    const [status, setStatus] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [noticias, setNoticias] = useState<noticia[] | null>(null);
    const [protocolo, setProtocolo] = useState<string[] | null>(null);
    const [type, setType] = useState<"sucesso" | "erro" | null>(null);
    const [message, setMessage] = useState<string>("");
    const [openPopUp, setOpenPopUp] = useState<popUp | null>(null);

    async function sleep(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    useEffect(()=>{

        const timer = setTimeout(()=>{
            setType(null)
            setMessage("")
        },3800);

        return ()=>{
            clearTimeout(timer)
        }
      
    },[type, message])

    async function classify(){

        setLoading(true);
        setNoticias(null);
        setStatus("Classificando notícias...")

        try {

            const [preNoticiasnoticias, protocoloResponse] = await Promise.all([
                fetch("/api/newsclassify",{method: "POST"}).then(res => res.json()),
                fetch("/api/getprotocolo", {method: "POST",}).then(res => res.json()),
            ]);

            setStatus("Salvando dados...")

            await fetch("/api/savenews",{
                method: "POST",
                body: JSON.stringify(preNoticiasnoticias.noticias)
            }).then(res => res.json())

            if(preNoticiasnoticias.sucesso === "ok")
                setNoticias(preNoticiasnoticias.noticias)

            setProtocolo(protocoloResponse)

            setType("sucesso")
            setMessage("Classificação realizada com sucesso!")
            setStatus(null)

        } catch (error) {
            setType("erro")
            setMessage("Ocorreu um erro durante a classificação!")
        }finally{
            setLoading(false);
        }

    }



    return(
        <>
        <Header />
        <main className="min-h-screen bg-slate-900 text-white py-32">
            <div className="container">
                <h2 className="text-3xl font-bold md:text-5xl fadeIn">Classificador de notícias</h2>
                
                {status && ( <div key={status} className="fadeIn"><h2 className={`${loading && "shiny-text"} mt-5 text-xl font-semibold `}>{status}</h2></div>)}

                <div onClick={classify} className="bg-blue-600 hover:bg-blue-700 w-fit font-bold text-xl sm:text-2xl rounded-lg px-6 py-1 sm:px-12 sm:py-2 mt-6 cursor-pointer scale mytransition fadeIn">Classificar!</div>

                {(loading && !noticias) && <Skeleton type="news" />}
                {noticias && protocolo &&
                    <>
                    <div className="w-full mt-10 rounded-2xl bg-slate-900/80 p-6 sm:p-8 shadow-xl border-1 border-slate-700/50">
                        <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">Análise de Protocolos de Rede</h2>

                        <div className="mt-1 space-y-6 flex flex-col md:flex-row justify-between">
      
                            <div className="pl-4 mt-2 space-y-3 border-l-2 border-slate-600">
                                <p className="text-sm sm:text-base text-slate-300">
                                    <span className="font-medium">Protocolo:</span> {protocolo[0] || 'Não disponível'}
                                </p>
                                <p className="text-sm sm:text-base text-slate-300">
                                    <span className="font-medium">Versão HTTP:</span> {protocolo[1] == "11" ? "HTTP/1.1" : " HTTP/2"}
                                </p>
                            </div>
                
                        </div>
                    </div>
                    <div className="w-full fadeIn mt-8">
                        <h2 className="text-3xl font-bold">Últimas notícias classificadas: </h2>
                        <h2 className="font-bold mt-1">{noticias.length} notícias encontradas</h2>
                    </div>
                    <div className="flex w-full flex-wrap justify-start gap-8 mt-8">
                        {noticias.map((noticia,index)=>{
                            let text_color;
                            let text_background;
    
                            if(noticia.class === "Irrelevante"){
                                text_color = "text-amber-100"
                                text_background = "bg-amber-600"
                            } else if(noticia.class === "Positiva"){
                                text_color = "text-green-100"
                                text_background = "bg-green-600"
                            }else{
                                text_color = "text-red-100"
                                text_background = "bg-red-600"
                            }

                            return(
                                <div
                                    onClick={()=>{setOpenPopUp({
                                        title: noticia.title,
                                        description: noticia.description,
                                        url: noticia.url,
                                        class: noticia.class,
                                        date: noticia.date,
                                        current: true
                                    })
                                    }}
                                    key={index}
                                    style={{animationDuration: `${(index * 0.2)+1}s`}}
                                    className="singleItem mytransition flex flex-col gap-3 p-5 bg-slate-800 rounded-xl text-white cursor-pointer scale border-slate-700 border hover:bg-slate-700 hover:border-slate-600 shadow-md hover:shadow-lg fadeIn"
                                >
                                    <h2 className="text-lg font-semibold text-gray-100 hover:text-white line-clamp-4">
                                        {noticia.title}
                                    </h2>

                                    <p className="text-sm text-gray-300 line-clamp-3">
                                        {noticia.description}
                                    </p>

                                    <span className={`${text_color} ${text_background} w-fit text-xs font-bold px-3 py-1 rounded-full`}>
                                        {noticia.class}
                                    </span>
                                </div>
                            )
                        })}
                    </div>
                    </>
                }
            </div>
        </main>
        <Alert type={type} message={message} />
        {openPopUp &&
            <>
            <div className="openPopUp p-8 relative bg-slate-900 rounded-xl shadow-2xl border border-slate-700 max-w-xl w-full mx-auto text-slate-100">

            <div 
                onClick={() => {setOpenPopUp(null)}} 
                className="absolute top-4 right-4 bg-slate-800 hover:bg-red-500 transition-colors duration-200 rounded-full w-8 h-8 flex items-center justify-center cursor-pointer"
            >
                <FontAwesomeIcon icon={faXmark} className="text-lg" />
            </div>
            

            <div className="mb-6 pb-4 border-b border-slate-700">
                <h2 className="text-slate-100 text-2xl font-bold font-montserrat mb-2 max-w-[96%]">
                {openPopUp.title}
                </h2>
                <div className="flex items-center gap-3">
                    <span className={`inline-block text-xs font-bold px-3 py-1 rounded-full bg-indigo-600 text-white`}>
                        {openPopUp.class}
                    </span>
                    <span className="text-slate-200 text-sm">
                        {new Date(openPopUp.date).toLocaleDateString("pt-BR")}
                    </span>
                </div>
            </div>
            

            <div className="mb-8">
                <p className="text-slate-300 font-montserrat leading-relaxed">
                {openPopUp.description}
                </p>
            </div>

            <div>
                <a 
                target="_blank" 
                href={openPopUp.url}
                className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 transition-colors px-5 py-2 rounded-lg font-medium text-white"
                >
                Abrir notícia
                <FontAwesomeIcon icon={faExternalLink} className="text-sm" />
                </a>
            </div>

            </div>
            <div className="popUpOverlay"></div>
            </>
        }
        <Footer />
        <BackToTop />
        </>
    )
}