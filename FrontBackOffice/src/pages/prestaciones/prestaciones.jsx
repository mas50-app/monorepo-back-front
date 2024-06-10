import React, { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { allPrestaciones } from "../../apis/calls";
import { Table } from "../../components/Table";
import {CgFileDocument} from "react-icons/all.js";

function Prestaciones() {
	const navigate = useNavigate();

	const fields = [
		{
			accessor: "cod_usuario",
			Header: "Cod Usuario",

		},
		{
			accessor: "cod_servicio",
			Header: "Cod Prestación",
		},
		{
			accessor: "nombre_usuario",
			Header: "Nombre de Usuario",
		},
		{
			accessor: "nom_servicio",
			Header: "Nombre del negocio",
		},
		{
			accessor: "comunas",
			Header: "Alcance",
			Cell: ({row}) => (
				row.values.comunas.length > 0 ?
					<>
						{row.values.comunas.length} {row.values.comunas.length > 1 ? "comunas": "comuna"}
					</>
					:
					<>
						Nacional
					</>
			)
		},
		{
			accessor: "categorias",
			Header: "Categoria",
			Cell: ({row}) => (
				<>{row.values.categorias[0].desc_categoria}</>
			)
		},
		{
			accessor: "dias_antelacion",
			Header: "Dias de antelacion",
		},
		{
            accessor: "cod_domicilio",
            Header: "Entrega",
            Cell: ({row}) => (
                <>{row.values.cod_domicilio === "S"? "Delivery": "En Local"}</>
            )
        },
		{
			accessor: null,
			Header: "Acciones",
			Cell: ({row}) => (
				<div className="btn-group">
					<button onClick={() => navigate(`/prestaciones/detalle/?codPrestacion=${row.values.cod_servicio}`)}>
						<CgFileDocument title="Ver Detalle" size="2em"/>
					</button>
				</div>
			)
		}
	];

	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["allPrestaciones"],
		queryFn: allPrestaciones,
		refetchOnWindowFocus: false,
		onSuccess: (result) => {
			console.log("allPrestaciones", result);
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
				<div className="flex flex-row justify-between">
					<h2 className="font-semibold text-gray-800">
						Todos las prestaciones{" "}
						<span className="text-gray-400 font-medium">{data.length}</span>
					</h2>
				</div>
			</header>{" "}
			<div className="overflow-x-auto">
				{data.length > 0 && (
					<Table
						data={data}
						COLUMNS={fields}
						hiddenColumns={["cod_usuario"]}
						parentName="Prestaciones"
					/>
				)}
			</div>
		</div>
	);
}

export default Prestaciones;
