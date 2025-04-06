import { NextApiRequest, NextApiResponse } from "next";

export default async function newsclassify(req: NextApiRequest, res: NextApiResponse){

    if(req.method !== "POST")
        return res.status(405).json({erro: "Método inválido!"})

    const url = "http://127.0.0.1:5000/api/noticias"

    const noticias = await fetch(url, {
        method: "POST"
    }).then(data => data.json());


    return res.status(200).json({sucesso: "ok", noticias})

}