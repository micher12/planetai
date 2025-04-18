"use client";

import { faGithub, faLinkedin } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Image from "next/image";
import Link from "next/link";

export default function Footer(){

    function navegation(e: React.MouseEvent<HTMLAnchorElement>){
        e.preventDefault();
        const el = e.target as HTMLAnchorElement;
        const path = window.location.pathname
        const id = el.getAttribute('href')?.split("/")[1].trim() as string;

        if(id === "" && path === "/"){
            window.scrollTo({top: 0, behavior: "smooth"});
            return
        }else if(path !== "/"){
            window.location.href = "/";
            return
        }
        
        const element = document.getElementById(id);

        if(element){
            element.scrollIntoView({behavior: "smooth"});
        }

    }

    return(
        <footer className="w-full bg-slate-950 py-10">
            <div className="container flex flex-col items-center justify-center gap-5">
                <div className="w-full flex flex-col sm:flex-row items-start justify-between gap-8">
                    <div className="flex items-center gap-2">
                        <Image src={"/planet.png"} width={50} height={60} alt="Logo" style={{width: "auto"}} />
                        <h2 className="font-bold text-xl text-slate-200">PlanetAI</h2>
                    </div>
                    <div className="flex flex-col gap-0.5">
                        <h2 className="font-bold  text-slate-200 mb-1">Navague</h2>
                        <Link onClick={navegation} href="/" className="text-slate-200 hover:text-white text-sm font-semibold">Início</Link>
                        <Link onClick={navegation} href="/sobre" className="text-slate-200 hover:text-white text-sm font-semibold">Sobre</Link>
                        <Link href="/results" className="text-slate-200 hover:text-white text-sm font-semibold">Histórico</Link>
                        <Link href="/classify" className="text-slate-200 hover:text-white text-sm font-semibold">Classificar</Link>
                    </div>
                    <div className="flex flex-col gap-0.5">
                        <h2 className="font-bold  text-slate-200 mb-1">Redes sociais</h2>
                        <div className="flex items-center gap-2">
                            <Link target="_blank" href={"https://github.com/micher12"} className="text-slate-200 border rounded-lg w-fit p-1 px-2 scale mytransition hover:bg-slate-700" ><FontAwesomeIcon icon={faGithub} /></Link>
                            <Link target="_blank" href={"https://www.linkedin.com/in/michel-alves-da-silva-0a1834212/"} className="text-slate-200 border rounded-lg w-fit p-1 px-2 scale mytransition hover:bg-slate-700" ><FontAwesomeIcon icon={faLinkedin} /></Link>
                        </div>
                    </div>
                </div>

                <div className="w-full bg-gradient-to-r from-tranparent via-slate-200/20 to-transparent pt-0.5 rounded-full "></div>
                <p className="text-slate-200">Website and PlanetAI powered by | <a target="_blank" href="https://code12.vercel.app" className="font-semibold cursor-pointer hover:underline text-rose-500 hover:text-rose-600 mytransition">Michel</a> 2025</p>
            </div>
        </footer>
    )

}