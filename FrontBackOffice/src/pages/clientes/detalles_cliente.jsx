import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
	getUsuarioByCod,
	setActivoUsuario,
	setPausadoUsuario,
} from "../../apis/calls";
import { useMutation } from "@tanstack/react-query";
const API_IMAGEN = import.meta.env.VITE_IMAGES_API;

const DetallesCliente = () => {
	const navigate = useNavigate();
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const codCliente = queryParams.get("codCliente");
	const [data, setData] = useState(null);
	const [refresh, setrefresh] = useState(false);

	useEffect(() => {
		if (codCliente != null) {
			getClienteDetail.mutate(codCliente);
		}
	}, [refresh]);

	const getClienteDetail = useMutation({
		mutationFn: getUsuarioByCod,
		onSuccess: (result) => {
			console.log("Result", result);
			setData(result);
		},
	});

	const setActivo = useMutation({
		mutationFn: setActivoUsuario,
		onSuccess: (result) => {
			setrefresh((e) => !e);
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const setPausado = useMutation({
		mutationFn: setPausadoUsuario,
		onSuccess: (result) => {
			setrefresh((e) => !e);
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	return (
		<div className="flex flex-col w-full h-full bg-white">
			{data != null && (
				<div className="flex flex-row bg-white p-2  w-full h-full overflow-y-auto gap-2">
					<div className="flex flex-col w-full h-full">
						<div className="flex flex-row w-full rounded-md">
							<div className="flex flex-col  justify-between w-3/5 p-2">
								<h2 className="text-lg font-extrabold">Ficha de Cliente</h2>
								<h3 className="text-lg font-medium mb-5">
									Información del Cliente
								</h3>
								<div className="flex flex-col w-full pr-2  mr-2 ">
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Nombre:
										<p className="ml-3 font-bold ">{data.nombre_usuario}</p>
									</label>

									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										RUT:
										<p className="ml-3 font-bold">{data.rut_usuario}</p>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Email:
										<p className="ml-3 font-bold">{data.mail_usuario}</p>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Comuna:
										<p className="ml-3 font-bold">{data.desc_comuna}</p>
									</label>
								</div>
							</div>
							{data.path_imagen != null && (
								<div className="inline-flex justify-center items-center border rounded-md w-1/2">
									<img
										src={`${API_IMAGEN}${data.path_imagen}`}
										alt=""
										className=" max-h-44 rounded-md"
									></img>
								</div>
							)}
						</div>

						<div className="flex space-x-2 justify-center items-center mt-4">
							<button
								onClick={() => navigate("/clientes")}
								type="button"
								className="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
							>
								Regresar
							</button>
							<button
								onClick={() =>
									setActivo.mutate({
										cod_usuario: data.cod_usuario,
										enum_str: data.cod_activo == "S" ? "N" : "S",
									})
								}
								type="button"
								className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
							>
								{data.cod_activo === "S" ? "Inactivar" : "Activar"}
							</button>
							{/*<button*/}
							{/*	onClick={() =>*/}
							{/*		setPausado.mutate({*/}
							{/*			cod_usuario: data.cod_usuario,*/}
							{/*			enum_str: data.cod_pausado == "S" ? "N" : "S",*/}
							{/*		})*/}
							{/*	}*/}
							{/*	type="button"*/}
							{/*	className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"*/}
							{/*>*/}
							{/*	{data.cod_pausado === "S" ? "Reanudar" : "Pausar"}*/}
							{/*</button>*/}
						</div>
					</div>
				</div>
			)}
		</div>
	);
};

export default DetallesCliente;
