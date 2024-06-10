import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useSearchParams } from "react-router-dom";

import { useMutation, useQuery } from "@tanstack/react-query";
import {devolucionByCod, devolucionCrear, getCambiosEstado} from "../../apis/calls";
import { BsArrowReturnRight } from "react-icons/bs";
import {BiLinkExternal} from "react-icons/all.js";
import {formatFloat} from "../../utils/formatMoney.js";

export const CrearDevolucion = () => {
	const navigate = useNavigate();
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const codDocumento = queryParams.get("codDocumento");
	const [mensaje, setMensaje] = useState("");
	const [devManual, setDevManual] = useState(false);

	const [data, setData] = useState(null);
	const [dataMap, setDataMap] = useState(null);

	useEffect(() => {
		if (codDocumento != null) {
			makeDataByCod.mutate(codDocumento);
			makeDataMapa.mutate(codDocumento)
		}
	}, [mensaje]);

	const makeDataByCod = useMutation({
		mutationFn: devolucionByCod,
		onSuccess: (result) => {
			console.log("prestador", result);
			setData(result);
		},
	});

	const crearDevolucion = useMutation({
		mutationFn: devolucionCrear,
		onSuccess: (result) => {
			navigate("/financiero/devoluciones");
		},
	});

	const makeDataMapa = useMutation({
		mutationFn: getCambiosEstado,
		onSuccess: (result) => {
			console.log("detalleDoc", result);
			setDataMap(result);
		},
	});

	return (
		data != null && (
			<div className="flex flex-row justify-center items-start rounded-md w-full  h-full overflow-hidden">
				<div
					className={`${
						data.detalles.length > 7 ? "w-1/3" : "w-1/2"
					} flex flex-col h-full overflow-y-scroll`}
				>
					<div className="px-4  w-full">
						<div className="flex flex-row justify-between mb-2 border rounded-md p-2 w-full">
							<div className="font-bold text-2xl text-center">Reporte</div>
							<div className="text-gray-500 text-center">
								{/*Documento {data.cod_documento}*/}
								Estado Documento <strong>{data.desc_estado_documento}</strong>
							</div>
						</div>
						<div className="grid grid-cols-2 gap-2 bg-white rounded-md p-2 border w-full">
							<div>
								<div className="font-bold mb-2">Descripción del documento</div>
								<div className="mb-4">{data.desc_documento}</div>

								<div className="font-bold mb-2">Monto del documento</div>
								<div className="mb-4">{data.monto_documento}</div>
								<div className="font-bold mb-2">Fecha del documento</div>
								<div className="mb-4">{data.fecha_documento}</div>
							</div>
							<div>
								<div className="font-bold mb-2">Flow Order</div>
								<div className="mb-4">{data.flow_order}</div>
								<div className="font-bold mb-2">En local</div>
								<div className="mb-4">
									{data.cod_retiro == "S" ? "SI" : "NO"}
								</div>
								<div className="font-bold mb-2">Delivery</div>
								<div className="mb-4">
									{data.cod_domicilio == "S" ? "SI" : "NO"}
								</div>
							</div>
						</div>
						<div className="flex flex-col mt-2 justify-between space-y-2">
							<div className="flex flex-col justify-start items-start bg-white  border rounded-md p-2">
								<div className="font-bold mb-2 flex flex-row w-full justify-around items-center">
									Información del vendedor{" "}
									<a
										href={`/prestadores/detalle/?codPrestador=${data.vendedor.cod_usuario}`}
									>
										<BiLinkExternal />
									</a>
								</div>
								<div className="mb-4">
									Nombre: {data.vendedor.nombre_usuario}{" "}
									{data.vendedor.apellido1_usuario}{" "}
									{data.vendedor.apellido2_usuario}
								</div>
								<div className="mb-4">Rut: {data.vendedor.rut_usuario}</div>
								<div className="mb-4">Mail: {data.vendedor.mail_usuario}</div>
							</div>
							<div className="flex flex-col justify-start items-start bg-white  border rounded-md p-2">
								<div className="font-bold mb-2">Información del comprador</div>
								<div className="mb-4">
									Nombre: {data.comprador.nombre_usuario}{" "}
									{data.comprador.apellido1_usuario}{" "}
									{data.comprador.apellido2_usuario}
								</div>
								<div className="mb-4">Rut: {data.comprador.rut_usuario}</div>
								<div className="mb-4">Mail: {data.comprador.mail_usuario}</div>
							</div>
							<div className="flex flex-col justify-start items-start bg-white  border rounded-md p-2">
								<div className="font-bold mb-2 flex flex-row w-full justify-around items-center">
									Historial de Estados{" "}
								</div>
								<div className="flex flex-row justify-center space-x-1">
									{dataMap?.map((estado, index) => (
										<div
											key={index}
											className="flex flex-col bg-gray-100 border rounded-lg p-4"
										>
											<h3 className="text-lg font-bold mb-2">
												{estado.desc_estado_documento}
											</h3>
											<p className="text-gray-600">{estado.fecha_cambio_estado}</p>
											{index !== 0 && <BsArrowReturnRight className="mt-2" />}
										</div>
									))}
								</div>{" "}
							</div>
						</div>
					</div>
				</div>

				<div
					className={`flex flex-col h-full ${
						data.detalles.length > 7 ? "w-1/3" : "w-1/2"
					} bg-rose-100 justify-start items-center rounded-md px-2 mx-2 `}
				>
					<div className="flex flex-col justify-start items-start my-4 w-full">
						<div className="font-bold text-2xl mx-3">Detalle de compra</div>
						<div className="flex flex-row justify-between items-center w-full">
							<div className="flex flex-row">
								<div className="font-bold mx-3">Nombre de negocio</div>
								<div className="">{data.detalles[0].nom_servicio}</div>
							</div>
							<div className="flex flex-row">
								<div className="font-bold mx-3">Fecha Agenda</div>
								<div className="mx-3">{data.detalles[0].fecha_agenda}</div>
							</div>
						</div>
					</div>

					<div
						className={`flex flex-col items-center justify-start pt-2 w-full h-full px-2 ${
							data.detalles.length > 7 ? "mb-4 overflow-y-scroll" : "p-1"
						} gap-1 `}
					>
						{data.detalles.map((item, index) => {
							return (
								<div
									key={index}
									className="flex flex-row justify-between items-center  bg-white rounded-md  w-full relative"
								>
									<span className="inline-flex justify-center items-center absolute -top-1 -left-1 h-7 w-7 rounded-full ml-2 bg-red-500 text-white shadow-md">
										{index + 1}
									</span>
									<div className="flex flex-col w-full py-2">
										<div className="flex flex-row justify-start items-start pl-10 gap-1">
											<div className="font-bold mx-3">Item</div>
											<div className="">{item.desc_item_servicio}</div>
										</div>
										<div className="flex flex-row justify-center items-start">
											<div className="flex flex-col w-full pl-3 justify-center items-start">
												<div className="font-bold">Cantidad</div>
												<div className="">
													{item.cantidad} x {item.desc_unidad}
												</div>
											</div>
											<div className="flex flex-col w-full pl-3 justify-center items-start">
												<div className="font-bold">Valor unidad</div>
												<div className="">{formatFloat(item.valor_unidad)}</div>
											</div>
											<div className="flex flex-col w-full pl-3 justify-center items-start">
												<div className="font-bold">Total</div>
												<div className="">{formatFloat(item.subtotal)}</div>
											</div>
										</div>
									</div>
								</div>
							);
						})}
					</div>
					{data.detalles.length <= 7 && (
						<div className="flex flex-col justify-center items-center bg-rose-100 w-full rounded-md px-2 mx-2">
							<div className="w-full mb-5 ">
								<div className="flex flex-row justify-between items-center text-center">
									<p className="font-bold text-2xl my-3">Comentario de la devolución</p>
									<div className="flex flex-row gap-2">
										<input id="manual" type="checkbox" checked={devManual} onChange={() => setDevManual(!devManual)}/>
										<label className="select-none" htmlFor="manual">Devolución Manual ?</label>
									</div>
								</div>
								<div className="my-1 w-full">
									<textarea
										rows={4}
										name="comment"
										id="comment"
										className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full h-full sm:text-sm border-gray-300 rounded-md max-h-32 p-3"
										defaultValue={""}
										onChange={(e) => setMensaje(e.target.value)}
									/>
								</div>
							</div>
							<div className="flex flex-row space-x-2 justify-center mb-5">
								<button
									onClick={() => navigate("/prestadores")}
									type="button"
									className="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
								>
									Cancelar
								</button>
								{mensaje != "" && (
									<button
										onClick={() =>
											crearDevolucion.mutate({
												desc_devolucion: mensaje,
												cod_documento: data.cod_documento,
												monto_devolucion: data.monto_documento,
												cod_manual: devManual === false ? "N": "S",
											})
										}
										type="button"
										className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
									>
										Crear
									</button>
								)}
							</div>
						</div>
					)}
				</div>

				{data.detalles.length > 7 && (
					<div className="h-screen w-1/3 flex flex-col justify-center items-center">
						<div className="flex flex-col justify-center items-center bg-rose-100 w-full rounded-md px-2 mx-2">
							<div className="w-full mb-5 ">
								<div className="font-bold text-2xl my-3">
									Comentario de la devolución
								</div>
								<div className="my-1 w-full">
									<textarea
										rows={4}
										name="comment"
										id="comment"
										className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full h-full sm:text-sm border-gray-300 rounded-md max-h-32 p-3"
										defaultValue={""}
										onChange={(e) => setMensaje(e.target.value)}
									/>
								</div>
							</div>
							<div className="flex flex-row space-x-2 justify-center mb-5">
								<button
									onClick={() => navigate("/prestadores")}
									type="button"
									className="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
								>
									Cancelar
								</button>
								{mensaje != "" && (
									<button
										onClick={() =>
											crearDevolucion.mutate({
												desc_devolucion: mensaje,
												cod_documento: data.cod_documento,
												monto_devolucion: data.monto_documento,
												cod_manual: "N",
											})
										}
										type="button"
										className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
									>
										Crear
									</button>
								)}
							</div>
						</div>
					</div>
				)}
			</div>
		)
	);
};
