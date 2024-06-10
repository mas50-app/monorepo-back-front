import React, { useState } from "react";
import { useModalStore } from "../../store/modalsStore";
import Modal_Base from "./modal_base";
import { devolucionCrear } from "../../api/apiBase";
import Modal_mensaje from "./modal_mensaje";
import { useMutation, useQueryClient } from "@tanstack/react-query";

const Modal_crear_devolucion = ({ data }) => {
	const { hideAllModals } = useModalStore();
	const modalsController = useModalStore((state) => state.modals);
	const [showAlert, setShowAlert] = useState(false);
	const [mensajeAlert, setMensajeAlert] = useState("");
	const [mensaje, setMensaje] = useState("");
	const queryClient = useQueryClient();
	const modalStatus = modalsController.find(
		(modal) => modal.name === "crearDevolucion"
	);

	const crearDevolucion = useMutation({
		mutationFn: devolucionCrear,
		onMutate: (variables) => {},
		onSuccess: (result) => {
			queryClient.invalidateQueries({ queryKey: ["devolucionesAll"] });
			hideAllModals();
		},
		onError: (error) => {
			setShowAlert(true);
			setMensajeAlert(
				error.response.data.message.replace("Internal Server Error - ", "")
			);
		},
	});

	return (
		<Modal_Base showModal={modalStatus.status} clickOut={false}>
			<div className="inline-block align-middle bg-white w-full h-full overflow-hidden">
				{data != null && (
					<div className="flex flex-row justify-center items-center rounded-md  w-full h-full my-5">
						<div className="flex flex-col h-full w-1/3 mt-16">
							<div className="px-4 py-6 w-full">
								<div className="flex flex-row justify-between mb-2 border rounded-md p-2 w-full">
									<div className="font-bold text-2xl">Reporte</div>
									<div className="text-gray-500">
										Documento {data.cod_documento}
									</div>
								</div>
								<div className="grid grid-cols-2 gap-2 bg-white rounded-md p-2 border w-full">
									<div>
										<div className="font-bold mb-2">
											Descripción del documento
										</div>
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
										<div className="font-bold mb-2">
											Información del vendedor
										</div>

										<div className="mb-4">
											Nombre: {data.vendedor.nombre_usuario}{" "}
											{data.vendedor.apellido1_usuario}{" "}
											{data.vendedor.apellido2_usuario}
										</div>
										<div className="mb-4">Rut: {data.vendedor.rut_usuario}</div>
										<div className="mb-4">
											Mail: {data.vendedor.mail_usuario}
										</div>
									</div>
									<div className="flex flex-col justify-start items-start bg-white  border rounded-md p-2">
										<div className="font-bold mb-2">
											Información del comprador
										</div>
										<div className="mb-4">
											Nombre: {data.comprador.nombre_usuario}{" "}
											{data.comprador.apellido1_usuario}{" "}
											{data.comprador.apellido2_usuario}
										</div>
										<div className="mb-4">
											Rut: {data.comprador.rut_usuario}
										</div>
										<div className="mb-4">
											Mail: {data.comprador.mail_usuario}
										</div>
									</div>
								</div>
							</div>
						</div>
						<div className="flex flex-col justify-center items-center bg-rose-100 w-1/3 h-full  rounded-r-md px-5">
							<div className="w-full mb-5">
								<label
									htmlFor="comment"
									className="block text-sm font-medium text-gray-700"
								>
									Comentario de la devolución
								</label>
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
							<div class="flex flex-row space-x-2 justify-center">
								<button
									onClick={() => hideAllModals()}
									type="button"
									class="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
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
										class="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
									>
										Crear
									</button>
								)}
							</div>
							<div>{mensajeAlert}</div>
						</div>
						<div className="flex flex-col h-full w-1/3 bg-rose-100 justify-start items-center ">
							<div className="flex flex-row justify-between items-center mb-5 mt-16">
								<div className="font-bold text-2xl">Detalle de compra</div>
								<div className="text-gray-500 ml-4">
									{data.detalles[0].fecha_agenda}
								</div>
							</div>

							<div className="flex flex-col items-center justify-center w-full px-4 overflow-y-auto">
								{data.detalles.map((item, index) => {
									return (
										<div
											key={index}
											className="flex flex-row justify-between items-center  bg-white rounded-md p-4 w-full"
										>
											<div className="flex flex-col justify-start items-start">
												<div className="font-bold mb-2">Nombre</div>
												<div className="mb-4">{item.desc_item_servicio}</div>
												<div className="font-bold mb-2">Cantidad</div>
												<div className="mb-4">{item.cantidad}</div>
											</div>
											<div className="flex flex-col justify-start items-start">
												<div className="font-bold mb-2">Fecha</div>
												<div className="mb-4">{item.fecha_agenda}</div>
												<div className="font-bold mb-2">Subtotal</div>
												<div className="mb-4">{item.subtotal}</div>
											</div>
										</div>
									);
								})}
							</div>
						</div>
					</div>
				)}
			</div>
		</Modal_Base>
	);
};

export default Modal_crear_devolucion;
