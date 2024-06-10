import React, { useEffect, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { liquidacionUsuario } from "../../apis/calls";
import { Table } from "../../components/Table";
import {GiPayMoney} from "react-icons/all.js";

const Liquidaciones = () => {
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
			accessor: "mail_usuario",
			Header: "Email",
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
			accessor: "pendientes",
			Header: "Ventas",
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
					<GiPayMoney title="Ir a Liquidar" size="2em"/>
				</button>
			),
		},
	];

	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["liquidacionesUsuario"],
		queryFn: liquidacionUsuario,
		refetchOnWindowFocus: true,
		onSuccess: (result) => {
			console.log("liquidacionUsuario", result);
		},
	});

	if (isLoading) {
		return <p>Loading ...</p>;
	}

	if (isError) {
		return <p>Error: {error.message}</p>;
	}

	return (
		<div className="bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<header className="px-5 py-4">
				<div className="flex flex-row justify-end">
					<h2 className="font-semibold text-gray-800">
						Todos las liquidaciones pendientes{" "}
						<span className="text-gray-400 font-medium">{data.length}</span>
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
							parentName="Liquidaciones"
						/>
					)}
				</div>
			</div>
		</div>
	);
};

export default Liquidaciones;
