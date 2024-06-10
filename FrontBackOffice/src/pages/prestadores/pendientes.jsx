import React from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { allByCodPrestaciones, pendientesPrestadores } from "../../apis/calls";
import { Table } from "../../components/Table";
import { useNavigate } from "react-router-dom";
import {ImProfile} from "react-icons/all.js";

function PrestadoresPendientes() {
	const navigate = useNavigate();
	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["pendientesPrestadores"],
		queryFn: pendientesPrestadores,
		refetchOnWindowFocus: false,
		onSuccess: (result) => {
			console.log(result);
		},
	});

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
			accessor: "apellido1_usuario",
			Header: "Apellido",
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
			width: 300,
			accessor: null,
			Header: "Acciones",
			Cell: ({ row }) => (
				<button
					onClick={() =>
						navigate(
							`/prestadores/detalle/?codPrestador=${row.values.cod_usuario}`
						)
					}
				>
					<ImProfile title="Ver Perfil" size="2em"/>
				</button>
			),
		},
	];

	if (isLoading) {
		return <p>Loading...</p>;
	}

	if (isError) {
		return <p>Error: {error.message}</p>;
	}

	return (
		<div className=" flex flex-col w-full h-full bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<div className="flex flex-row justify-end m-5">
				<h2 className="font-semibold text-gray-800">
					Prestadores pendientes de revisión{" "}
					<span className="text-gray-400 font-medium">{data.length}</span>
				</h2>
			</div>

			<div className="overflow-y-auto">
				{data.length > 0 && (
					<Table
						data={data}
						COLUMNS={fields}
						hiddenColumns={[
							// "cod_usuario"
						]}
						parentName="Prestadores"
					/>
				)}
			</div>
		</div>
	);
}

export default PrestadoresPendientes;
