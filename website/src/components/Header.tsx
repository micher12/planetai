"use client";

import { AnimatePresence, motion } from "motion/react";
import Image from "next/image";
import Link from "next/link";
import { use, useEffect, useState, MouseEvent } from "react";


export default function Header() { 

    const [mobile, setMobile] = useState(false);
    const [mobileIsOpen, setMobileIsOpen] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(()=>{

        function resizing(){
            const width = window.innerWidth;
            if(width <= 650){
                setMobile(true);
                mobileIsOpen && openMenu();
                setMobileIsOpen(false);
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
        setMobileIsOpen(!mobileIsOpen)
    }


    function navegation(e: MouseEvent<HTMLAnchorElement>){
        e.preventDefault();
        const el = e.target as HTMLAnchorElement;
        const path = window.location.pathname
        const id = el.getAttribute('href')?.split("/")[1].trim() as string;

        if(id === "" && path === "/"){
            window.scrollTo({top: 0, behavior: "smooth"});
            mobileIsOpen && openMenu();
            return
        }else if(path !== "/"){
            window.location.href = "/";
            return
        }
        
        const element = document.getElementById(id);

        if(element){
            element.scrollIntoView({behavior: "smooth"});
            mobileIsOpen && openMenu();
        }

    }


    return(
        <>
        {!loading &&
            <>
            <header className="w-full fixed top-0 left-0 py-4 z-50">
                <div className="container mytransition expandHeader">
                    <div className="w-full backdrop-blur bg-gradient-to-br from-slate-200/20 to-transparent  border border-slate-100/30 px-3 py-2 rounded-lg shadow-md">
                        <div className={`flex flex-col sm:flex-row mytransition items-center ${!mobile ? "justify-between" : "justify-center"}`}>
                            {mobile ? 
                            <div onClick={openMenu} className="w-fit cursor-pointer text-slate-50 font-bold flex items-center gap-2 text-lg select-none">
                                <Image src={"/planet.png"} width={40} height={40} alt="Logo PlanetAI" /> PlanetAI
                            </div>
                            :
                            <Link href={"/"} className="w-fit text-slate-50 font-bold flex items-center gap-2 text-lg"><Image  src={"/planet.png"} width={30} height={30} alt="Logo PlanetAI" /> PlanetAI</Link>
                            }

                    
                            {mobile ? <></> : 
                            <nav className="flex-1 flex justify-center text-slate-50 font-bold gap-3">
                                <Link onClick={navegation} href={"/"} className="hover:bg-indigo-500 px-2 rounded mytransition">Início</Link>
                                <Link onClick={navegation} href={"/sobre"} className="cursor-pointer hover:bg-indigo-500 px-2 rounded mytransition">Sobre</Link>
                                <Link href={"/results"} className="hover:bg-indigo-500 px-2 rounded mytransition">Histórico</Link>
                            </nav>
                            }
                        
                            {mobile ? <></> :
                            <div className=" flex justify-center text-slate-50 font-bold gap-6 pr-5">
                                <Link  href={"/classify"} className="bg-rose-500 hover:bg-rose-600 mytransition px-2 rounded">Classificar</Link>
                            </div>
                            }

                        <AnimatePresence>
                            {mobileIsOpen &&

                                <motion.div 
                                initial={{height: 0, opacity: 0, filter: "blur(10px)"}}
                                animate={{height: "170px", opacity: 1, filter: "blur(0)"}}
                                transition={{ 
                                    type: "spring",
                                    stiffness: 180,
                                    damping: 24,
                                }}
                                exit={{height: 0, filter: "blur(10px)", opacity: 0}}
                                className="text-white w-full flex items-center justify-center font-bold flex-col gap-3"
                                >

                                    <Link onClick={navegation} href={"/"}>Início</Link>
                                    <Link onClick={navegation} href={"/sobre"} className="cursor-pointer">Sobre</Link>
                                    <Link href={"/results"}>Histórico</Link>
                                    <Link  href={"/classify"} className="bg-rose-500 px-2 rounded">Classificar</Link>
                        
                                </motion.div>
                            }
                        </AnimatePresence>

                        </div>
                    </div>
                </div>
            </header>
            {mobileIsOpen && <div className="popUpOverlay fadeIn-sm"></div>}
            </>
        }
        </>
    )

}