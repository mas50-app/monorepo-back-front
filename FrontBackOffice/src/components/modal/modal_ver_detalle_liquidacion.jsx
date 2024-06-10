import React, { useState } from "react";
import { useModalStore } from "../../store/modalsStore";
import Modal_Base from "./modal_base";
import { devolucionCrear, liquidacionCrear } from "../../api/apiBase";
import Modal_mensaje from "./modal_mensaje";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Modal_splash from "./modal_splash";
import { dollarUSLocale } from "../../common/utils/formateo";

const Modal_ver_detalle_liquidacion = ({ dataModal }) => {
	const { hideAllModals } = useModalStore();
	const modalsController = useModalStore((state) => state.modals);
	const [mensaje, setMensaje] = useState("");

	const modalStatus = modalsController.find(
		(modal) => modal.name === "historicoLiquidacion"
	);

	const dataTable = [
		{ type: "text", titulo: "N°" },

		{ type: "text", titulo: "Monto documento" },
		{ type: "text", titulo: "%" },
		{ type: "text", titulo: "Monto liquidación" },
		{ type: "text", titulo: "Monto comisión" },
		{ type: "text", titulo: "Fecha Documento" },
	];

	return (
		<Modal_Base showModal={modalStatus.status} clickOut={true}>
			<div className="inline-block align-middle bg-white w-full h-full overflow-hidden mt-16">
				<div className="flex flex-col justify-start items-start h-full ">
					<div className="flex flex-row justify-between w-full h-full p-3">
						<div className="flex flex-col w-full h-3/5 overflow-y-auto ">
							<div className="overflow-x-auto">
								<table className="table-auto w-full">
									<thead className="text-xs font-semibold uppercase text-gray-500 bg-gray-50 border-t border-b border-gray-200">
										<tr>
											{Array.isArray(dataTable) &&
												dataTable.map((e, i) => {
													if (e.type == "checkBox") {
														return (
															<th
																key={i}
																className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap w-px"
															>
																<div className="flex items-center">
																	<label className="inline-flex">
																		<span className="sr-only">Select all</span>

																		<input
																			id="parent-checkbox"
																			className="form-checkbox"
																			type="checkbox"
																			onChange={() => tongleAll()}
																		/>
																	</label>
																</div>
															</th>
														);
													} else if (e.type == "button") {
														return (
															<th
																key={i}
																className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap w-px"
															>
																<div className="flex items-center">
																	<label className="inline-flex">
																		{e.titulo}
																	</label>
																</div>
															</th>
														);
													} else if (e.type == "text") {
														return (
															<th
																key={i}
																className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap"
															>
																<div className="font-semibold text-left">
																	{e.titulo}
																</div>
															</th>
														);
													}
												})}
										</tr>
									</thead>
									{dataModal != null && (
										<tbody className="text-sm divide-y divide-gray-200">
											{Array.isArray(dataModal.data) &&
												dataModal.data.map((e, i) => (
													<tr key={i} className="cursor-pointer select-none">
														<td>
															<div className="font-medium text-light-blue-500 capitalize">
																{i + 1}
															</div>
														</td>
														{Object.keys(e).map((a, o) => {
															if (
																a == "monto_venta" ||
																a == "monto_liquidacion" ||
																a == "fecha_liquidacion" ||
																a == "monto_comision" ||
																a == "comision"
															) {
																return (
																	<td
																		key={o}
																		className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap"
																	>
																		<div className="font-medium text-light-blue-500 capitalize">
																			{a.includes("monto")
																				? dollarUSLocale(e[a])
																				: e[a]}
																		</div>
																	</td>
																);
															}
														})}
													</tr>
												))}
										</tbody>
									)}
								</table>
							</div>
						</div>
					</div>

					{dataModal.user != undefined && (
						<div className="flex flex-row  w-full bg-rose-100 justify-around items-center p-4 space-x-2">
							<div className="flex flex-col border rounded-md bg-white p-2 justify-start items-start">
								<div>Vendedor: {dataModal.user.nombre_usuario} </div>
								<div>Rut: {dataModal.user.rut_usuario} </div>
								<div>Email: {dataModal.user.mail_usuario} </div>
							</div>
						</div>
					)}

					<div className="flex flex-row mt-5 justify-between rounded-md bg-rose-100 p-2  mx-auto my-5">
						<button
							onClick={() => hideAllModals()}
							type="button"
							class="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
						>
							Cancelar
						</button>
					</div>
				</div>
			</div>
		</Modal_Base>
	);
};

export default Modal_ver_detalle_liquidacion;
