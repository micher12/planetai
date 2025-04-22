import getConnection from "@/components/getConnection";
import { NextApiRequest, NextApiResponse } from "next";

interface noticia {
    title: string,
    description: string,
    url: string,
    class: string,
    date: string
}

interface noticiaExistente{
    id_noticia: number,
    title_noticia: string,
    description_noticia: string,
    url_noticia: string,
    class_noticia: string,
    date_noticia: string,
}

export default async function savenews(req: NextApiRequest, res: NextApiResponse){

    if(req.method !== "POST")
        return res.status(405).json({erro: "Método inválido!"})

    if(!req.body)
        return res.status(404).json({erro: "Inválido!"})

    const body = req.body;

    if(body.length <= 0)
        return res.status(404).json({erro: "Inválido!"})

    const connection = await getConnection();

    try {
        const noticias: noticia[] = JSON.parse(body)

        const [allNoticias] = await connection.query("SELECT * FROM `noticias`");
        const noticiasExistentes = allNoticias as noticiaExistente[];

        const titlesExisting = new Set(noticiasExistentes.map(n => n.title_noticia));

        const descriptionsExisting = new Set(noticiasExistentes.map(n => n.description_noticia));

        const noticiasFiltradas = noticias.filter(noticia => 
                (noticia.title && noticia.description) &&
                !titlesExisting.has(noticia.title) && 
                !descriptionsExisting.has(noticia.description)
         
        );

        for (const noticiaItem of noticiasFiltradas) {
            await connection.query(
            'INSERT INTO `noticias` VALUES (?, ?, ?, ?, ?, ?)',
            [
                null,
                noticiaItem.title,
                noticiaItem.description,
                noticiaItem.url,
                noticiaItem.class,
                noticiaItem.date,
            ]
            );
        }


        return res.status(200).json({sucesso: "ok"})
        
    } catch (error) {
        console.log(error)
        return res.status(404).json({erro: "Algo deu errado!"})
    }

}