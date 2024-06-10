import { useMutation, useQuery } from "@tanstack/react-query";
import React, { useEffect, useState } from "react";
import { devolucionCancelar, devolucionesAll } from "../../apis/calls";
import { Table } from "../../components/Table";
import { useNavigate } from "react-router-dom";
import {CgFileDocument} from "react-icons/all.js";
import {formatFloat} from "../../utils/formatMoney.js";

const Devoluciones = () => {
	const navigate = useNavigate();

	const [devoluciones, setDevoluciones] = useState([]);

	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["devolucionesAll"],
		queryFn: devolucionesAll,
		refetchOnWindowFocus: false,
		onSuccess: (result) => {
			console.log("resultado", result);
			setDevoluciones(result)
		},
	});

	const cancelarDevolucionByCod = useMutation({
		mutationFn: devolucionCancelar,
		onMutate: (variables) => {
			console.log("variables", variables);
		},
		onSuccess: (result) => {
			console.log("resultado", result);
		},
		onError: (error) => {
			console.log("error", error);
		},
	});

	const fields = [
		{
			accessor: "cod_documento",
			Header: "Cod Documento",
		},
		{
			accessor: "comprador.cod_usuario",
			Header: "Comprador",
		},
		{
			accessor: "comprador.nombre_usuario",
			Header: "Comprador",
		},
		{
			accessor: "vendedor.cod_usuario",
			Header: "Vendedor",
		},
		{
			accessor: "vendedor.nombre_usuario",
			Header: "Vendedor",
			Cell: ({row}) => (
				<a href={`/prestadores/detalle/?codPrestador=${row.values['vendedor.cod_usuario']}`}>
					{row.values['vendedor.nombre_usuario']}
				</a>
			)
		},
		{
			accessor: "fecha_documento",
			Header: "Fecha Documento",
		},
		{
			accessor: "monto_documento",
			Header: "Monto Documento",
			Cell: ({row}) => (
				<>{formatFloat(row.values.monto_documento)}</>
			)
		},
		{
			width: 300,
			accessor: null,
			Header: "Acciones",
			Cell: ({ row }) => (
				<button
					onClick={() => navigate(`/financiero/devoluciones/crear/?codDocumento=${row.values.cod_documento}`)}
				>
					<CgFileDocument title="Ver Detalle" size="2em"/>
				</button>
			)
		},
	];

	if (isLoading) {
		return <p>Loading...</p>;
	}

	if (isError) {
		return <p>Error: {error.message}</p>;
	}

	return (
		<div className="bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<header className="px-5 py-4">
				<div className="flex flex-row justify-between">
					<h2 className="font-semibold text-gray-800">
						Devoluciones
						<span className="text-gray-400 font-medium ml-5">
							{devoluciones.length}
						</span>
					</h2>
				</div>
			</header>
			<div>
				<div className="overflow-x-auto">
					{devoluciones.length > 0 && (
						<Table
							data={devoluciones}
							COLUMNS={fields}
							hiddenColumns={[
								// "cod_documento"
								"comprador.cod_usuario",
								"vendedor.cod_usuario"
							]}
							parentName="Prestadores"
						/>
					)}
				</div>
			</div>
		</div>
	);
};

export default Devoluciones;
