import React, {
	forwardRef,
	useEffect,
	useRef,
	useState,
} from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
	allByCodPrestaciones, deleteAntecedentes, getBancos, getComunas, getTiposCuentaBancaria,
	liquidacionCrear,
	liquidacionDocumentoByUser,
	setActivoPrestador,
	setPausadoPrestador,
	setRevisadoPrestador, updatePrestador,
} from "../../apis/calls";
import { useMutation } from "@tanstack/react-query";
import { Table } from "../../components/Table";
import { formatFloat } from "../../utils/formatMoney.js";
import {
	errorMessagePopUp,
	loadingPopup,
	questionMessagePopUp,
	SimpleLoadingPopup,
	successMessagePopUp
} from "../../components/alerts.jsx";
import {useForm} from "react-hook-form";
import {OutlinedSimpleInput} from "../../components/forms/Inputs.jsx";
import ChileanRutify from "chilean-rutify";
const API_IMAGEN = import.meta.env.VITE_IMAGES_API;

const IndeterminateCheckbox = forwardRef(({ indeterminate, ...rest }, ref) => {
	const defaultRef = useRef();
	const resolvedRef = ref || defaultRef;

	useEffect(() => {
		resolvedRef.current.indeterminate = indeterminate;
	}, [resolvedRef, indeterminate]);
	return (
		<>
			<input type="checkbox" ref={resolvedRef} {...rest} />
		</>
	);
});

export const DetallePrestador = () => {
	const navigate = useNavigate();
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const codPrestador = queryParams.get("codPrestador");

	const [refresh, setrefresh] = useState(false);
	const [data, setData] = useState(null);
	const [liquidacionesByUser, setliquidacionesByUser] = useState(null);
	const [selectedRows, setSelectedRows] = React.useState([]);
	const [mensaje, setMensaje] = useState("");
	const [bancos, setBancos] = useState(null);
	const [bancosOpts, setBancosOpts] = useState(null);
	const [tiposCBancaria, setTiposCBancaria] = useState(null);
	const [tiposCBancOpts, setTiposCBancOpts] = useState(null);
	const [regiones, setRegiones] = useState(null);
	const [provinciasOpts, setProvinciasOpts] = useState(null);
	const [comunasOpts, setComunasOpts] = useState(null);
	const [selectedProvincia, setSelectedProvincia] = useState(null);
	const [montoALiquidar, setMontoALiquidar] = useState(0);
	const [dataChanged, setDataChanged] = useState(false);

	const [dataIsLoading, setDataIsLoading] = useState(true);
	const [bancosIsLoading, setBancosIsLoading] = useState(true);
	const [comunasIsLoading, setComunasIsLoading] = useState(true);
	const [montosIsLoading, setMontosIsLoading] = useState(true);

	const { register, handleSubmit, formState: { errors }, watch, setValue } = useForm();

	useEffect(() => {
		if (codPrestador != null) {
			getDataBancos.mutate()
			getDataTiposCBancaria.mutate()
			getDataComunas.mutate()
			getPrestador.mutate(codPrestador)
		}
		setDataIsLoading(false)
	}, [refresh]);

	useEffect(() => {
		if (bancos != null && bancosOpts == null){
			let bOps = []
			bancos?.forEach(banco => {
				bOps.push({
					field: banco.cod_banco,
					label: banco.desc_banco
				})
			});
			setBancosOpts(bOps)
		}
		if (tiposCBancaria != null && tiposCBancOpts ==  null){
			let tcOps = []
			tiposCBancaria?.forEach(cta => {
				tcOps.push({
					field: cta.cod_tipo_cuenta_bancaria,
					label: cta.desc_tipo_cuenta_bancaria
				})
			});
			setTiposCBancOpts(tcOps)
		}
		setBancosIsLoading(false)
	}, [bancos, tiposCBancaria]);

	useEffect(() => {
		if (regiones != null){
			if (provinciasOpts == null){
				let provOps = []
				regiones?.forEach((region, index) => {
					region.provincias.forEach((provincia) => {
						if (provincia.cod_provincia === selectedProvincia) {
							regiones[index].provincias.forEach(prov => {
								provOps.push({
									field: prov.cod_provincia,
									label: prov.desc_provincia
								})
							})

						}
					})
				});
				setProvinciasOpts(provOps)
			}
			if (comunasOpts == null){
				console.log("ENTRO a comunas")
				let comOps = []
				regiones?.forEach(region => {
					region.provincias.forEach(provincia => {
						if (provincia.cod_provincia === selectedProvincia) {
							provincia.comunas.forEach(comuna => {
								comOps.push({
									field: comuna.cod_comuna,
									label: comuna.desc_comuna
								})
							})
						}
					})
				});
				setComunasOpts(comOps)
			}
		}
		setComunasIsLoading(false)
	}, [regiones, selectedProvincia]);


	useEffect(() => {
		if (selectedRows.length > 0) {
			let monto = 0.0;
			selectedRows.map((row) => {
				monto += parseFloat(row.original.monto_liquidacion);
			});
			setMontoALiquidar(monto);
			return;
		}
		setMontoALiquidar(0);
		setMontosIsLoading(false)
	}, [selectedRows]);

	const getLiquidacionByDocument = useMutation({
		mutationFn: liquidacionDocumentoByUser,
		onSuccess: (result) => {
			setliquidacionesByUser(result);
		},
	});

	const getPrestador = useMutation({
		mutationFn: allByCodPrestaciones,
		onSuccess: (result) => {
			setData(result);
			setSelectedProvincia(result.cod_provincia);
			Object.keys(result).forEach(key => {
				if (key === "rut_usuario"){
					setValue(key, ChileanRutify.formatRut(result[key]))
				}else{
					setValue(key, result[key])
				}
			});
			getLiquidacionByDocument.mutate(codPrestador);
		},
	});

	const updateDataPrestador = useMutation({
		mutationFn: updatePrestador,
		onSuccess: (result) => {
			if (result === null) {
				errorMessagePopUp({title: "Error", message: "No se pudo actualizar el registro"})
				return
			}
			successMessagePopUp({title:"Terminado", message:"Registro actualizado exitosamente"})
			setrefresh((e) => !e);
			setDataChanged(false)
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const setRevisado = useMutation({
		mutationFn: setRevisadoPrestador,
		onSuccess: (result) => {
			setrefresh((e) => !e);
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const deleteAnts = useMutation({
		mutationFn: deleteAntecedentes,
		onSuccess: (result) => {
			setrefresh((e) => !e);
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const setActivo = useMutation({
		mutationFn: setActivoPrestador,
		onSuccess: (result) => {
			setrefresh((e) => !e);
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const setPausado = useMutation({
		mutationFn: setPausadoPrestador,
		onSuccess: (result) => {
			setrefresh((e) => !e);
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const getDataComunas = useMutation({
		mutationFn: getComunas,
		onSuccess: (result) => {
			setRegiones(result)
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const getDataBancos = useMutation({
		mutationFn: getBancos,
		onSuccess: (result) => {
			setBancos(result)
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const getDataTiposCBancaria = useMutation({
		mutationFn: getTiposCuentaBancaria,
		onSuccess: (result) => {
			setTiposCBancaria(result)
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const crearLiquidacion = useMutation({
		mutationFn: liquidacionCrear,
		onSuccess: (result) => {
			refreshPage();
		},
		onError: (e) => {
			console.log("error", e);
		},
	});

	const refreshPage = () => {
		window.location.reload();
	};

	const fields = [
		{
			id: "selection",
			// The header can use the table's getToggleAllRowsSelectedProps method
			// to render a checkbox
			Header: ({ getToggleAllRowsSelectedProps }) => (
				<div>
					<IndeterminateCheckbox {...getToggleAllRowsSelectedProps()} />
				</div>
			),
			// The cell can use the individual row's getToggleRowSelectedProps method
			// to the render a checkbox
			Cell: ({ row, selectedFlatRows }) => {
				return <IndeterminateCheckbox {...row.getToggleRowSelectedProps()} />;
			},
		},
		{
			accessor: "cod_documento",
			Header: "Cod documento",
		},
		{
			accessor: "monto_documento",
			Header: (
				<div className="justify-center text-center" title="Pago recibido">
					Venta
				</div>
			),
			Cell: ({ row }) => <>{formatFloat(row.values.monto_documento)}</>,
		},
		{
			accessor: "comision",
			Header: <div title="% de Comisión">%C</div>,
			Cell: ({ row }) => <>{row.values.comision}</>,
		},
		{
			accessor: "monto_comision_neto",
			Header: <div title="Monto Comisión">M.Com</div>,
			Cell: ({ row }) => <>{formatFloat(row.values.monto_comision_neto)}</>,
		},
		{
			accessor: "monto_iva",
			Header: <div title="19%">IVA</div>,
			Cell: ({ row }) => <>{formatFloat(row.values.monto_iva)}</>,
		},
		{
			accessor: "monto_comision_bruto",
			Header: <div title="Monto de Comisión + IVA">Com.+IVA</div>,
			Cell: ({ row }) => <>{formatFloat(row.values.monto_comision_bruto)}</>,
		},
		{
			accessor: "monto_liquidacion",
			Header: <div title="Monto Liquidación">M. Liq</div>,
			Cell: ({ row }) => <>{formatFloat(row.values.monto_liquidacion)}</>,
		},
	];

	const handleProvinciaChange = (e) => {
		setValue("cod_provincia", e)
		setSelectedProvincia(e)
		setComunasOpts(null)
		setDataChanged(true)
	}

	const onSubmit = (d) => {
		const onConfirm = () => {
			updateDataPrestador.mutate({
				cod_usuario: d.cod_usuario,
				desc_usuario: d.desc_usuario,
				nombre_usuario: d.nombre_usuario,
				apellido1_usuario: d.apellido1_usuario,
				rut_usuario: d.rut_usuario,
				mail_usuario: d.mail_usuario,
				cod_comuna: d.cod_comuna,
				comision: d.comision,
				cod_banco: d.cod_banco,
				cod_tipo_cuenta_bancaria: d.cod_tipo_cuenta_bancaria,
				nro_cuenta_bancaria: d.nro_cuenta_bancaria,
			})
		}
		questionMessagePopUp({title: "Está seguro de guardar los cambios?", functionOnConfirm: onConfirm})
	}

	if (
		dataIsLoading || comunasIsLoading || montosIsLoading ||
		bancosIsLoading || comunasOpts === null || provinciasOpts === null ||
		tiposCBancOpts === null || bancosOpts === null
	){
		return <SimpleLoadingPopup/>
	}

	return (
		<div className="flex flex-row bg-white w-full h-full">
			<div className="flex flex-col w-full h-full">
				{data != null && (
					<form onSubmit={handleSubmit(onSubmit)} className="flex flex-col bg-white p-6 rounded-lg shadow-md w-full overflow-y-auto">
						<h2 className="text-xl font-extrabold">Ficha Prestador</h2>
						<div className="flex flex-row">
							<div className="flex flex-col justify-around mb-5 w-1/2">
								<label className="flex flex-row w-3/5 text-gray-700 font-bold mb-1 border-b-2">
									<p className="flex w-2/3">Comisión:</p>
									<div className="flex w-1/3">
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "comision",
													type: "number",
													required: true
												}
											}
										/>
									</div>
								</label>
								<h3 className="text-lg font-medium">
									Información del prestador
								</h3>
							</div>
							<div className="flex flex-row justify-end items-around mb-5 w-1/2">
								<div className="inline-flex justify-center items-center border rounded-md w-1/2">
									<img
										src={`${API_IMAGEN}${data.path_imagen}`}
										alt=""
										className="max-h-44 m-2 rounded-md"
									/>
								</div>
							</div>
						</div>
						{dataChanged &&
							<button
								type="submit"
								className="inline-block px-4 py-3 bg-red-600 w-1/4 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-red-900 hover:shadow-lg focus:bg-red-900 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-red-800 active:shadow-lg transition duration-150 ease-in-out"
								data-mdb-ripple="true"
								data-mdb-ripple-color="light"
							>
								Actualizar
							</button>
						}
						{(comunasOpts?.length > 0 && provinciasOpts?.length > 0 && comunasIsLoading === false) &&
							<div className="flex flex-row mt-2">
								<div className="w-1/2 pr-2  mr-2 ">
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

								<div className="w-1/2 pl-2 ">
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Apellido:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "apellido1_usuario",
													type: "text",
													required: true
												}
											}
										/>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Comuna:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={setDataChanged}
											field={
												{
													field: "cod_comuna",
													type: "option",
													required: true,
													options: comunasOpts
												}
											}
										/>
									</label>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										Provincia:
										<OutlinedSimpleInput
											register={register}
											watch={watch}
											errors={errors}
											changeFunc={handleProvinciaChange}
											field={
												{
													field: "cod_provincia",
													type: "option",
													required: true,
													options: provinciasOpts
												}
											}
										/>
									</label>
								</div>
							</div>
						}
						{(bancosOpts?.length > 0 && tiposCBancOpts?.length > 0) &&
							<div className="mt-4">
								<h3 className="text-lg font-medium mb-5">Datos Bancarios</h3>
								<div className="flex flex-row mt-2">
									<div className="w-1/2 pr-2 mr-2">
										<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
											Banco:
											<OutlinedSimpleInput
												register={register}
												watch={watch}
												errors={errors}
												changeFunc={setDataChanged}
												field={
													{
														field: "cod_banco",
														type: "option",
														required: true,
														options: bancosOpts
													}
												}
											/>
										</label>
										<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
											N°cuenta:
											<OutlinedSimpleInput
												register={register}
												watch={watch}
												errors={errors}
												changeFunc={setDataChanged}
												field={
													{
														field: "nro_cuenta_bancaria",
														type: "text",
														required: true
													}
												}
											/>
										</label>
									</div>

									<div className="w-1/2 pl-2 ">
										<label className="text-gray-700 font-medium mb-1 flex flex-row border-b-2">
											Tip.Cuenta:
											<OutlinedSimpleInput
												register={register}
												watch={watch}
												errors={errors}
												changeFunc={setDataChanged}
												field={
													{
														field: "cod_tipo_cuenta_bancaria",
														type: "option",
														required: true,
														options: tiposCBancOpts
													}
												}
											/>
										</label>
									</div>
								</div>
							</div>
						}

						<div className="mt-4">
							{
								data.docs.length > 0 ?
									<>
										<h3 className="text-lg font-medium">Antecedentes</h3>
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
														className="flex flex-col mt-4 rounded-md bg-rose-100 p-2 shadow-lg border-2 border-rose-200 justify-start items-center"
													>
														<p className="text-lg font-medium">
															{i + 1} - {desc_tipo_antecedente}
														</p>

														<img
															className="w-72"
															src={API_IMAGEN + path_imagen}
															alt="antecedentes"
														/>
													</div>
												);
											})}
										</div>
										<div className="justify-center text-center">
											<button
												onClick={(e) => {
													e.preventDefault();
													const delAnt = async () => {
														await deleteAnts.mutateAsync(codPrestador)
													};
													questionMessagePopUp({
														title: "Está seguro de realizar esta acción?",
														functionOnConfirm: delAnt
													})
												}
												}
												className="mt-2 px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-red-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
											>
												Rechazar Antecedentes
											</button>
										</div>
									</>:
									<>
										<h3 className="text-lg font-medium">Antecedentes</h3>
										<p className="text-lg font-medium text-center">Se rechazaron los antecedentes</p>
									</>
							}

							{data.servicios.length > 0 && (
								<div className="bg-white p-6 rounded-md flex flex-col">
									<h2 className="text-lg font-medium">Lista de talentos</h2>
									<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
										<p className="ml-3 font-bold">
											{data.desc_talento_usuario}
										</p>
									</label>

									<div className="mt-4">
										{data.servicios.map((e, i) => (
											<a
												title="Ir a Prestación"
												href={`/prestaciones/detalle/?codPrestacion=${e.cod_servicio}`}
												key={i}
												className="relative flex  justify-between p-2 rounded-lg bg-gray-200 my-4"
											>
												<p className="absolute -top-3 bg-rose-200 rounded-md px-2">
													{i + 1}
												</p>
												<div className="flex flex-col mt-1 ">
											<span className="flex flex-row items-start">
												<p>Nombre: </p>
												<p className="ml-2 font-bold">{e.nom_servicio}</p>
											</span>
													<span className="flex flex-row items-start">
												<p>Unidad de venta: </p>
												<p className="ml-2 font-bold">{e.desc_unidad}</p>
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
												<p className="ml-2 font-bold">{e.direccion}</p>
											</span>
											{/*		<span className="flex flex-row items-start">*/}
											{/*	<p>Precio: </p>*/}
											{/*	<p className="ml-2 font-extrabold text-rose-500">*/}
											{/*		{e.valor_unidad}*/}
											{/*	</p>*/}
											{/*</span>*/}
												</div>
												<div className="flex flex-col">
													<div className="flex flex-col justify-end text-right">
														<div className="font-bold">Descripción:</div>
														<div className="">{e.desc_servicio}</div>
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
											</a>
										))}
									</div>
								</div>
							)}
							{
								<div className="flex space-x-2 justify-center items-center mt-4">
									<button
										onClick={() => navigate("/prestadores")}
										type="button"
										className="inline-block px-6 py-2.5 bg-red-400 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-red-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
									>
										Regresar
									</button>

									<button
										onClick={() => setRevisado.mutate(data.cod_usuario)}
										type="button"
										disabled={data.cod_revisado !== "N"}
										className={`inline-block  ${
											data.cod_revisado !== "N"
												? "bg-gray-400"
												: "bg-rose-600 hover:bg-red-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 "
										}  px-6 py-2.5  text-white font-medium text-xs leading-tight uppercase rounded shadow-md active:shadow-lg transition duration-150 ease-in-out`}
									>
										{data.cod_revisado !== "N" ? "Validado" : "Validar"}
									</button>
									<button
										onClick={() =>
											setActivo.mutate({
												cod_usuario: data.cod_usuario,
												enum_str: data.cod_activo == "S" ? "N" : "S",
											})
										}
										type="button"
										className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-red-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
									>
										{data.cod_activo === "S" ? "Inactivar" : "Activar"}
									</button>
									<button
										onClick={() =>
											setPausado.mutate({
												cod_usuario: data.cod_usuario,
												enum_str: data.cod_pausado == "S" ? "N" : "S",
											})
										}
										type="button"
										className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-red-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
									>
										{data.cod_pausado === "S" ? "Reanudar" : "Pausar"}
									</button>
								</div>
							}
						</div>
						<div className="bg-white p-6 rounded-md flex flex-col">
							<h2 className="text-lg font-medium">Couriers</h2>
							<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2"/>
							<div className="flex flex-row justify-start gap-4 p-4">
								{
									data.couriers?.map((courier) => (
										<div
											key={courier.cod_courier}
											className="flex flex-col gap-2 rounded-md justify-center items-center bg-gray-200 shadow-md p-2"
										>
											<img
												// width={60}
												// height={60}
												className="rounded-md"
												src={`${API_IMAGEN}${courier.path_imagen}`}
												alt="Imagen Courier"
											/>
											<p>{courier?.desc_courier}</p>
										</div>
									))
								}
							</div>
						</div>
					</form>
				)}
			</div>
			<div className="flex flex-col justify-start items-center w-3/4 h-full rounded-md shadow overflow-y-auto">
				{liquidacionesByUser != null &&
					(liquidacionesByUser.docs.length > 0 ? (
						<div className="flex flex-col justify-start w-full items-center">
							<p className="border-sm rounded-md mb-2 bg-red-300 w-full text-center">
								Liquidaciones pendientes
							</p>
							<div className="w-full px-4 ">
								<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
									Monto total ventas:
									<p className="ml-3 font-bold ">
										{formatFloat(liquidacionesByUser.monto_total_ventas)}
									</p>
								</label>

								<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
									Monto total comisión:
									<p className="ml-3 font-bold ">
										{formatFloat(liquidacionesByUser.monto_total_comision)}
									</p>
								</label>
								<label className=" text-gray-700 font-medium mb-1 flex flex-row border-b-2">
									Monto total liquidación:
									<p className="ml-3 font-bold ">
										{formatFloat(liquidacionesByUser.monto_total_liquidacion)}
									</p>
								</label>
							</div>

							<div className="overflow-x-auto w-full">
								<Table
									className="text-xs"
									onRowSelect={(rows) => setSelectedRows(rows)}
									data={liquidacionesByUser.docs}
									COLUMNS={fields}
									hiddenColumns={["cod_documento"]}
									parentName="A Liquidar"
									filterGlobal={false}
								/>
							</div>
							<p className="mb-3">Comentario de la Liquidación</p>
							<div className="my-1 px-2 w-full">
						<textarea
							rows={4}
							name="comment"
							id="comment"
							className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full h-full sm:text-sm border border-gray-300 rounded-md max-h-32 p-3"
							defaultValue={""}
							onChange={(e) => setMensaje(e.target.value)}
						/>
							</div>
							{mensaje != "" && (
								<>
									<button
										onClick={() => {
											let monto_venta = 0;
											let monto_comision_bruto = 0;
											let monto_liquidacion = 0;
											let detalles = [];
											selectedRows.map((item) => {
												monto_venta += item.original.monto_documento;
												monto_comision_bruto +=
													item.original.monto_comision_bruto;
												monto_liquidacion += item.original.monto_liquidacion;
												detalles.push({
													desc_detalle_liquidacion: "",
													cod_documento: item.original.cod_documento,
													monto_documento: item.original.monto_documento,
												});
											});

											selectedRows.length > 0 &&
											crearLiquidacion.mutate({
												cod_usuario: data.cod_usuario,
												comision: monto_comision_bruto,
												desc_liquidacion: mensaje,
												monto_liquidacion: monto_liquidacion,
												monto_venta: monto_venta,
												detalles: detalles,
											});
										}}
										className="inline-block px-6 py-2.5 bg-rose-600 text-white font-medium text-xs leading-tight uppercase rounded shadow-md hover:bg-red-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
									>
										Liquidar{" "}
										{selectedRows.length === 0
											? ""
											: formatFloat(montoALiquidar)}
									</button>
								</>
							)}
						</div>
					) : (
						<div className="flex flex-col justify-start items-center p-5 border rounded-md">
							<p>No hay liquidaciones pendientes</p>
						</div>
					))}
			</div>
		</div>
	);
};
