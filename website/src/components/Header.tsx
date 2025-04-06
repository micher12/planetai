"use client";

import { AnimatePresence, motion } from "motion/react";
import Image from "next/image";
import Link from "next/link";
import { use, useEffect, useState, MouseEvent } from "react";


export default function Header() { 

    const [mobile, setMobile] = useState(false);
    const [monileIsOpen, setMobileIsOpen] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(()=>{

        function resizing(){
            const width = window.innerWidth;
            if(width <= 650){
                setMobile(true);
            }else{
                setMobile(false);
            }

        }

        resizing();

        setLoading(false);

        window.addEventListener('resize', resizing);
        return () => window.removeEventListener('resize', resizing);

    },[]);


    function openMenu(){
        setMobileIsOpen(!monileIsOpen)
    }


    function navegation(e: MouseEvent<HTMLAnchorElement>){
        e.preventDefault();
        const el = e.target as HTMLAnchorElement;
        const path = window.location.pathname
        const id = el.getAttribute('href')?.split("/")[1].trim() as string;

        if(id === "" && path === "/"){
            window.scrollTo({top: 0, behavior: "smooth"});
            openMenu();
            return
        }else if(path !== "/"){
            window.location.href = "/";
            return
        }
        
        const element = document.getElementById(id);

        if(element){
            element.scrollIntoView({behavior: "smooth"});
            openMenu();
        }

    }


    return(
        <>
        {!loading &&
        <header className="w-full fixed top-0 left-0 py-4 expandHeader z-50">
            <div className="container hover:container-xl mytransition">
                <div className="w-full backdrop-blur bg-slate-200/20 px-3 py-2 rounded-lg shadow-md">
                    <div className={`flex mytransition items-center ${!mobile ? "justify-between" : "justify-center"}`}>
                        {mobile ? 
                        <div onClick={openMenu} className="w-fit cursor-pointer text-slate-50 font-bold flex items-center gap-2 text-lg select-none">
                            <Image src={"/planet.png"} width={30} height={30} alt="Logo PlanetAI" /> PlanetAI
                        </div>
                        :
                        <Link href={"/"} className="w-fit text-slate-50 font-bold flex items-center gap-2 text-lg"><Image  src={"/planet.png"} width={30} height={30} alt="Logo PlanetAI" /> PlanetAI</Link>
                        }

                
                        {mobile ? <></> : 
                        <nav className="flex-1 flex justify-center text-slate-50 font-bold gap-6">
                            <Link onClick={navegation} href={"/"}>Início</Link>
                            <Link onClick={navegation} href={"/sobre"} className="cursor-pointer">Sobre</Link>
                            <Link href={"/results"}>Histórico</Link>
                        </nav>
                        }
                    
                        {mobile ? <></> :
                        <div className=" flex justify-center text-slate-50 font-bold gap-6 pr-5">
                            <Link  href={"/classify"} className="bg-rose-500 px-2 rounded">Classificar</Link>
                        </div>
                        }

                    </div>
                </div>

                <AnimatePresence>
                    {monileIsOpen &&

                        <motion.div
                        initial={{opacity: 0, y: -20}}
                        animate={{opacity: 1, y: 0}}
                        transition={{ duration: 0.3 }}
                        exit={{opacity: 0}}
                        className="text-white fixed top-20 left-0 container w-full"
                        >
                        
                            <motion.div 
                            initial={{height: 0, filter: "blur(10px)"}}
                            animate={{height: "170px", filter: "blur(0)"}}
                            transition={{ 
                                type: "spring",
                                stiffness: 180,
                                damping: 24,
                            }}
                            exit={{height: 0, filter: "blur(10px)"}}
                            className="bg-slate-50/20 p-3 py-5 rounded-lg flex items-center font-bold flex-col gap-3 enableblur animateBlur"
                            >
                        
                                <Link onClick={navegation} href={"/"}>Início</Link>
                                <Link onClick={navegation} href={"/sobre"} className="cursor-pointer">Sobre</Link>
                                <Link href={"/results"}>Histórico</Link>
                                <Link  href={"/classify"} className="bg-rose-500 px-2 rounded">Classificar</Link>
                        
                            </motion.div>
                        
                        </motion.div>
        
                    }
                </AnimatePresence>
            </div>
        </header>
        }
        </>
    )

}