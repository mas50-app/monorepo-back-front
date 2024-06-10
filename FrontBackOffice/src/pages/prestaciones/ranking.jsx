import React, { useEffect, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { ImListNumbered } from "react-icons/im";
import { dashBoardFiltros, rankingPrestaciones } from "../../apis/calls";
import Filters from "../../components/filters/RankingPrestacionesFilters";
import { AiFillFilter, AiOutlineFilter } from "react-icons/ai";

function RankingPrestaciones() {

	const [filters, setFilters] = useState({
		desde: "",
		hasta: "",
		cantidad: 10
	})

	const [filterOpen, setFilterOpen] = useState(false)

	const [data, setData] = useState([])

	const rankingPrest = useMutation({
		mutationFn: rankingPrestaciones,
		onSuccess: (result) => {
			setData(result)
		}
	})

	const { isLoading: filterIsLoading, data: filtersData, isError: filtersIsError, error: filtersError, refetch: filtersRefetch } = useQuery({
		queryKey: ["dashboardFilters"],
		queryFn: dashBoardFiltros,
	});

	useEffect(() => {
		if (filtersData){
			let parseFilter = {...filters}
				parseFilter.hasta = `${filtersData[0].mes}-31`
				setFilters(parseFilter)
		}
	}, [filtersData])

	useEffect(() => {
		if (filters.hasta != ""){
			rankingPrest.mutate(filters)
		}
	}, [filters])


	useEffect(() => {
	}, [data])
	
	

	if (filterIsLoading || rankingPrest.isLoading) {
		return <p>Loading...</p>;
	}
	if (rankingPrest.isError || filtersIsError) {
		return <p>Error: {filtersError || rankingPrest.error}</p>;
	}

	const handleClickFilter = () => {
		if (!filterOpen){
			setFilterOpen(!filterOpen)
		}else{
			setFiltrar(!filtrar)
		}
	}

	return (
		<div className="bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<header className="px-5 py-4">
				<div className="flex flex-row justify-between">
					<div className="flex flex-row items-center space-x-3">
						<ImListNumbered size={30} />{" "}
						<h1 className="font-semibold text-gray-800">
							Ranking de pretaciones
						</h1>
					</div>
					{filterOpen ?
						<Filters data={filtersData} filters={filters} setFilters={setFilters} setFilterOpen={setFilterOpen} />
						:
						<button
						className={`flex flex-row justify-center items-center gap-2`}
							onClick={() => setFilterOpen(true)}
						>
							Filtros
							<AiFillFilter/>
						</button>
					}		
				</div>
			</header>

			<div className="transition-opacity duration-300 ease-in-out opacity-100">
				<div className="overflow-x-auto">
					<section className="p-6 my-6  text-gray-800">
						<div className="container grid grid-cols-1 gap-6 mx-auto sm:grid-cols-2 xl:grid-cols-4">
							{Array.isArray(data) &&
								data.slice(0, 10).map((e, i) => (
									<a
										href={`/prestaciones/detalle/?codPrestacion=${e.cod_servicio}`}
										key={i}
										className="flex p-1 space-x-1 rounded-lg md:space-x-6 bg-rose-50 text-gray-800"
									>
										<div className="flex justify-center items-center  align-middle rounded-lg sm:p-4 bg-pink-600 text-white font-extrabold text-[20px] w-20 border-4 border-white ">
											{i + 1}
										</div>
										<div className="flex flex-col justify-center align-middle w-full">
											<p className="text-2xl  leading-none mt-2">
												{e.nom_servicio}
											</p>
											<div className="flex flex-col mt-2 items-end mr-1">
												<p className="capitalize text-slate-500">Prestador: </p>
												<p className="capitalize text-right font-extrabold text-sm">
													{e.nombre_usuario}
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

export default RankingPrestaciones;
