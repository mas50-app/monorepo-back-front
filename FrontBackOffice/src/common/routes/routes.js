import Home from "../../pages/home";
import Prestadores from "../../pages/prestadores/prestadores";
import { DetallePrestador } from "../../pages/prestadores/detalle.jsx";
import PrestadoresPendientes from "../../pages/prestadores/pendientes";
import RankingPrestadores from "../../pages/prestadores/ranking";
import Clientes from "../../pages/clientes/clientes";
import Prestaciones from "../../pages/prestaciones/prestaciones";
import RankingPrestaciones from "../../pages/prestaciones/ranking";
import LiquidacionesPagadas from "../../pages/financiero/liquidacionesPagadas";
import Devoluciones from "../../pages/financiero/devoluciones";
import { CrearDevolucion } from "../../pages/financiero/crearDevolucion";
import Liquidaciones from "../../pages/financiero/liquidaciones";
import DocumentMap from "../../pages/documentos/diagrama.jsx";
import Documentos from "../../pages/documentos/documentos.jsx";
import { DetalleDocumento } from "../../pages/documentos/detalleDocumento.jsx";
import { DetallePrestacion } from "../../pages/prestaciones/detallePrestacion.jsx";
import DetallesCliente from "../../pages/clientes/detalles_cliente";
import {MantenedorUsuarios} from "../../pages/configuracion/mantenedorUsuarios.jsx";
import {AppM} from "../../pages/configuracion/app.jsx";
import {MantenedorBancos} from "../../pages/configuracion/mantenedorBancos.jsx";
import {mantenedorCourier} from "../../pages/configuracion/mantenedorCouriers.jsx";
import HistorialDevoluciones from "../../pages/financiero/HistorialDevoluciones";
export const routes = [
	{
		path: "/home",
		href: "/home",
		name: "Home",
		component: Home,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/prestadores",
		href: "/prestadores",
		name: "Prestadores",
		component: Prestadores,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/prestadores/detalle",
		href: "/prestadores/detalle",
		// name: "Prestadores",
		component: DetallePrestador,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/prestadores/pendientes",
		href: "/prestadores/pendientes",
		// name: "Prestadores",
		component: PrestadoresPendientes,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/prestadores/ranking",
		href: "/prestadores/ranking",
		// name: "Prestadores",
		component: RankingPrestadores,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/clientes",
		href: "/clientes",
		// name: "Prestadores",
		component: Clientes,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/clientes/detalle",
		href: "/clientes/detalle",
		// name: "Prestadores",
		component: DetallesCliente,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/prestaciones",
		href: "/prestaciones",
		// name: "Prestadores",
		component: Prestaciones,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/prestaciones/ranking",
		href: "/prestaciones/ranking",
		// name: "Prestadores",
		component: RankingPrestaciones,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/prestaciones/detalle",
		href: "/prestaciones/detalle",
		// name: "Prestadores",
		component: DetallePrestacion,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/documentos/mapa",
		href: "/documentos/mapa",
		// name: "Prestadores",
		component: DocumentMap,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/documentos",
		href: "/documentos",
		// name: "Prestadores",
		component: Documentos,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/documentos/detalle",
		href: "/documentos/detalle",
		// name: "Prestadores",
		component: DetalleDocumento,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/financiero/pagadas",
		href: "/financiero/pagadas",
		// name: "Prestadores",
		component: LiquidacionesPagadas,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/financiero/historial-devoluciones",
		href: "/financiero/historial-devoluciones",
		component: HistorialDevoluciones,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/financiero/devoluciones",
		href: "/financiero/devoluciones",
		// name: "Prestadores",
		component: Devoluciones,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/financiero/devoluciones/crear",
		href: "/financiero/devoluciones/crear",
		// name: "Prestadores",
		component: CrearDevolucion,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/financiero/liquidaciones",
		href: "/financiero/liquidaciones",
		// name: "Prestadores",
		component: Liquidaciones,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/configuracion/personal",
		href: "/configuracion/personal",
		// name: "Prestadores",
		component: MantenedorUsuarios,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/configuracion/app",
		href: "/configuracion/app",
		// name: "Prestadores",
		component: AppM,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/configuracion/bancos",
		href: "/configuracion/bancos",
		// name: "Prestadores",
		component: MantenedorBancos,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
	{
		path: "/configuracion/couriers",
		href: "/configuracion/couriers",
		// name: "Prestadores",
		component: mantenedorCourier,
		icon: "",
		inSidebar: true,
		permisos: [1, 2, 3],
	},
];
