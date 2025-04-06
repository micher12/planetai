"use client"

export default function Skeleton({type}: {type: string}){

    if(type === "news"){
        return(
            <div className="flex w-full flex-wrap justify-start gap-8 mt-10 fadeIn">
                {
                    [...Array(6)].map((_, index)=>(
                        <div key={index} className="animate-pulse singleItem mytransition flex flex-col gap-5 p-5 bg-slate-800 rounded-xl text-white border-slate-700 border shadow-md">
                            <h2 className="w-full bg-slate-600 h-10 rounded-lg"></h2>
                            <h2 className="w-full bg-slate-600 h-24 rounded-lg"></h2>
                            <span className="w-20 h-6 bg-slate-600 rounded-lg"></span>
                        </div>
                    ))
                }
            </div>
        )
    }

}