import mysql from "mysql2/promise"

export default async function getConnection(){
    const connection = await mysql.createConnection({
        host: process.env.DB_LOCALHOST,
        user: process.env.DB_USER,
        database: 'planetai',
    });

    return connection;
}