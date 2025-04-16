import { NextApiRequest, NextApiResponse } from "next";

export default async function getProtocolo(req: NextApiRequest, res: NextApiResponse) {
    
    if(req.method != "POST")
        return res.status(405).json({erro: "Método Inválido"})

    const response = await fetch("http://127.0.0.1:5000/api/protocolo",{
        method: "POST"
    }).then(res => res.json())
    .then(res => res.relatorio)

    return res.status(200).json(response)

}