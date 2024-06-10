import React, { useEffect, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { PdfLiquidacion, liquidacionAll } from "../../apis/calls";
import { Table } from "../../components/Table";
import { BsFiletypePdf } from "react-icons/bs";
import { toast } from "react-toastify";

const LiquidacionesPagadas = () => {
	const navigate = useNavigate();

	const fields = [
		{
			accessor: "cod_liquidacion",
			Header: "Cod liquidacion",
		},
		{
			accessor: "nombre_usuario",
			Header: "Nombre de Usuario",
		},
		{
			accessor: "apellido1_usuario",
			Header: "Apellido de Usuario",
		},
		{
			accessor: "rut_usuario",
			Header: "RUT",
		},
		{
			accessor: "mail_usuario",
			Header: "Email",
		},
		{
			accessor: "monto_venta",
			Header: "Monto de venta",
		},
		{
			accessor: "comision",
			Header: "Monto comisión",
		},
		{
			accessor: "monto_liquidacion",
			Header: "Monto liquidación",
		},
		{
			accessor: "",
			Header: "Acciones",
			Cell: ({row}) => (
				<button
					onClick={() => handleDownloadPDF(row.values.cod_liquidacion)}
				>
					<BsFiletypePdf title="Descargar PDF" size="2em"/>
				</button>
			)
		},
	];

	const handleDownloadPDF = async (codLiquidacion) => {
        const download = async () => {
            const fileUrl = await PdfLiquidacion({cod_liquidacion: codLiquidacion})
            const link = document.createElement("a");
            link.href = fileUrl;
            link.download = `liquidacion_${codLiquidacion}.pdf`;

            link.click();
			toast.info("Descargando Liquidación PDF...",{
				pauseOnFocusLoss: false,
				hideProgressBar: true,
				autoClose: 2000
			})
		}
		await download()
		
    }

	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["liquidacionAll"],
		queryFn: liquidacionAll,
		refetchOnWindowFocus: true,
		onSuccess: (result) => {
			console.log("liquidacionAll", result);
		},
		onError: (error) => {
			console.log(error);
		},
	});

	if (isLoading) {
		return <p>Loading...</p>;
	}

	if (isError) {
		return <p>Error: {error.message}</p>;
	}

	return (
		<div className="bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<header className="px-5 py-4">
				<div className="flex flex-row justify-end">
					<h2 className="font-semibold text-gray-800">
						Historico de pagos
						<span className="text-gray-400 font-medium ml-5">
							{data.liquidaciones.length}
						</span>
					</h2>
					{/* Barra de busqueda */}
				</div>
			</header>
			<div>
				<div className="overflow-x-auto">
					{data.liquidaciones.length > 0 && (
						<Table
							data={data.liquidaciones}
							COLUMNS={fields}
							hiddenColumns={["cod_liquidacion"]}
							parentName="HistoricoPagos"
						/>
					)}
				</div>
			</div>
		</div>
	);
};

export default LiquidacionesPagadas;
