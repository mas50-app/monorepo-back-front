import React, { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ImListNumbered } from "react-icons/im";
import { rankingPrestadores } from "../../apis/calls";

function RankingPrestadores() {
	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["rankingPrestadores"],
		queryFn: rankingPrestadores,
		// refetchOnWindowFocus: false,
		onSuccess: (data) => {
			console.log("rankingPrestadores", data);
		},
	});

	if (isLoading) {
		return <p>Loading...</p>;
	}
	if (isError) {
		return <p>Error: {error.message}</p>;
	}

	return (
		<div className="bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<header className="px-5 py-4">
				<div className="flex flex-row justify-between">
					<div className="flex flex-row items-center space-x-3">
						<ImListNumbered size={30} />{" "}
						<h1 className="font-semibold text-gray-800">
							Ranking de prestadores
						</h1>
					</div>
				</div>
			</header>

			<div x-data="handleSelect">
				<div className="overflow-x-auto">
					<section className="p-6 my-6  text-gray-800">
						<div className="container grid grid-cols-1 gap-6 mx-auto sm:grid-cols-2 xl:grid-cols-4">
							{Array.isArray(data) &&
								data.slice(0, 10).map((e, i) => (
									<a
										href={`/prestadores/detalle/?codPrestador=${e.cod_usuario}`}
										key={i}
										className="flex p-1 space-x-1 rounded-lg md:space-x-6 bg-rose-50 text-gray-800"
									>
										<div className="flex justify-center items-center  align-middle rounded-lg sm:p-4 bg-pink-600 text-white font-extrabold text-[20px] w-20 border-4 border-white ">
											{i + 1}
										</div>
										<div className="flex flex-col justify-center align-middle w-full">
											<p className="text-2xl  leading-none mt-2">
												{e.nombre_usuario}
											</p>
											<div className="flex flex-col mt-2 items-end mr-1">
												<p className="capitalize text-slate-500">Talento: </p>
												<p className="capitalize text-right font-extrabold text-sm">
													{e.desc_talento_usuario}
												</p>
												<p className="capitalize ">Ventas: {e.ventas}</p>
											</div>
										</div>
									</a>
								))}
						</div>
					</section>
				</div>
			</div>
		</div>
	);
}

export default RankingPrestadores;
