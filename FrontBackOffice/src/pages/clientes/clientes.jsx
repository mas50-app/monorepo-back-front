import React from "react";
import { useQuery } from "@tanstack/react-query";
import { BiError } from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import { allClientes } from "../../apis/calls";
import { Table } from "../../components/Table";
import { ImProfile } from "react-icons/im";

function Clientes() {
	const navigate = useNavigate();

	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["allClientes"],
		queryFn: allClientes,
		refetchOnWindowFocus: true,
		onSuccess: (result) => {
			console.log("allClientes", result);
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
			accessor: "last_login",
			Header: "Último Login",
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
				<button
					className="justify-center text-center"
					onClick={() =>
						navigate(`/clientes/detalle?codCliente=${row.values.cod_usuario}`)
					}
				>
					<ImProfile title="Ver Perfil" size="2em" />
				</button>
			),
		},
	];

	if (isLoading) {
		return <p>Loading...</p>;
	}
	if (isError) {
		return (
			<p>
				<BiError /> Error: {error.message}
			</p>
		);
	}

	return (
		<div className="bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<header className="px-5 py-4">
				<div className="flex flex-row justify-end">
					<h2 className="font-semibold text-gray-800">
						Todos los clientes
						<span className="text-gray-400 font-medium">
							{" " + data.length}
						</span>
					</h2>
				</div>
			</header>
			<div>
				<div className="overflow-x-auto">
					{data.length > 0 && (
						<Table
							data={data}
							COLUMNS={fields}
							hiddenColumns={["cod_usuario"]}
							parentName="Clientes"
						/>
					)}
				</div>
			</div>
		</div>
	);
}

export default Clientes;
