import { Line, Pie } from "react-chartjs-2";
import 'chartjs-adapter-moment';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {
	Chart as ChartJS,
	ArcElement,
	Tooltip,
	Legend,
	CategoryScale,
	registerables,
} from "chart.js";
import {
	dashBoardClientes,
	dashBoardFiltros,
	dashBoardOperaciones,
	dashBoardPrestadores,
	dashBoardVentas,
	dashBoardVentasAnual,
	dashBoardVentasMensual, dashResumenMontos, getCategoriasAll, getRegionesAll,
} from "../apis/calls";
import randomColor from "randomcolor";
import { useMutation, useQuery } from "@tanstack/react-query";

import {useEffect, useState} from "react";
import Modal_splash from "../components/modal/modal_splash";
import {ChartCard, DataBlueCard, DataGreenCard, DataRedCard, DataYellowCard} from "../components/Cards.jsx";
import {AiFillFilter, AiOutlineFilter, BsFiletypePdf, FaCashRegister, FaMoneyBillWave, FaPeopleCarry, TbUsers} from "react-icons/all.js";
import {formatFloat} from "../utils/formatMoney.js";
import Filters from "../components/filters/dashboardFilters";
import { useRef } from "react";
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';


ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, ...registerables);

export default function Home() {
	const [dataChar1, setDataChar1] = useState(null);
	const [dataChar2, setDataChar2] = useState(null);
	const [dataChar3, setDataChar3] = useState(null);
	const [dataChar4, setDataChar4] = useState(null);
	const [dataChar5, setDataChar5] = useState(null);
	const [dataChar6, setDataChar6] = useState(null);
	const [dataMontosResumen, setdataMontosResumen] = useState(null);

	const componentRef = useRef();

	const [filtrar, setFiltrar] = useState(false)

	const { isLoading, data, isError, error, refetch } = useQuery({
		queryKey: ["dashboardFilters"],
		queryFn: dashBoardFiltros,
	});

	useEffect(() => {
		if (data){
			let parseFilter = [...filters]
				parseFilter[3].selected = `${data[0].mes}-31`
				setFilters(parseFilter)
		}
	}, [data])
	
	
	const [filters, setFilters] = useState([
		{ 
			id: 'cod_categoria',
			name: 'Categorías',
			options: [],
			selected: []
		},
		{ 
			id: 'cod_region',
			name: 'Regiones',
			options: [],
			selected: []
		},
		{ 
			id: 'desde',
			name: 'Desde',
			selected: ""
		},
		{ 
			id: 'hasta',
			name: 'Hasta',
			selected: ""
		},
	])

	const [filterOpen, setFilterOpen] = useState(false)

	const getCategorias = useQuery({
		queryKey: ["categorias"],
		queryFn: async () => {
			const cats = await getCategoriasAll()
			let cOps = []
			cats.map(cat => {
				cOps.push({
					value: cat.cod_categoria,
					label: cat.desc_categoria
				})
			})
			return cOps
		}
	})

	const getRegiones = useQuery({
		queryKey: ["regiones"],
		queryFn: async () => {
			const regs = await getRegionesAll()
			let rOps = []
			regs.map(cat => {
				rOps.push({
					value: cat.cod_region,
					label: cat.desc_region
				})
			})
			return rOps
		}
	})

	useEffect(() => {
		let parseFilters = [...filters]
		parseFilters[0].options = getCategorias.data
		setFilters(parseFilters)
		const isFiltered = filters.filter((fil) => fil.selected.length > 0).length > 0
		if (isFiltered) {
			handleMutate()
		}
	}, [getCategorias.isLoading, getCategorias.data, filtrar])


	useEffect(() => {
		let parseFilters = [...filters]
		parseFilters[1].options = getRegiones.data
	  		setFilters(parseFilters)
	}, [getRegiones.data, getRegiones.isLoading])

	const handleMutate = () => {
		let cuerpo = {}
			filters.map(fil => {
				if (fil.selected.length > 0 || fil.selected != ""){
					cuerpo[fil.id] = fil.selected
				}
			})
			mutationChart1.mutate(cuerpo)
			mutationChart2.mutate(cuerpo)
			mutationChart3.mutate(cuerpo)
			mutationChart4.mutate(cuerpo)
			mutationChart5.mutate(cuerpo)
			mutationChart6.mutate(cuerpo)
			getMontosResumen.mutate(cuerpo)
			setFilterOpen(false)
	}

	const generateColors = (value) => {
		const colors = [];
		for (let i = 0; i < value.length; i++) {
			const color = randomColor();
			colors.push(color);
		}
		return colors;
	};

	const getMontosResumen = useMutation({
		mutationFn: dashResumenMontos,
		onSuccess: (result) => {
			setdataMontosResumen(result);
		},
		onError: (response) => {
			console.log(response.response.data);
		},
	});

	const mutationChart1 = useMutation({
		mutationFn: dashBoardOperaciones,
		onSuccess: (value) => {
			const labels = value.map((item) => item.name);
			const dataP = value.map((item) => item.value);
			const backColors = generateColors(value);
			const hoverColors = generateColors(value);
			const parsedData = {
				labels: labels,
				datasets: [
					{
						data: dataP,
						backgroundColor: backColors,
						hoverBackgroundColor: hoverColors,
					},
				],
			};
			setDataChar1(parsedData);
		},
		onError: (response) => {
			console.log(response.response.data);
		},
	});

	const mutationChart2 = useMutation({
		mutationFn: dashBoardVentas,
		onSuccess: (value) => {
			const labels = value.map((item) => item.name);
			const dataP = value.map((item) => item.value);
			const backColors = generateColors(value);
			const hoverColors = generateColors(value);
			const parsedData = {
				labels: labels,
				datasets: [
					{
						data: dataP,
						backgroundColor: backColors,
						hoverBackgroundColor: hoverColors,
					},
				],
			};
			setDataChar2(parsedData);
		},
		onError: (response) => {
			console.log(response.response.data);
		},
	});

	const mutationChart3 = useMutation({
		mutationFn: dashBoardPrestadores,
		onSuccess: (value) => {
			const labels = value.map((item) => item.name);
			const dataP = value.map((item) => item.value);
			const backColors = generateColors(value);
			const hoverColors = generateColors(value);
			const parsedData = {
				labels: labels,
				datasets: [
					{
						data: dataP,
						backgroundColor: backColors,
						hoverBackgroundColor: hoverColors,
					},
				],
			};
			setDataChar3(parsedData);
		},
		onError: (response) => {
			console.log(response.response.data);
		},
	});

	const mutationChart4 = useMutation({
		mutationFn: dashBoardClientes,
		onSuccess: (value) => {
			const labels = value.map((item) => item.name);
			const dataP = value.map((item) => item.value);
			const backColors = generateColors(value);
			const hoverColors = generateColors(value);
			const parsedData = {
				labels: labels,
				datasets: [
					{
						data: dataP,
						backgroundColor: backColors,
						hoverBackgroundColor: hoverColors,
					},
				],
			};
			setDataChar4(parsedData);
		},
		onError: (response) => {
			console.log(response.response.data);
		},
	});

	const mutationChart5 = useMutation({
		mutationFn: dashBoardVentasMensual,
		onSuccess: (value) => {
			const labels = value.map((item) => item.name);
			const dataP = value.map((item) => item.value);
			const parsedData = {
				labels,
				datasets: [
					{
						data: dataP,
						borderColor: "rgb(255, 99, 132)",
						backgroundColor: "rgba(255, 99, 132, 0.5)",
					},
				],
			};
			setDataChar5(parsedData);
		},
		onError: (response) => {
			console.log(response.response.data);
		},
	});

	const mutationChart6 = useMutation({
		mutationFn: dashBoardVentasAnual,
		onSuccess: (value) => {
			const labels = value.map((item) => item.name);
			const dataP = value.map((item) => item.value);
			const parsedData = {
				labels,
				datasets: [
					{
						data: dataP,
						borderColor: "rgb(255, 99, 132)",
						backgroundColor: "rgba(255, 99, 132, 0.5)",
					},
				],
			};
			setDataChar6(parsedData);
		},
		onError: (response) => {
			console.log(response.response.data);
		},
	});

	if (mutationChart1.isLoading || mutationChart2.isLoading || mutationChart3.isLoading || mutationChart4.isLoading || mutationChart5.isLoading || mutationChart6.isLoading) {
		return <Modal_splash estado={true} />;
	}
	if (isError) {
		return <p>Error: {error}</p>;
	}

	if (!dataMontosResumen && getMontosResumen.isSuccess){
		toast.dismiss();
		toast.error("Solo gráfico de ventas");
	}

	const options = {
		responsive: true,
		plugins: {
			legend: {
				display: false,
			},
			title: {
				display: false,
				text: "Ventas en el Mes",
			},
		},
		scales: {
            x: {
                type: 'time',
                time: {
                    unit: "day"
                },
				ticks: {
					callback: (value) => {
						const date = new Date(value);
						return Intl.DateTimeFormat('es-ES', {
							year: 'numeric',
							month: '2-digit',
							day: '2-digit'
						}).format(date)
					}
				}
            },
			y: {
				beginAtZero: true
			}
        }
	};

	const options1 = {
		responsive: true,
		plugins: {
			legend: {
				display: false,
			},
			title: {
				display: false,
				text: "Ventas en el Año",
			},
		},
		scales: {
            x: {
                type: 'timeseries',
                time: {
                    unit: "month"
                },
				ticks: {
					callback: (value) => {
						const date = new Date(value);
						return Intl.DateTimeFormat('es-ES', {
							year: 'numeric',
							month: '2-digit',
						}).format(date)
					}
				}
            },
			y: {
				beginAtZero: true
			}
        }
	};

	const options2 = {
		responsive: true,
		plugins: {
			legend: {
				display: true,
				position: 'bottom'
			},
		},
	};	

	const handleClickFilter = () => {
		if (!filterOpen){
			setFilterOpen(!filterOpen)
		}else{
			setFiltrar(!filtrar)
		}
	}

	const exportToPDF = () => {
		const input = componentRef.current;
		if (!input) return;
	
		// Capturar el dashboard como una imagen
		html2canvas(input).then((canvas) => {
			const imgData = canvas.toDataURL('image/png');
	  
			// Crear el documento PDF
			const pdf = new jsPDF('p', 'mm', 'a4');
			const pdfWidth = pdf.internal.pageSize.getWidth();
			const pdfHeight = pdf.internal.pageSize.getHeight();
	  
			// Calcular la relación de aspecto de la imagen
			const imgProps = pdf.getImageProperties(imgData);
			const aspectRatio = imgProps.width / imgProps.height;
	  
			// Ajustar el tamaño de la imagen para que quepa en una página del PDF
			let imgWidth = pdfWidth;
			let imgHeight = pdfWidth / aspectRatio;
	  
			if (imgHeight > pdfHeight) {
			  imgHeight = pdfHeight;
			  imgWidth = pdfHeight * aspectRatio;
			}
	  
			// Agregar la imagen al PDF
			pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
			pdf.save(`dashboard_${filters[2].selected && filters[2].selected + "_"}${filters[3].selected && filters[3].selected}.pdf`);
		  });
	  };


	return (
		<div className="overflow-y-auto h-full w-full flex flex-col flex-1 bg-gray-100 mt-12 md:mt-2 pb-24 md:pb-5">
			<div className="flex flex-row justify-between rounded-lg bg-red-500 p-4 shadow text-2xl text-white">
				<h3 className="font-bold uppercase pl-2">
					DASHBOARD
				</h3>
				<div className="flex flex-row justify-between items-center gap-6">
					<button
					className="flex flex-row justify-center items-center gap-2 hover:text-red-400"
						onClick={() => handleClickFilter()}
					>
						{!filterOpen ? "Filtros" : "Filtrar"}
						{filterOpen ? <AiFillFilter/>: <AiOutlineFilter/>}
					</button>
					<button 
						className="flex flex-row  hover:text-red-400"
						onClick={() => exportToPDF()}
					>
						<BsFiletypePdf/>
					</button>
				</div>
				
			</div>
			{filterOpen && 
				<Filters filters={filters} setFilters={setFilters} data={data} setFilterOpen={setFilterOpen} filtrar={filtrar} setFiltrar={setFiltrar}/>
			}
			<div ref={componentRef}>
				{dataMontosResumen != null && (
						<div className="flex flex-wrap">
							<DataYellowCard title="Total Recaudado" icon={<FaMoneyBillWave size="3em"/>} value={formatFloat(dataMontosResumen?.total_recaudado)}/>
							<DataGreenCard title="Comisión +50" icon={<FaMoneyBillWave size="3em"/>} value={formatFloat(dataMontosResumen?.utilidad_bruta)}/>
							<DataBlueCard title="Comisión Flow" icon={<FaCashRegister size="3em"/>} value={formatFloat(dataMontosResumen?.flow_bruto)}/>
							<DataRedCard title="Pagado a Prestadores" icon={<FaPeopleCarry size="3em"/>} value={formatFloat(dataMontosResumen?.pagos_prestadores)}/>
						</div>
					)}
				<div className="flex flex-row flex-wrap flex-grow mt-2">
					{dataChar6 != null && dataChar6.labels.length > 0 && (
						<ChartCard title="Ventas en el Año" chart={<Line options={options1} data={dataChar6} />}/>
					)}
					{dataChar5 != null && dataChar5.labels.length > 0 && (
						<ChartCard title="Ventas en el Mes" chart={<Line options={options} data={dataChar5} />}/>
					)}
				</div>
				<div className="flex flex-row flex-wrap flex-grow mt-2">
					{dataChar1 != null && dataChar1.labels.length > 0 && (
						<ChartCard title="Operaciones" chart={<Pie data={dataChar1} options={options2} />}/>
					)}
					{dataChar2 != null && dataChar2.labels.length > 0 && (
						<ChartCard title="Ventas" chart={<Pie data={dataChar2} options={options2} />}/>
					)}
				</div>
				<div className="flex flex-row flex-wrap flex-grow mt-2">
					{dataChar3 != null && dataChar3.labels.length > 0 ? (
						<ChartCard title="Top Prestadores" chart={<Pie data={dataChar3} options={options2}/>}/>
					) : (
						""
					)}
					{dataChar4 != null && dataChar4.labels.length > 0 && (
						<ChartCard title="Top Clientes" chart={<Pie data={dataChar4} options={options2}/>}/>
					)}
				</div>
			</div>
			
		</div>
	);
}
