import React, {useEffect, useState} from "react";
import {getDocumentos, getMesesDocs, getPdfDocumento} from "../../apis/calls.js";
import {Table} from "../../components/Table.jsx";
import {BsFiletypePdf, CgFileDocument, FaRegFilePdf, FcSerialTasks, RiRefund2Line, TbReceiptRefund} from "react-icons/all.js";
import {useNavigate} from "react-router-dom";
import { toast } from "react-toastify";


const Documentos = () => {

    const [meses, setMeses] = useState([]);
    const [documentos, setDocumentos] = useState([]);

    const [mesActual, setMesActual] = useState(null);

    const navigate = useNavigate()

    useEffect(() => {
        (async () => {
            if (mesActual == null) await handleGetMeses()
            if (mesActual != null) await handleGetDocs()
        })()
    }, [mesActual]);

    const handleGetMeses = async () => {
        const mesResp = await getMesesDocs()
        console.log("Meses", mesResp)
        if (mesResp){
            setMeses(mesResp)
            setMesActual(mesResp[0].mes)
        }
    }

    const handleGetDocs = async () => {
        const docsResp = await getDocumentos({mes:mesActual})
        if (docsResp){
            console.log(docsResp)
            setDocumentos(docsResp)
        }
    }

    const handleDownloadPDF = async (codCodumento) => {
        toast.info("Descargando archivo PDF...",{
            pauseOnFocusLoss: false,
            hideProgressBar: true,
            autoClose: 2000
        })
        const download = async () => {
            const fileUrl = await getPdfDocumento({cod_documento: codCodumento})
            const link = document.createElement("a");
            link.href = fileUrl;
            link.download = `documento_${codCodumento}.pdf`;

            link.click();
        }
        await download()
    }

    const COLUMNS = [
        {
            accessor: "cod_documento",
            Header: "Cod Documento"
        },
        {
            accessor: "cod_comprador",
            Header: "Cod Comprador"
        },
        {
            accessor: "nombre_comprador",
            Header: "Comprador"
        },
        {
            accessor: "cod_vendedor",
            Header: "Cod Vendedor"
        },
        {
            accessor: "nombre_vendedor",
            Header: "Vendedor"
        },
        {
            accessor: "comision",
            Header: "% Comisión"
        },
        {
            accessor: "monto_documento",
            Header: "Monto Documento"
        },
        
        {
            accessor: "monto_venta",
            Header: "Monto Venta"
        },
        {
            accessor: "monto_comision_bruto",
            Header: "Monto Comisión"
        },
        {
            accessor: "fecha_documento",
            Header: "Fecha"
        },
        {
            accessor: "cod_domicilio",
            Header: "Entrega",
            Cell: ({row}) => (
                <>{row.values.cod_domicilio === "S"? "Delivery": "En Local"}</>
            )
        },
        {
            accessor: "devolucion",
            Header: "Devolución"
        },
        {
            accessor: "desc_estado_documento",
            Header: "Estado"
        },
        {
            accessor: null,
            Header: "Acciones",
            Cell: ({row}) => (
                <div className="flex flex-row gap-1 justify-center items-center">
                    <button
                        onClick={() => handleDownloadPDF(row.values.cod_documento)}
                    >
                        <BsFiletypePdf title="Descargar PDF" size="2em"/>
                    </button>
                    <button onClick={() => navigate(`/documentos/detalle/?codDocumento=${row.values.cod_documento}`)}>
                        <CgFileDocument title="Ver Detalle" size="2em"/>
                    </button>
                    {row.values.devolucion === "N" ?
                        <button onClick={() => navigate(`/financiero/devoluciones/crear/?codDocumento=${row.values.cod_documento}`)}>
                            <RiRefund2Line title="Crear Devolución" size="2em"/>
                        </button>:
                        <TbReceiptRefund title="Posee devolución" size="2em"/>
                    }
                </div>

            )
        },
    ]


    return (
        <div className="flex flex-col h-full w-full bg-white shadow-lg rounded-sm border border-gray-200 m-2">
            <div className="flex justify-between p-2 mb-2">
                <select
                    className="rounded-md bg-gray-200 lg:w-[10%] sm:w-[50%] h-10 pl-2 ml-6"
                    onChange={(e) => {
                        console.log("mes seleccionado", e.target.value);
                        setMesActual(e.target.value)
                    }
                    }
                >
                    {
                        meses.length > 0 && (
                            meses.map((mes, index) => (
                                <option value={mes.mes} key={index}>
                                    {mes.desc_mes}
                                </option>
                            ))

                        )
                    }
                </select>
                <label className="m-3">
                    Documentos : {documentos.length > 0 ? documentos.length: 0}
                </label>
            </div>
            {
                documentos.length > 0 &&
                <Table data={documentos} COLUMNS={COLUMNS} hiddenColumns={[
                    "cod_vendedor",
                    "cod_comprador",
                    "devolucion"
                ]} parentName="Documentos"/>
            }
        </div>

    )
}

export default Documentos