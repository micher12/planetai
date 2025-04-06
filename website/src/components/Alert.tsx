"use client";

interface alertProps{
    message: string,
    type: "sucesso" | "erro" | null,
}

const Alert: React.FC<alertProps> = ({ message, type}) => {
    if (type === "sucesso") {
        return (
            <div className="alertSucesso fadeIn">
                {message}
            </div>
        );
    }
    if (type === "erro") {
        return (
            <div className="alertErro fadeIn">
                {message}
            </div>
        );
    }

    return null;
};

export default Alert;