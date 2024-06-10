import React, { useEffect, useState } from "react";
import { useLocation, useNavigate, useSearchParams } from "react-router-dom";

import { useMutation } from "@tanstack/react-query";
import {
	devolByCod,
	getCambiosEstado,
	getDetalleDoc,
} from "../../apis/calls";
import { BsArrowReturnRight } from "react-icons/bs";
import { BiLinkExternal } from "react-icons/all.js";
import {formatFloat} from "../../utils/formatMoney.js";

export const DetalleDocumento = () => {
	const navigate = useNavigate();
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const codDocumento = queryParams.get("codDocumento");
	const [devolucion, setDevolucion] = useState(null);

	const [data, setData] = useState(null);
	const [dataMap, setDataMap] = useState(null);

	useEffect(() => {
		if (codDocumento != null) {
			makeDataByCod.mutate(codDocumento);
			makeDataMapa.mutate(codDocumento);
			makeDataDevol.mutate(codDocumento)
		}
	}, []);

	const makeDataByCod = useMutation({
		mutationFn: getDetalleDoc,
		onSuccess: (result) => {
			console.log("detalleDoc", result);
			setData(result);
		},
	});

	const makeDataDevol = useMutation({
		mutationFn: devolByCod,
		onSuccess: (result) => {
			console.log("devoluciones", result);
			setDevolucion(result);
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
			<div className="flex flex-row justify-center items-start rounded-md w-full h-full overflow-hidden">
				<div className={`w-1/2 flex flex-col h-full overflow-y-scroll`}>
					<div className="px-2  w-full flex flex-col">
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
						<div className="flex flex-col mt-2 justify-between space-y-2 w-full">
							<div className="flex flex-col justify-start items-start bg-white  border rounded-md p-2">
								<div className="font-bold mb-2 flex flex-row w-full justify-around items-center">
									Información del vendedor{" "}
									<a
										href={`/prestadores/detalle/?codPrestador=${data.vendedor.cod_usuario}`}
									>
										<BiLinkExternal title="Ver Perfil" />
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
							<div className="flex flex-col bg-white border rounded-md p-2 w-full">
								<p className="font-bold mb-2 w-full text-center">
									Historial de Estados{" "}
								</p>
								<div className="flex flex-row w-full space-x-1 overflow-x-auto">
									{dataMap?.map((estado, index) => (
										<div
											key={index}
											className="flex flex-col w-full bg-gray-100 border rounded-lg py-3 px-2 relative"
										>
											<h3 className="card-width text-md font-bold mb-1 text-center inline-flex items-center justify-center">
												{estado.desc_estado_documento}
											</h3>
											<div className=" flex flex-row  justify-between text-sm text-gray-600 space-x-1 ">
												<p>Hora:</p><p>{estado.fecha_cambio_estado.split(" ")[0]}</p>
											</div>
											<div className="flex flex-row  justify-between text-sm text-gray-600 space-x-1 ">
												<p>Fecha:</p><p>{estado.fecha_cambio_estado.split(" ")[1]}</p>
											</div>
											{index !== 0 && <BsArrowReturnRight className="mt-2 absolute left-0 transform -translate-x-1/2" />}
										</div>
									))}
								</div>{" "}
							</div>
						</div>
					</div>
				</div>
				<div className="flex flex-col w-1/2 h-full">
					<div
						className={`flex flex-col h-full w-full bg-rose-100 justify-start items-center rounded-md overflow-y-scroll`}
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
							className={`flex flex-col items-center justify-start pt-2 w-full h-full px-2 mb-4 gap-1 `}
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
					</div>
					{devolucion &&
						<div className="flex flex-col my-2 mx-2 gap-1 h-1/6 w-full">
							<p className="font-bold text-xl px-2 select-none w-full">
								Devolución
							</p>
							<div className="flex flex-row justify-between items-center bg-red-100 p-3 rounded-md">
								<div className="flex flex-col w-full justify-center items-start">
									<p className="font-bold w-full text-center">Cod Devol</p>
									<p className="text-center w-full">
										{devolucion.cod_devolucion}
									</p>
								</div>
								<div className="flex flex-col w-full justify-center items-start">
									<p className="font-bold w-full text-center">Manual</p>
									<p className="text-center w-full">
										{devolucion.cod_manual === "S" ? "SI": "NO"}
									</p>
								</div>
								<div className="flex flex-col w-full justify-center items-start">
									<p className="font-bold w-full text-center">Fecha Devol</p>
									<p className="text-center w-full">{devolucion.fecha_devolucion}</p>
								</div>
								<div className="flex flex-col w-full justify-center items-start">
									<p className="font-bold w-full text-center">Monto Devuelto</p>
									<p className="text-center w-full">{formatFloat(devolucion.monto_devolucion)}</p>
								</div>
								<div className="flex flex-col w-full justify-center items-start text-center">
									<p className="font-bold w-full text-center">Observación</p>
									<p className="text-center w-full">{devolucion.desc_devolucion}</p>
								</div>
							</div>
						</div>
					}
				</div>
			</div>
		)
	);
};
