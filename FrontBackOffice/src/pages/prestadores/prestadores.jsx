import React from "react";
import { useQuery } from "@tanstack/react-query";
import Modal_splash from "../../components/modal/modal_splash";
import { allPrestadores, PdfCartolaPrestador } from "../../apis/calls";
import { Table } from "../../components/Table.jsx";
import { useNavigate } from "react-router-dom";
import { BsFiletypePdf, ImProfile } from "react-icons/all.js";
import { FormPopup } from "../../components/alerts";
import { toast } from "react-toastify";
import { useRef } from "react";

function Prestadores() {
	const desdeRef = useRef(null);
    const hastaRef = useRef(null);
	const navigate = useNavigate();

	const fields = [
		{
			accessor: "cod_usuario",
			Header: "Cod Usuario",
		},
		{
			accessor: "nombre_usuario",
			Header: "Nombre de Usuario",
		},
		{
			accessor: "rut_usuario",
			Header: "RUT",
		},
		{
			accessor: "desc_comuna",
			Header: "Comuna",
		},
		{
			accessor: "mail_usuario",
			Header: "Email",
		},
		{
			accessor: "cod_revisado",
			Header: "Cod Revisado",
		},
		{
			accessor: "comision",
			Header: "Comision",
			Cell: ({ row }) => (
				<>
					{row.values.comision.toFixed(1)} <span title="19%">+ IVA</span>
				</>
			),
		},
		{
			accessor: "last_login",
			Header: "Última conexión",
		},
		{
			accessor: "fecha_registro",
			Header: "Fecha de Registro",
		},
		{
			width: 300,
			accessor: null,
			Header: "Acciones",
			Cell: ({ row }) => (
				<div className="flex flex-row gap-1 justify-center items-center">
					<button
                        onClick={() => handleDownloadPDF(row.values.cod_usuario)}
                    >
                        <BsFiletypePdf title="Descargar Pdf Cartola" size="1.5em"/>
                    </button>
					<button
					className="relative justify-center text-center"
					onClick={() =>
						navigate(
							`/prestadores/detalle/?codPrestador=${row.values.cod_usuario}`
						)
					}
				>
					<ImProfile title="Ver Perfil" size="1.5em" />
					{row.values.cod_revisado == "N" ? (
						<span className="absolute -top-1 -right-1 h-2 w-2 rounded-full ml-2 bg-red-500">
							{" "}
						</span>
					) : (
						<span className="absolute -top-1 -right-1 h-2 w-2 rounded-full ml-2 bg-green-500"></span>
					)}
				</button>
				</div>
			),
		},
	];

	const handleDownloadPDF = async (codPrestador) => {
        const download = async () => {
			const {desde, hasta} = await FormPopup(desdeRef, hastaRef)
			console.log("FECHASSSS", desde, hasta);
			if (!desde && !hasta){
				toast.error("Debe elegir un rango de fecha",{
					pauseOnFocusLoss: false,
					hideProgressBar: true,
					autoClose: 2000
				})
				return
			}
			let cuerpo = {}
			cuerpo.cod_prestador = codPrestador
			if (desde){
				cuerpo.desde = desde
			}
			if (hasta){
				cuerpo.hasta = hasta
			}
            const fileUrl = await PdfCartolaPrestador(cuerpo)
			if (!fileUrl) {
				toast.error("No posee ventas aún.",{
					pauseOnFocusLoss: false,
					hideProgressBar: true,
					autoClose: 2000
				})
				return
			}
			console.log("FILEURL", fileUrl);
            const link = document.createElement("a");
            link.href = fileUrl;
            link.download = `cartolaPrestador_${codPrestador}.pdf`;

            link.click();
			toast.info("Descargando Cartola PDF...",{
				pauseOnFocusLoss: false,
				hideProgressBar: true,
				autoClose: 2000
			})
		}
		
		await download()
		
    }

	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["allPrestadores"],
		queryFn: allPrestadores,
		refetchOnWindowFocus: true,
		onSuccess: (result) => {
			console.log(result);
		},
	});

	if (isLoading) {
		return <Modal_splash estado={true} />;
	}
	if (isError) {
		return <p>Error: {error.message}</p>;
	}

	return (
		<div className="flex flex-col h-full w-full bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<div className="flex flex-row justify-end">
				<h2 className="font-semibold text-gray-800 mr-5 mt-2">
					Todos los prestadores :{" "}
					<span className="text-gray-400 font-medium">{data.length}</span>
				</h2>
			</div>

			<div>
				<div className="overflow-y-auto">
					{data.length > 0 && (
						<Table
							data={data}
							COLUMNS={fields}
							hiddenColumns={[
								// "cod_usuario"
								"cod_revisado",
							]}
							parentName="Prestadores"
						/>
					)}
				</div>
			</div>
		</div>
	);
}

export default Prestadores;
