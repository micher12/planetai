"use client";

import { faChevronUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function BackToTop() {

    return (
        <div className="fixed bottom-4 right-4 z-50">
        <button
            className="rounded-full bg-blue-500 p-2 cursor-pointer flex items-center justify-center text-white shadow-lg hover:bg-blue-600"
            onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
        >
           <FontAwesomeIcon icon={faChevronUp} />
        </button>
        </div>
    );

}