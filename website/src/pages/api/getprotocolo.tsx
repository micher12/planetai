import { NextApiRequest, NextApiResponse } from "next";

export default async function getProtocolo(req: NextApiRequest, res: NextApiResponse) {
    
    if(req.method != "POST")
        return res.status(405).json({erro: "Método Inválido"})

    const host_url = process.env.REQUEST_URL as string;

    const response = await fetch(`${host_url}/api/protocolo`,{
        method: "POST",
        headers:{
            "Authorization": `Bearer ${process.env.MY_API_KEY as string}`,
        }
    }).then(res => res.json())

    return res.status(200).json(response)

}