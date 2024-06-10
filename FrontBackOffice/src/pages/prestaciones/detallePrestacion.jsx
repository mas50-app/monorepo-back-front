import React, { forwardRef, useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
	detallePrestacion,
	pivotActivo,
	pivotItemActivo,
	pivotPausado,
	setRevisado,
	updatePrestacion
} from "../../apis/calls";
import { useMutation } from "@tanstack/react-query";
import { SimpleTable } from "../../components/SimpleTable.jsx";
import { FaRegPauseCircle, FaRegPlayCircle } from "react-icons/all.js";
import { Rating } from "react-simple-star-rating";
import {formatDate1} from "../../utils/dateFormat.js";
import {formatFloat} from "../../utils/formatMoney.js";
import {useForm} from "react-hook-form";
import {OutlinedSimpleInput} from "../../components/forms/Inputs.jsx";
import ChileanRutify from "chilean-rutify";
import { questionMessagePopUp } from "../../components/alerts";

const API_IMAGEN = import.meta.env.VITE_IMAGES_API;

export const DetallePrestacion = () => {
	const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm();
	const navigate = useNavigate();
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const codPrestacion = queryParams.get("codPrestacion");
	const [detalleData, setDetalleData] = useState(null);

	const [refresh, setrefresh] = useState(false);
	const [dataChanged, setDataChanged] = useState(false);

	useEffect(() => {
		if (codPrestacion != null) {
			getPrestacionDetail.mutate(codPrestacion);
		}
	}, [refresh]);

	const getPrestacionDetail = useMutation({
		mutationFn: detallePrestacion,
		onSuccess: (result) => {
			setDetalleData(result);
			Object.keys(result).forEach(key => {
				if (key === "rut_usuario"){
					setValue(key, ChileanRutify.formatRut(result[key]))
				}else{
					setValue(key, result[key])
				}
			});
		},
	});

	const updatePrestData = useMutation({
		mutationFn: updatePrestacion,
		onSuccess: (result) => {
			setrefresh((e) => !e);
		},
	});

	const setPresRevisado = useMutation({
		mutationFn: setRevisado,
		onSuccess: (result) => {
			console.log("Result", result);
			setrefresh((e) => !e);
		},
		onError: (response) => {
			console.log("Error", response)
	}
	});

	const pivotPresActivo = useMutation({
		mutationFn: pivotActivo,
		onSuccess: (result) => {
			console.log("Result", result);
			setrefresh((e) => !e);
		},
		onError: (response) => {
			console.log("Error", response)
		}
	});

	const pivotPresPausado = useMutation({
		mutationFn: pivotPausado,
		onSuccess: (result) => {
			console.log("Result", result);
			setrefresh((e) => !e);
		},
		onError: (response) => {
			console.log("Error", response)
		}
	});

	const pivotItemsActivo = useMutation({
		mutationFn: pivotItemActivo,
		onSuccess: (result) => {
			console.log("Result", result);
			setrefresh((e) => !e);
		},
		onError: (response) => {
			console.log("Error", response)
		}
	});

	const fields = [
		{
			accessor: "cod_item_servicio",
			Header: "Cod Item",
		},
		{
			accessor: "desc_item_servicio",
			Header: "Nombre Item",
		},
		{
			accessor: "desc_unidad",
			Header: "Unidad",
		},
		{
			accessor: "valor_unidad",
			Header: "Valor",
			Cell: ({row}) => (
				<>{formatFloat(row.values.valor_unidad)}</>
			)
		},
		{
			accessor: "cod_activo",
			Header: "Cod Activo",
		},
		{
			accessor: null,
			Header: "Acción",
			Cell: ({ row }) => (
				<button onClick={() => {
					const cuerpo = {
						cod_item_servicio: row.values.cod_item_servicio,
						enum_str: row.values.cod_activo == 'S'? "N" : "S"
					}
					pivotItemsActivo.mutate(cuerpo)}
				}>
					{row.values.cod_activo == "S" ? (
						<FaRegPauseCircle title="Pausar" size="1.5em" />
					) : (
						<FaRegPlayCircle title="Reanudar" size="1.5em" />
					)}
				</button>
			),
		},
	];

	const onSubmit = (d) => {
		const onConfirm = () => {
			updatePrestData.mutate(d)
			setDataChanged(false)
		}
		questionMessagePopUp({title: "Está seguro de guardar los cambios?", functionOnConfirm: onConfirm})
	}

	const snOpts = [
		{
			field: "S",
			label: "S"
		},
		{
			field: "N",
			label: "N"
		}
	]

	return (
		<div className="flex flex-col w-full h-full bg-white">
			{detalleData != null && (
				<form onSubmit={handleSubmit(onSubmit)} className="flex flex-row bg-white p-2 w-full h-full gap-2">
					<div className="flex flex-col w-full">
						<div className="flex flex-row w-full rounded-md">
							<div className="flex flex-col  justify-between w-3/5 p-2">
								<h2 className="text-lg font-extrabold">Ficha de Negocio</h2>
								<div className="flex flex-row justify-between items-around mb-5">
									<h3 className="text-lg font-medium">
										Información del prestador
									</h3>
									{dataChanged &&
										<button
											type="submit"
											className="inline-block px-4 py-3 bg-red-600  text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-red-900 hover:shadow-lg focus:bg-red-900 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-red-800 active:shadow-lg transition duration-150 ease-in-out"
											data-mdb-ripple="true"
											data-mdb-ripple-color="light"
										>
											Actualizar
										</button>
									}

								</div>
								<div className="flex flex-col w-full pr-2  mr-2 ">
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Nombre:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "nombre_usuario",
													type: "text",
													required: true
												}
											}
										/>
									</label>

									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										RUT:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "rut_usuario",
													type: "text",
													required: true
												}
											}
										/>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Email:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "mail_usuario",
													type: "email",
													required: true
												}
											}
										/>
									</label>
								</div>
							</div>
							<div className="inline-flex justify-center items-center border rounded-md w-1/2">
								<img
									src={`${API_IMAGEN}${detalleData.path_imagen}`}
									alt=""
									className=" max-h-44 rounded-md"
								></img>
							</div>
						</div>

						<div className="flex flex-col bg-slate-50 rounded-md p-2 mt-2">
							<h3 className="text-lg font-medium mb-5">Datos del Negocio</h3>

							<div className="flex flex-row w-full pr-2 mr-2 gap-4">
								<div className="flex flex-col w-2/3">
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Nombre:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "nom_servicio",
													type: "text",
													required: true
												}
											}
										/>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Descripción:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "desc_servicio",
													type: "text",
													required: true
												}
											}
										/>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Dirección:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "direccion",
													type: "text",
													required: true
												}
											}
										/>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Domicilio:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "desc_domicilio",
													type: "text",
													required: true
												}
											}
										/>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										D.Antelación:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "dias_antelacion",
													type: "number",
													required: true
												}
											}
										/>
									</label>
								</div>
								<div className="flex flex-col w-1/3">
									<label className="flex flex-row w-full text-gray-700 font-medium mb-1 border-b-2">
										<p className="flex w-2/3">Es Nacional?:</p>
										<div className="flex w-1/3">
											<OutlinedSimpleInput
												register={register}
												watch={watch}
												errors={errors}
												changeFunc={setDataChanged}
												field={
													{
														field: "cod_es_nacional",
														type: "option",
														required: true,
														options: snOpts
													}
												}
											/>
										</div>
									</label>
									<label className="text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										<p className="flex w-2/3">Es Artículo?:</p>
										<div className="flex w-1/3">
											<OutlinedSimpleInput
												register={register}
												watch={watch}
												errors={errors}
												changeFunc={setDataChanged}
												field={
													{
														field: "cod_es_articulo",
														type: "option",
														required: true,
														options: snOpts
													}
												}
											/>
										</div>
									</label>
									<label className="text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										<p className="flex w-2/3">Retiro Local?:</p>
										<div className="flex w-1/3">
											<OutlinedSimpleInput
												register={register}
												watch={watch}
												errors={errors}
												changeFunc={setDataChanged}
												field={
													{
														field: "cod_retiro",
														type: "option",
														required: true,
														options: snOpts
													}
												}
											/>
										</div>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										<p className="flex w-2/3">Delivery?:</p>
										<div className="flex w-1/3">
											<OutlinedSimpleInput
												register={register}
												watch={watch}
												errors={errors}
												changeFunc={setDataChanged}
												field={
													{
														field: "cod_domicilio",
														type: "option",
														required: true,
														options: snOpts
													}
												}
											/>
										</div>
									</label>
								</div>
							</div>
						</div>
						<div className="flex flex-col bg-slate-50 rounded-md p-2 mt-2 overflow-hidden">
							<div className="flex flex-row items-center mb-5 justify-between border-b-2">
								<h3 className="text-lg font-medium ">Valoraciones</h3>
								{detalleData.valoraciones ? (
									<div className="flex flex-row justify-end text-end">
										<label className="flex items-center justify-center text-gray-700 text-center font-medium uppercase">
											Media
										</label>
										<Rating
											className="my-4 mr-2 ml-3"
											readonly
											transition
											size={30}
											initialValue={detalleData.valoraciones.valoracion_media}
											fillColorArray={[
												"#f17a45",
												"#f19745",
												"#f1a545",
												"#f1b345",
												"#f1d045",
											]}
										/>
									</div>
								) : (
									<label>No evaluado</label>
								)}
							</div>
							<div className="overflow-y-auto w-full pr-2 mr-2">
								{detalleData.valoraciones &&
									detalleData.valoraciones.evaluaciones.map((ev, index) => (
										<div className="border-b-2 mb-2">
											<div className="flex flex-row justify-between mb-2">
												<label
													className=" text-gray-700 font-medium"
													key={index}
												>
													{ev.desc_usuario}
												</label>
												<Rating
													transition
													readonly
													size={20}
													initialValue={ev.valor}
													fillColorArray={[
														"#f17a45",
														"#f19745",
														"#f1a545",
														"#f1b345",
														"#f1d045",
													]}
												/>
												<label className="text-gray-700 font-medium mb-1">
													{formatDate1(ev.fecha_evaluacion)}
												</label>
											</div>
											<div className="flex flex-row">
												<p className="ml-3 font-bold text-gray-400">{ev.desc_evaluacion}</p>
											</div>
										</div>
									))}
								</div>
							</div>
						</div>
					<div className="flex flex-col">
						<h3 className="text-lg font-medium text-center bg-red-200 rounded-md">
							Lista de Items
						</h3>

						{detalleData.items.length > 0 && (
							<div className="overflow-y-auto flex flex-col my-2 border rounded-md h-full">
								<SimpleTable
									COLUMNS={fields}
									data={detalleData.items}
									hiddenColumns={["cod_activo"]}
								/>
							</div>
						)}

						<div className="flex space-x-2 justify-center items-center mt-4">
							<button
								onClick={() => navigate("/prestaciones")}
								type="button"
								className="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
							>
								Regresar
							</button>

							<button
								onClick={() => setPresRevisado.mutate(detalleData.cod_servicio)}
								type="button"
								disabled={detalleData.cod_revisado !== "N"}
								className={`inline-block  ${
									detalleData.cod_revisado !== "N"
										? "bg-gray-400"
										: "bg-rose-600 hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 "
								}  px-6 py-2.5  text-white font-medium text-xs leading-tight uppercase rounded shadow-md active:shadow-lg transition duration-150 ease-in-out`}
							>
								{detalleData.cod_revisado !== "N" ? "Revisado" : "Revisar"}
							</button>
							<button
								onClick={() => {
									const cuerpo = {
										cod_servicio: detalleData.cod_servicio,
										enum_str: detalleData.cod_activo == 'S'? "N" : "S"
									};
									pivotPresActivo.mutate(cuerpo)
								}
								}
								type="button"
								className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
							>
								{detalleData.cod_activo === "S" ? "Inactivar" : "Activar"}
							</button>
							<button
								onClick={() => {
									const cuerpo = {
										cod_servicio: detalleData.cod_servicio,
										enum_str: detalleData.cod_pausado == 'S'? "N" : "S"
									}
									pivotPresPausado.mutate(cuerpo)
								}
								}

								type="button"
								className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
							>
								{detalleData.cod_pausado === "S" ? "Reanudar" : "Pausar"}
							</button>
						</div>
					</div>
				</form>
			)}
		</div>
	);
};
