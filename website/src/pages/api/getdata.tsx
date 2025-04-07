import { NextApiRequest, NextApiResponse } from "next";
import getConnection from "@/components/getConnection";

interface noticiaExistente{
    id_noticia: number,
    title_noticia: string,
    description_noticia: string,
    url_noticia: string,
    class_noticia: string,
    date_noticia: string,
}

export default async function getdata(req: NextApiRequest, res: NextApiResponse){

    if(req.method !== 'POST')
        return res.status(405).json({erro: "Método inválido!"})

    const connection = await getConnection();

    try{

        const [last5] = await connection.query(
            'SELECT * FROM noticias WHERE `date_noticia` >= CURDATE() - INTERVAL 5 DAY ORDER BY date_noticia DESC'
        );

        const [allData] = await connection.query(
            'SELECT * FROM noticias ORDER BY date_noticia DESC' 
        );

        const [result] = await connection.query(
            "SELECT " +
            "count(*) as total,"+
            "SUM(CASE WHEN `class_noticia` = 'Positiva' THEN 1 ELSE 0 END) as positiva, " +
            "SUM(CASE WHEN `class_noticia` = 'Negativa' THEN 1 ELSE 0 END) as negativa, " +
            "SUM(CASE WHEN `class_noticia` = 'Irrelevante' THEN 1 ELSE 0 END) as irrelevante " +
            "FROM `noticias`"
        );

        return res.status(200).json({last5, allData, result})

    }catch(erro){
        console.log(erro)
        return res.status(400).json({error: "Erro ao buscar dados"})
    }

}