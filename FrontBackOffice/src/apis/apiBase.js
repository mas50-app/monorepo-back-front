import axios from "axios";
// 	baseURL: "http://190.114.255.200:8002/api/v1/back_office/",
const axiosWithAuth = (token) => {
	if (token == undefined) {
		return axios.create({
			baseURL: "http://45.236.128.241:8003/api/v1/back_office/",
		});
	} else {
		return axios.create({
			baseURL: "http://45.236.128.241:8003/api/v1/back_office/",
			timeout: 0,
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});
	}
};

/* const axiosWithAuth = (token) => {
	if (token == undefined) {
		return axios.create({
			baseURL: "http://192.168.1.93:8002/api/v1/back_office/",
		});
	} else {
		return axios.create({
			baseURL: "http://192.168.1.93:8002/api/v1/back_office/",
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});
	}
}; */

export const login = async (cuerpo) => {
	console.log("cuerpo entrante", cuerpo);
	const res = await axiosWithAuth().post("auth/login", cuerpo);
	console.log("res", res);
	return res;
};

export const allPrestadores = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get("prestadores/all");
	return res;
};

export const pendientesPrestadores = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get("prestadores/pendientes");
	console.log("pendientes", res);
	return res;
};

export const setPendientesPrestadores = async (codes) => {
	const res1 = await axios.get("/api/getToken");

	const cuerpo = {
		cod_usuario: codes,
	};
	console.log(cuerpo);
	const res = await axiosWithAuth(res1.data).put(
		"prestadores/cambiar_estado_revisado",
		cuerpo
	);
	return res;
};

export const allClientes = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get("usuarios/all");
	return res;
};

export const allPrestaciones = async () => {
	const res1 = await axios.get("/api/getToken");

	const res = await axiosWithAuth(res1.data).get("prestaciones/all");

	return res;
};

export const allByCodPrestaciones = async (cod) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		cod_usuario: cod,
	};
	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).post(
		"prestaciones/por_cod",
		cuerpo
	);
	return res;
};

export const rankingPrestaciones = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get(
		"prestaciones/top_prestaciones"
	);
	return res;
};

export const rankingPrestadores = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get("prestadores/top_prestadores");
	return res;
};

export const dashBoardFiltros = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get("dashboard/filtros");
	return res;
};

export const dashBoardOperaciones = async (filtro) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		mes: filtro,
	};
	const res = await axiosWithAuth(res1.data).post(
		"dashboard/operaciones",
		cuerpo
	);
	return res;
};

export const dashBoardVentas = async (filtro) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		mes: filtro,
	};
	const res = await axiosWithAuth(res1.data).post("dashboard/ventas", cuerpo);
	return res;
};

export const dashBoardPrestadores = async (filtro) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		mes: filtro,
	};
	const res = await axiosWithAuth(res1.data).post(
		"dashboard/prestadores",
		cuerpo
	);
	return res;
};

export const dashBoardClientes = async (filtro) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		mes: filtro,
	};
	const res = await axiosWithAuth(res1.data).post("dashboard/clientes", cuerpo);
	return res;
};

export const dashBoardVentasMensual = async (filtro) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		mes: filtro,
	};
	const res = await axiosWithAuth(res1.data).post(
		"dashboard/ventas_mensual",
		cuerpo
	);
	return res;
};

export const dashBoardVentasAnual = async (filtro) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		mes: filtro,
	};
	const res = await axiosWithAuth(res1.data).post(
		"dashboard/ventas_anual",
		cuerpo
	);
	return res;
};
export const devolucionesAll = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get("devoluciones/all");
	console.log("devolucionesAll", res);
	return res;
};

export const devolucionByCod = async (code) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		cod_documento: code,
	};
	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).post(
		"devoluciones/by_cod_doc",
		cuerpo
	);
	console.log("devolucionByCod", res);
	return res;
};

export const devolucionCancelar = async (code) => {
	const res1 = await axios.get("/api/getToken");
	const cuerpo = {
		cod_devolucion: code,
	};
	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).put(
		"devoluciones/cancelar",
		cuerpo
	);
	console.log(cuerpo);
	return res;
};

export const devolucionCrear = async (cuerpo) => {
	const res1 = await axios.get("/api/getToken");

	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).post("devoluciones/crear", cuerpo);
	console.log("res", res);
	return res;
};

export const liquidacionAll = async (pag) => {
	const res1 = await axios.get("/api/getToken");
	let cuerpo = {
		page: pag,
		page_size: 100,
	};
	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).post("liquidaciones/all", cuerpo);
	console.log("res", res);
	return res;
};

export const liquidacionCrear = async (cuerpo) => {
	const res1 = await axios.get("/api/getToken");

	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).post(
		"liquidaciones/crear",
		cuerpo
	);
	console.log("res", res);
	return res;
};

export const liquidacionUsuario = async () => {
	const res1 = await axios.get("/api/getToken");
	const res = await axiosWithAuth(res1.data).get(
		"liquidaciones/usuarios_a_liquidar"
	);

	return res;
};

export const liquidacionDocumentoByUser = async (cod) => {
	const res1 = await axios.get("/api/getToken");
	let cuerpo = {
		cod_usuario: cod,
	};
	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).post(
		"liquidaciones/documentos_pendientes_por_usuario",
		cuerpo
	);

	return res;
};
export const liquidacionHistoricaByCod = async (cod) => {
	const res1 = await axios.get("/api/getToken");
	let cuerpo = {
		cod_usuario: cod,
	};
	console.log("cuerpo", cuerpo);
	const res = await axiosWithAuth(res1.data).post(
		"liquidaciones/historico_por_prestador",
		cuerpo
	);

	return res;
};
