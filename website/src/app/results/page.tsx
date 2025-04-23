"use client"
import Header from "@/components/Header";
import { useEffect, useState } from "react";
import Chart, { ChartConfiguration, ChartConfigurationCustomTypesPerDataset, scales } from 'chart.js/auto'
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faExternalLink, faXmark } from "@fortawesome/free-solid-svg-icons";
import BackToTop from "@/components/BackToTop";
import Footer from "@/components/Footer";

interface noticia {
    id_noticia: number,
    title_noticia: string,
    description_noticia: string,
    url_noticia: string,
    class_noticia: string,
    date_noticia: string
}

interface chartData {
    irrelevante: number
    negativa: number
    positiva: number
    total: number
}

interface top5 {
    irrelevante: number
    negativa: number
    positiva: number
    total: number,
}

interface popUp{
    title: string,
    description: string,
    url: string,
    class: string,
    date: string,
}

export default function Results(){
 
    const [data, setData] = useState<noticia[] | null>(null);
    const [copyData, setCopyData] = useState<noticia[] | null>(null);
    const [quantidade, setQuantidade] = useState<chartData>({
        irrelevante: 0,
        negativa: 0,
        positiva: 0,
        total: 0
    });
    const [allData, setAllData] = useState<noticia[] | null>(null);
    const [copyallData, setCopyAllData] = useState<noticia[] | null>(null);
    const [showAll, setShowAll] = useState(false);
    const [openPopUp, setOpenPopUp] = useState<popUp | null>(null);
    const [top5, setTop5] = useState<top5>({
      irrelevante: 0,
      negativa: 0,
      positiva: 0,
      total: 0,
    });
    const [search, setSearch] = useState<string>("");
    const [categoria, setCategoria] = useState<string>("all");

    const configChart1: ChartConfiguration = 
    {
      type: 'pie',
      data: {
      labels: [
        "Positiva ("+((quantidade.positiva/quantidade.total)*100).toFixed(2)+"%)", 
        "Negativa ("+((quantidade.negativa/quantidade.total)*100).toFixed(2)+"%)", 
        "Irrelevante ("+((quantidade.irrelevante/quantidade.total)*100).toFixed(2)+"%)"],
        datasets: [{
            label: "Quantidade de notícias",
            data: [quantidade.positiva, quantidade.negativa, quantidade.irrelevante],
            backgroundColor: [
              "rgba(75, 192, 92, 0.9)",  
              "rgba(255, 99, 132, 0.9)",
              "rgba(255, 205, 86, 0.9)" 
            ],
            borderColor: [
              "rgb(75, 192, 92)",
              "rgb(255, 99, 132)",
              "rgb(255, 205, 86)"
            ],
            borderWidth: 2,
            hoverOffset: 15
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Todas notícias',
            font: {
              size: 16,
              weight: 'bold'
            },
            color: '#ffffff',
            padding: 20
          },
          legend: {
            display: true,
            position: 'bottom',
            labels: {
              color: "#ffffff",
              padding: 15,
              font: {
                size: 12
              }
            }
          },
        }
      }
    }

    const configChart2: ChartConfiguration = 
    {
      type: 'pie',
      data: {  
        labels: [
          "Positiva ("+((top5.positiva/top5.total)*100).toFixed(2)+"%)", 
          "Negativa ("+((top5.negativa/top5.total)*100).toFixed(2)+"%)", 
          "Irrelevante ("+((top5.irrelevante/top5.total)*100).toFixed(2)+"%)"],
      datasets: [{
        label: "Grafico",
        data: [top5.positiva, top5.negativa, top5.irrelevante],
        backgroundColor: [
          "rgba(75, 192, 92, 0.9)",  
          "rgba(255, 99, 132, 0.9)", 
          "rgba(255, 205, 86, 0.9)"  
        ],
        borderColor: [
          "rgb(75, 192, 92)",
          "rgb(255, 99, 132)",
          "rgb(255, 205, 86)"
        ],
        borderWidth: 2,
        hoverOffset: 15
      }]
      },
      options:{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Notícias dos últimos 5 dias',
            font: {
              size: 16,
              weight: 'bold'
            },
            color: '#ffffff',
            padding: 20
          },
          legend: {
            display: true,
            position: 'bottom',
            labels: {
                color: "#ffffff",
                padding: 15,
                font: {
                  size: 12
                }
            }
          },
        },
      }
    }

    useEffect(()=>{
        async function getdata(){
            const thisData = await fetch('/api/getdata', {
                method:"POST"
            })
            .then(res => res.json());

            const noticias: noticia[] = thisData.last5;

            const titles = new Set(noticias.map(n => n.title_noticia));
            const description = new Set(noticias.map(n => n.description_noticia));

            const preAllData: noticia[] = thisData.allData;

            const newAllData = preAllData.filter((noticia)=>{
                return (
                    !titles.has(noticia.title_noticia) && 
                    !description.has(noticia.description_noticia)
                )
            })

            const resultado = thisData.result[0];

            setData(noticias)
            setCopyData(noticias)
            setQuantidade(resultado)
            setAllData(newAllData)
            setCopyAllData(newAllData)
        }
        getdata()
    },[]);

    useEffect(()=>{
        if(copyData){
            const total = copyData.length
            
            const contadores = copyData.reduce((acc, val) => {
                if (val.class_noticia === "Positiva") {
                  acc.positiva += 1;
                } else if (val.class_noticia === "Negativa") {
                  acc.negativa += 1;
                } else if (val.class_noticia === "Irrelevante") {
                  acc.irrelevante += 1;
                }
                return acc;
            }, { positiva: 0, negativa: 0, irrelevante: 0 });

            setTop5({
                irrelevante: contadores.irrelevante,
                negativa: contadores.negativa,
                positiva: contadores.positiva,
                total: total,
            })

            const chartElement = document.getElementById("acquisitions") as HTMLCanvasElement | null;
            if (chartElement) {
                const myChart = new Chart(chartElement, configChart1);

                return () => {
                    myChart.destroy();
                }
            }
        }
    },[copyData]);

    useEffect(()=>{
        const top5noticias = document.getElementById("top5noticias") as HTMLCanvasElement | null;
        if (top5noticias) {
            const myChar = new Chart(top5noticias, configChart2);

            return () => {
                myChar.destroy();
            }
        }
    },[top5])

    useEffect(() => {
        if (data && allData) {
            const normalizeText = (text: string) => {
                return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
            }

            const normalizedSearch = normalizeText(search);

            const filteredData = data.filter((noticia) => {
                const matchesCategory = categoria === "all" || noticia.class_noticia === categoria;

                const matchesSearch = normalizeText(noticia.title_noticia).includes(normalizedSearch) || 
                                      normalizeText(noticia.description_noticia).includes(normalizedSearch);

                return matchesCategory && matchesSearch;
            });

            const restante = allData.filter((noticia) => {
                const matchesCategory = categoria === "all" || noticia.class_noticia === categoria;

                const matchesSearch = normalizeText(noticia.title_noticia).includes(normalizedSearch) || 
                                      normalizeText(noticia.description_noticia).includes(normalizedSearch);

                return matchesCategory && matchesSearch;
            });

            setCopyData(filteredData);
            setCopyAllData(restante);
        }
    }, [categoria, search]);

    function changeCategory(e: React.ChangeEvent<HTMLSelectElement>) {
        const el = e.target as HTMLSelectElement;

        setCategoria(el.value);
    }

    function changeSearch(e: React.ChangeEvent<HTMLInputElement>){
        const el = e.target as HTMLInputElement

        setSearch(el.value)
    }


    return(
        <>
        <Header />
        <main className="min-h-screen bg-slate-900 text-white py-32">
            <div className="container">
                <h2 className="text-3xl font-bold fadeIn">Histórico de Notícias: </h2>
                {copyData &&
                <>
                    <div className="chart-container">
                        <div className="chart-card fadeIn">
                            <canvas id="top5noticias"></canvas>
                        </div>
                        <div className="chart-card fadeIn">
                            <canvas id="acquisitions"></canvas>
                        </div>
                    </div>
                    <div className="flex flex-col md:flex-row w-full fadeIn items-start gap-5 sm:justify-between md:items-center mt-10">
                        <div className="flex flex-col gap-2">
                            <h2 className="text-lg font-semibold">Mostrando: {copyData.length} notícias dos últimos 5 dias:</h2>
                            <input onChange={changeSearch} placeholder="Queimadas" value={search} className="border rounded px-3 py-2" />
                        </div>

                        <div className="flex flex-col gap-2">
                            <span>Filtrar por categorias:</span>
                            <select onChange={changeCategory} className="border rounded px-3 py-1 categorias">
                                <option value="all" >Todas</option>
                                <option value="Positiva" >Positiva</option>
                                <option value="Negativa" >Negativa</option>
                                <option value="Irrelevante" >Irrelevante</option>
                            </select>
                        </div>
                    </div>
                    <div className="flex w-full flex-wrap justify-start gap-8 mt-10">

                      {copyData.map((noticia, index) => {

                        let text_color;
                        let text_background;

                        if(noticia.class_noticia === "Irrelevante"){
                            text_color = "text-amber-100"
                            text_background = "bg-amber-600"
                        } else if(noticia.class_noticia === "Positiva"){
                            text_color = "text-green-100"
                            text_background = "bg-green-600"
                        }else{
                            text_color = "text-red-100"
                            text_background = "bg-red-600"
                        }

                        return (
                            <div
                                onClick={()=>{setOpenPopUp({
                                    title: noticia.title_noticia,
                                    description: noticia.description_noticia,
                                    url: noticia.url_noticia,
                                    class: noticia.class_noticia,
                                    date: noticia.date_noticia,

                                })
                                }}
                                key={index}
                                style={{animationDuration: `${(index * 0.12)+1}s`}}
                                className={`singleItem mytransition flex flex-col gap-3 p-5 bg-slate-800 rounded-xl text-white cursor-pointer scale border-slate-700 border hover:bg-slate-700 hover:border-slate-600 shadow-md hover:shadow-lg fadeIn`}
                            >
                                <h2 className="text-lg font-semibold text-gray-100 hover:text-white line-clamp-4">
                                    {noticia.title_noticia}
                                </h2>

                                <p className="text-sm text-gray-300 line-clamp-3">
                                    {noticia.description_noticia}
                                </p>

                                <span className={`${text_color} ${text_background} w-fit text-xs font-bold px-3 py-1 rounded-full`}>
                                    {noticia.class_noticia}
                                </span>
                                
                            </div>
                        )
                      })}


                      {(showAll && copyallData) &&
                        <>
                            <div className="w-full pt-0.5 my-2 rounded-xl bg-gradient-to-r from-transparent via-slate-200/50 to-transparent"></div>
                            <div className="w-full fadeIn">
                                <h2 className="text-3xl font-bold">Restante das notícias</h2>
                                <h2 className="text-lg mt-1">Mostrando: {copyallData.length} Notícias restantes.</h2>
                            </div>

                            {copyallData.map((noticia, index) => {
                                
                                let text_color;
                                let text_background;

                                if(noticia.class_noticia === "Irrelevante"){
                                    text_color = "text-amber-100"
                                    text_background = "bg-amber-600"
                                } else if(noticia.class_noticia === "Positiva"){
                                    text_color = "text-green-100"
                                    text_background = "bg-green-600"
                                }else{
                                    text_color = "text-red-100"
                                    text_background = "bg-red-600"
                                }

                                return (
                                    <div
                                        onClick={()=>{setOpenPopUp({
                                            title: noticia.title_noticia,
                                            description: noticia.description_noticia,
                                            url: noticia.url_noticia,
                                            class: noticia.class_noticia,
                                            date: noticia.date_noticia,
                                        })
                                        }}
                                        key={index}
                                        style={{animationDuration: `${(index * 0.1)+1}s`}}
                                        className="singleItem mytransition flex flex-col gap-3 p-5 bg-slate-800 rounded-xl text-white cursor-pointer scale border-slate-700 border hover:bg-slate-700 hover:border-slate-600 shadow-md hover:shadow-lg fadeIn"
                                    >
                                        <h2 className="text-lg font-semibold text-gray-100 hover:text-white line-clamp-4">
                                            {noticia.title_noticia}
                                        </h2>

                                        <p className="text-sm text-gray-300 line-clamp-3">
                                            {noticia.description_noticia}
                                        </p>

                                        <span className={`${text_color} ${text_background} w-fit text-xs font-bold px-3 py-1 rounded-full`}>
                                            {noticia.class_noticia}
                                        </span>
                                    </div>
                                )
                            })}
                        </>
                      }

                    </div>

                    {!showAll && 
                      <div className="flex justify-center mt-4">
                        <button
                          className="bg-blue-600 text-white px-4 py-2 rounded cursor-pointer mytransition hover:bg-blue-500 scale font-bold text-2xl mt-10"
                          onClick={() => setShowAll(true)}
                        >
                            Visualizar todas as noticias
                        </button>
                      </div>
                    }

                </>
                }
            </div>
        </main>
        <Footer />
        <BackToTop/>
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
            <div className="popUpOverlay fadeIn-sm"></div>
            </>
        }
        </>
    )
}