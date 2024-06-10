import Cookies from "js-cookie";
import {baseDelete, baseGet, basePost, basePostImageDataUrl, basePut, multiPartPost, multiPartPut} from "./base";

export const login = async (cuerpo) => {
	return await basePost("auth/login", "", cuerpo);
};

export const verifyToken = async (cuerpo) => {
	return await baseGet("auth/verifica-token", cuerpo);
};

export const dashBoardClientes = async (filtro) => {
	const token = Cookies.get("token");
	return await basePost("dashboard/clientes", token, filtro);
};

export const dashResumenMontos = async (filtro) => {
	const token = Cookies.get("token");
	return await basePost("dashboard/resumen_montos", token, filtro);
};
export const dashBoardFiltros = async () => {
	const token = Cookies.get("token");
	return await baseGet("dashboard/filtros", token);
};

export const dashBoardOperaciones = async (filtro) => {
	const token = Cookies.get("token");
	console.log("Filtrossssss", filtro);
	return await basePost("dashboard/operaciones", token, filtro);
};
export const dashBoardPrestadores = async (filtro) => {
	const token = Cookies.get("token");
	return await basePost("dashboard/prestadores", token, filtro);
};

export const updatePrestador = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("prestadores/update", token, cuerpo);
};

export async function PdfCartolaPrestador(cuerpo) {
	const token = Cookies.get("token");
	return await basePostImageDataUrl("prestadores/download-pdf", token, cuerpo);
}

export const dashBoardVentasMensual = async (filtro) => {
	const token = Cookies.get("token");
	return await basePost("dashboard/ventas_mensual", token, filtro);
};
export const dashBoardVentasAnual = async (filtro) => {
	const token = Cookies.get("token");
	return await basePost("dashboard/ventas_anual", token, filtro);
};
export const dashBoardVentas = async (filtro) => {
	const token = Cookies.get("token");
	return await basePost("dashboard/ventas", token, filtro);
};
export const allPrestadores = async () => {
	const token = Cookies.get("token");
	return await baseGet("prestadores/all", token);
};
export const allByCodPrestaciones = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_usuario: cod,
	};
	return await basePost("prestaciones/por_cod", token, cuerpo);
};

export const setRevisado = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_servicio: cod,
	};
	return await basePut("prestaciones/cambio_estado_revisado", token, cuerpo);
};

export const pivotActivo = async (cuerpo) => {
	const token = Cookies.get("token");
	console.log(cuerpo)
	return await basePut("prestaciones/cambio_estado_activo", token, cuerpo);
};

export const pivotPausado = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("prestaciones/cambio_estado_pausado", token, cuerpo);
};

export const pivotItemActivo = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("prestaciones/items/cambio_estado_activo", token, cuerpo);
};


export const updatePrestacion = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("prestaciones/update", token, cuerpo);
};

export const pendientesPrestadores = async () => {
	const token = Cookies.get("token");
	return await baseGet("prestadores/pendientes", token);
};
export const rankingPrestadores = async () => {
	const token = Cookies.get("token");
	return await baseGet("prestadores/top_prestadores", token);
};
export const setRevisadoPrestador = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_usuario: cod,
	};
	return await basePut("prestadores/cambiar_estado_revisado", token, cuerpo);
};
export const setActivoPrestador = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("prestadores/cambiar_estado_activo", token, cuerpo);
};
export const setPausadoPrestador = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("prestadores/cambiar_estado_pausado", token, cuerpo);
};

export const allClientes = async () => {
	const token = Cookies.get("token");
	return await baseGet("usuarios/all", token);
};

export const deleteAntecedentes = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_usuario: cod
	}
	return await basePost("usuarios/eliminar_antecedentes", token, cuerpo);
};

export const allPrestaciones = async () => {
	const token = Cookies.get("token");
	return await baseGet("prestaciones/all", token);
};
export const rankingPrestaciones = async (filters) => {
	const token = Cookies.get("token");
	let cuerpo = {}
	Object.keys(filters).map(key => {
		if (filters[key] != "" || filters[key] != 0){
			cuerpo[key] = filters[key]
		}
	})
	return await basePost("prestaciones/top_prestaciones", token, cuerpo);
};

export const detallePrestacion = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_servicio: cod,
	};
	return await basePost("prestaciones/detalle", token, cuerpo);
};

export const liquidacionAll = async () => {
	const token = Cookies.get("token");
	let cuerpo = {
		page: 1,
		page_size: 2000,
	};
	return await basePost("liquidaciones/all", token, cuerpo);
};
export async function PdfLiquidacion(cuerpo) {
	const token = Cookies.get("token");
	return await basePostImageDataUrl("liquidaciones/download-pdf", token, cuerpo);
}

export const devolucionesAll = async () => {
	const token = Cookies.get("token");
	return await baseGet("devoluciones/all-docs-rech", token);
};

export const getDevoluciones = async () => {
	const token = Cookies.get("token");
	return await baseGet("devoluciones/all", token);
};

export const devolucionByCod = async (code) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_documento: code,
	};
	return await basePost("devoluciones/by_cod_doc", token, cuerpo);
};

export const devolByCod = async (code) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_documento: code,
	};
	return await basePost("devoluciones/dev-por-doc", token, cuerpo);
};
export const devolucionCrear = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePost("devoluciones/crear", token, cuerpo);
};

export const devolucionCancelar = async (code) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_devolucion: code,
	};
	const res = await basePut("devoluciones/cancelar", token, cuerpo);
	return res;
};
export const liquidacionUsuario = async () => {
	const token = Cookies.get("token");
	const res = await baseGet("liquidaciones/usuarios_a_liquidar", token);

	return res;
};
export const liquidacionDocumentoByUser = async (cod) => {
	const token = Cookies.get("token");
	let cuerpo = {
		cod_usuario: cod,
	};
	const res = await basePost(
		"liquidaciones/documentos_pendientes_por_usuario",
		token,
		cuerpo
	);
	return res;
};
export const liquidacionCrear = async (cuerpo) => {
	const token = Cookies.get("token");
	const res = await basePost("liquidaciones/crear", token, cuerpo);
	console.log("crear liquidacion", res);
	return res;
};

export const getMesesDocs = async () => {
	const token = Cookies.get("token");
	return await baseGet("documentos/filtro_meses", token);
};

export const getDocumentos = async (mes) => {
	const token = Cookies.get("token");
	return await basePost("documentos/all", token, mes);
};

export async function getPdfDocumento(cuerpo) {
	const token = Cookies.get("token");
	return await basePostImageDataUrl("documentos/download-pdf", token, cuerpo);
}

export const getCambiosEstado = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_documento: cod,
	};
	return await basePost("documentos/mapa", token, cuerpo);
};

export const getDetalleDoc = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_documento: cod,
	};
	return await basePost("documentos/by_cod_doc", token, cuerpo);
};
export const getUsuarioByCod = async (cod) => {
	const token = Cookies.get("token");
	const cuerpo = {
		cod_usuario: cod,
	};
	return await basePost("usuarios/por_cod", token, cuerpo);
};
export const setActivoUsuario = async (cuerpo) => {
	const token = Cookies.get("token");

	return await basePut("usuarios/cambiar_estado_activo", token, cuerpo);
};
export const setPausadoUsuario = async (cuerpo) => {
	const token = Cookies.get("token");

	return await basePut("usuarios/cambiar_estado_pausado", token, cuerpo);
};

export const getAppData = async () => {
	const token = Cookies.get("token");
	return await baseGet("app/info", token);
};

export const updateAppData = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("app/info", token, cuerpo);
};

export const getBancos = async () => {
	const token = Cookies.get("token");
	return await baseGet("bancos/all", token);
};

export const createBanco = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePost("bancos/crear", token, cuerpo);
};

export const updateBanco = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("bancos/actualizar", token, cuerpo);
};

export const deleteBanco = async (cuerpo) => {
	const token = Cookies.get("token");
	return await baseDelete("bancos/eliminar", token, cuerpo);
};

export const getTiposCuentaBancaria = async () => {
	const token = Cookies.get("token");
	return await baseGet("tipos_cuentas_bancarias/all", token);
};

export const createTiposCuentaBancaria = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePost("tipos_cuentas_bancarias/crear", token, cuerpo);
};

export const updateTiposCuentaBancaria = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("tipos_cuentas_bancarias/actualizar", token, cuerpo);
};

export const deleteTiposCuentaBancaria = async (cuerpo) => {
	const token = Cookies.get("token");
	return await baseDelete("tipos_cuentas_bancarias/borrar", token, cuerpo);
};

export const getComunas = async () => {
	const token = Cookies.get("token");
	return await baseGet("comunas/all", token);
};


export const getPersonal = async () => {
	const token = Cookies.get("token");
	return await baseGet("personal/all", token);
};

export const createPersonal = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePost("personal/create", token, cuerpo);
};

export const updatePersonal = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePut("personal/update", token, cuerpo);
};

export const deletePersonal = async (cuerpo) => {
	const token = Cookies.get("token");
	return await baseDelete("personal/delete", token, cuerpo);
};

export const getTiposPersonal = async () => {
	const token = Cookies.get("token");
	return await baseGet("tipos_personal/all", token);
};

export const getPermisos = async () => {
	const token = Cookies.get("token");
	return await baseGet("tipos_personal/permisos", token);
};

export const createTP = async (cuerpo) => {
	const token = Cookies.get("token");
	return await basePost("tipos_personal/create", token, cuerpo);
};

export const updateTP = async (cuerpo) => {
	const token = Cookies.get("token");
	const body = {
		cod_tipo_personal: cuerpo.cod_tipo_personal,
		desc_tipo_personal: cuerpo.desc_tipo_personal,
		permisos: cuerpo.permisos[0] === undefined ? []: cuerpo.permisos
	}
	return await basePut("tipos_personal/update", token, body);
};

export const deleteTP = async (cuerpo) => {
	const token = Cookies.get("token");
	return await baseDelete("tipos_personal/delete", token, cuerpo);
};


export const getCouriers = async (cuerpo) => {
	const token = Cookies.get("token");
	return await baseGet("couriers/all", token, cuerpo);
};


export const  createCourier = async ({img, desc_courier, link_courier}) => {
	console.log("DATA LLEGANDO", img, desc_courier, link_courier)
	const formData = new FormData();
	if (img){
		formData.append('img', img);
	}
	formData.append('desc_courier', desc_courier);
	formData.append('link_courier', link_courier);
	console.log("FORM DATA", formData)
	const token = Cookies.get("token");
	return await multiPartPost("couriers/create", token, formData);
}


export const  updateCourier = async ({img, cod_courier, desc_courier, link_courier}) => {
	console.log("DATA LLEGANDO", img, desc_courier, link_courier)
	const formData = new FormData();
	if (img){
		formData.append('img', img);
	}
	formData.append('cod_courier', cod_courier);
	formData.append('desc_courier', desc_courier);
	formData.append('link_courier', link_courier);
	console.log("FORM DATA", formData)
	const token = Cookies.get("token");
	return await multiPartPut("couriers/update", token, formData);
}


export const deleteCourier = async (cuerpo) => {
	const token = Cookies.get("token");
	return await baseDelete("couriers/delete", token, cuerpo);
};

export const getCategoriasAll = async () => {
	const token = Cookies.get("token");
	return await baseGet("categorias/all", token);
};

export const getRegionesAll = async () => {
	const token = Cookies.get("token");
	return await baseGet("regiones/all", token);
};