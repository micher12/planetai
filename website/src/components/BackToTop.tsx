"use client";

import { faChevronUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useEffect, useState } from "react";

export default function BackToTop() {

    const [active, setActive] = useState(false);

    useEffect(()=>{

        function scroll(){

            const altura = window.scrollY;

            if(altura >= 200){
                setActive(true);
            }else{
                setActive(false);
            }
        }
        scroll()

        window.addEventListener("scroll", scroll);

        return ()=>{
            window.removeEventListener("scroll",scroll);
        }
    },[])

    return(
                
        <>
        {active &&
            <div className="fixed bottom-4 right-4 z-50 fadeIn-sm">
                <button
                    className="rounded-full bg-blue-500 p-2 cursor-pointer flex items-center justify-center text-white shadow-lg hover:bg-blue-600"
                    onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
                >
                    <FontAwesomeIcon icon={faChevronUp} />
                </button>
            </div>
        }
        </>
    
    )

}