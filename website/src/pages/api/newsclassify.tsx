import { NextApiRequest, NextApiResponse } from "next";

export default async function newsclassify(req: NextApiRequest, res: NextApiResponse){

    if(req.method !== "POST")
        return res.status(405).json({erro: "Método inválido!"})

    const host_url = process.env.REQUEST_URL as string;

    const url = `${host_url}/api/noticias`

    const noticias = await fetch(url, {
        method: "POST",
        headers:{
            "Authorization": `Bearer ${process.env.MY_API_KEY as string}`,
        }
    }).then(data => data.json());


    return res.status(200).json({sucesso: "ok", noticias})

}