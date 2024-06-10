import React, { useEffect, useState } from "react";
import { QueryClient, useMutation } from "@tanstack/react-query";
import { useModalStore } from "../../store/modalsStore";
const API_IMAGEN = import.meta.env.VITE_IMAGES_API;

function Modal_ficha_prestador({ data }) {
	const { hideAllModals } = useModalStore();
	const modalsController = useModalStore((state) => state.modals);
	const modalStatus = modalsController.find(
		(modal) => modal.name === "fichaAntecedentes"
	);
	const setPendientes = useMutation({
		mutationFn: setPendientesPrestadores,
		onSuccess: (result) => {
			hideAllModals();
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	return (
		<Modal_Base showModal={modalStatus.status} clickOut={false}>
			<div className="inline-block align-middle bg-white w-full">
				<div className="w-full h-full ">
					<div className="bg-white p-4 rounded-lg w-full flex justify-center">
						{data != null && (
							<div class="bg-white p-6 rounded-lg shadow-md w-[50rem]">
								<h2 class="text-lg font-extrabold">Ficha Prestador</h2>
								<div class="mt-4">
									<h3 class="text-lg font-medium mb-5">
										Información del prestador
									</h3>
									<div class="flex flex-row mt-2">
										<div class="w-1/2 pr-2  mr-2 ">
											<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
												Nombre:
												<p className="ml-3 font-bold ">{data.nombre_usuario}</p>
											</label>

											<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
												RUT:
												<p className="ml-3 font-bold">{data.rut_usuario}</p>
											</label>
											<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
												Email:
												<p className="ml-3 font-bold">{data.mail_usuario}</p>
											</label>
										</div>

										<div class="w-1/2 pl-2 ">
											<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
												Apellido:
												<p className="ml-3 font-bold">
													{data.apellido1_usuario}
												</p>
											</label>
											<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
												Comuna:
												<p className="ml-3 font-bold">{data.desc_comuna}</p>
											</label>
											<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
												Provincia:
												<p className="ml-3 font-bold">{data.desc_provincia}</p>
											</label>
										</div>
									</div>

									<div class="mt-4">
										<h3 class="text-lg font-medium mb-5">Datos Bancarios</h3>
										<div class="flex flex-row mt-2">
											<div class="w-1/2 pr-2 mr-2">
												<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
													Nombre:
													<p className="ml-3 font-bold ">{data.desc_banco}</p>
												</label>
												<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
													N° cuenta:
													<p className="ml-3 font-bold ">
														{data.nro_cuenta_bancaria}
													</p>
												</label>
											</div>

											<div class="w-1/2 pl-2 ">
												<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
													Tipo de cuenta:
													<p className="ml-3 font-bold ">
														{data.desc_tipo_cuenta_bancaria}
													</p>
												</label>
											</div>
										</div>
									</div>

									<div class="mt-4">
										<h3 class="text-lg font-medium">Antecedentes</h3>
										<div className="flex flex-wrap gap-3 justify-center">
											{data.docs.map((doc, i) => {
												const {
													cod_antecedente,
													desc_antecedente,
													cod_tipo_antecedente,
													desc_tipo_antecedente,
													path_imagen,
												} = doc;

												return (
													<div
														key={cod_antecedente}
														className="mt-4 rounded-md bg-rose-100 p-2 shadow-lg border-2 border-rose-200"
													>
														<h4 className="text-lg font-medium">
															{i + 1} - {desc_tipo_antecedente}
														</h4>
														<img
															width={200}
															height={200}
															src={{ API_IMAGEN } + path_imagen}
															alt="antecedentes"
														/>
													</div>
												);
											})}
										</div>
										<div class="bg-white p-6 rounded-lg shadow-md">
											<h2 class="text-lg font-medium">Lista de talentos</h2>
											<label class=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
												Talento:
												<p className="ml-3 font-bold">
													{data.desc_talento_usuario}
												</p>
											</label>
											<div class="mt-4">
												<div>
													{data.servicios.map((e, i) => (
														<div
															key={i}
															class="relative flex  justify-between p-2 rounded-lg bg-gray-200 my-4"
														>
															<p className="absolute -top-3 bg-rose-200 rounded-md px-2">
																{i + 1}
															</p>
															<div className="flex flex-col mt-1 ">
																<span className="flex flex-row items-start">
																	<p>Nombre: </p>
																	<p className="ml-2 font-bold">
																		{e.nom_servicio}
																	</p>
																</span>
																<span className="flex flex-row items-start">
																	<p>Unidad de venta: </p>
																	<p className="ml-2 font-bold">
																		{e.desc_unidad}
																	</p>
																</span>
																<span className="flex flex-row items-start">
																	<p>Con agenda: </p>
																	<p className="ml-2 font-bold">
																		{e.dias_antelacion > 0 ? "Si" : "No"}
																	</p>
																</span>
																{e.dias_antelacion > 0 && (
																	<span className="flex flex-row items-start">
																		<p>Dias de antelación: </p>
																		<p className="ml-2 font-bold">
																			{e.dias_antelacion}
																		</p>
																	</span>
																)}
																<span className="flex flex-row items-start">
																	<p>Dirección: </p>
																	<p className="ml-2 font-bold">
																		{e.direccion}
																	</p>
																</span>
																<span className="flex flex-row items-start">
																	<p>Precio: </p>
																	<p className="ml-2 font-extrabold text-rose-500">
																		{e.valor_unidad}
																	</p>
																</span>
															</div>
															<div className="flex flex-col">
																<div className="flex flex-col justify-end text-right">
																	<div className="font-bold">Descripción:</div>
																	<div className="capitalize">
																		{e.desc_servicio}
																	</div>
																</div>
																<div className="flex flex-col justify-end text-right">
																	<div className="font-bold">Retiro:</div>
																	<div className="capitalize">
																		{e.cod_retiro == "N"
																			? "Sin retiro"
																			: "Con retiro"}
																	</div>
																</div>
															</div>
														</div>
													))}
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						)}
					</div>
				</div>
				<div className="flex flex-row mt-5 justify-between rounded-md bg-rose-100 p-2 w-60 mx-auto my-5">
					<div class="flex space-x-2 justify-center">
						<button
							onClick={() => hideAllModals()}
							type="button"
							class="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
						>
							Cancelar
						</button>
					</div>
					<div class="flex space-x-2 justify-center">
						<button
							onClick={() => setPendientes.mutate(data.cod_usuario)}
							type="button"
							class="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
						>
							Validar
						</button>
					</div>
				</div>
			</div>
		</Modal_Base>
	);
}

export default Modal_ficha_prestador;
