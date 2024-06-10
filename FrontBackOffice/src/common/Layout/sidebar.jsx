import React, { useState } from "react";
import { FaArrowDown } from "react-icons/fa";
import { Link } from "react-router-dom";

function Sidebar() {
	const [expandTitle, setexpandTitle] = useState([
		{
			titulo: "Prestadores",
			estado: false,
			subtitulo: [
				{ titulo: "Todos", ruta: "/prestadores" },
				{ titulo: "Pendientes", ruta: "/prestadores/pendientes" },
				{ titulo: "Ranking", ruta: "/prestadores/ranking" },
			],
		},
		{
			titulo: "Clientes",
			estado: false,
			subtitulo: [{ titulo: "Todos", ruta: "/clientes" }],
		},
		{
			titulo: "Prestaciones",
			estado: false,
			subtitulo: [
				{ titulo: "Todos", ruta: "/prestaciones" },
				{ titulo: "Ranking", ruta: "/prestaciones/ranking" },
			],
		},
		{
			titulo: "Financiero",
			estado: false,
			subtitulo: [
				{ titulo: "Por Liquidar", ruta: "/financiero/liquidaciones" },
				{ titulo: "Histórico pagos", ruta: "/financiero/pagadas" },
				{ titulo: "Devoluciones", ruta: "/financiero/historial-devoluciones" },
				{ titulo: "Devoluciones Pendientes", ruta: "/financiero/devoluciones" },
			],
		},
		{
			titulo: "Documentos",
			estado: false,
			subtitulo: [
				{ titulo: "Todos", ruta: "/documentos" },
				// { titulo: "Mapa de Estados", ruta: "/documentos/mapa" },
			],
		},
		{
			titulo: "Configuración",
			estado: false,
			subtitulo: [
				{ titulo: "App", ruta: "/configuracion/app" },
				{ titulo: "Personal", ruta: "/configuracion/personal" },
				{ titulo: "Bancos", ruta: "/configuracion/bancos" },
				{ titulo: "Couriers", ruta: "/configuracion/couriers" },
			],
		},
	]);

	const dropdownTitle = (id) => {
		const newExpandTitle = [...expandTitle];
		const elementIndex = newExpandTitle.findIndex((e) => e.titulo === id);
		newExpandTitle[elementIndex].estado = !newExpandTitle[elementIndex].estado;
		setexpandTitle(newExpandTitle);
	};

	return (
		<aside className="w-44 flex flex-col h-full" aria-label="Sidebar">
			<div className="overflow-y-auto py-4 px-1  rounded rounded-r-none rounded-t-none bg-rose-800 h-full ">
				<ul className=" mr-2 text-left text-sm space-y-1">
					{Array.isArray(expandTitle) &&
						expandTitle.map((element, i) => (
							<div key={i}>
								<li
									className="p-3 flex items-center justify-between rounded-md  duration-300 cursor-pointer hover:bg-rose-800 text-white"
									id={element.titulo}
									onClick={(e) => dropdownTitle(e.currentTarget.id)}
								>
									<span className="text-[15px]  text-gray-200 font-bold">
										{element.titulo}
									</span>
									<FaArrowDown
										className={`${
											expandTitle[
												expandTitle.findIndex((e) => e.titulo == element.titulo)
											].estado
												? "rotate-180"
												: "rotate-0"
										} `}
									/>
								</li>
								<div
									className={`${
										expandTitle[
											expandTitle.findIndex((e) => e.titulo == element.titulo)
										].estado
											? ""
											: "hidden"
									}  text-right text-sm my-2 text-black font-bold space-y-1  rounded-md bg-slate-100`}
								>
									{Array.isArray(element.subtitulo) &&
										element.subtitulo.map((element1, i1) => (
											<a href={element1.ruta} key={i1}>
												<h1 className="cursor-pointer p-3  hover:bg-rose-700 hover:text-white rounded-md pr-3">
													{element1.titulo}
												</h1>
											</a>
										))}
								</div>
							</div>
						))}
				</ul>
			</div>
		</aside>
	);
}

export default Sidebar;
