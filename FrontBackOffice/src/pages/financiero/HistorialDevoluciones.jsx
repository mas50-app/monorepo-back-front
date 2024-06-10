import { useQuery } from "@tanstack/react-query";
import { getDevoluciones } from "../../apis/calls";
import Modal_splash from "../../components/modal/modal_splash";
import { Table } from "../../components/Table";
import { useNavigate } from "react-router-dom";


const HistorialDevoluciones = () => {

    const navigate = useNavigate()

    const {data, isLoading, isError, error} = useQuery(["getDevoluciones"], { queryFn: getDevoluciones})
    const fields = [
        {
			accessor: "cod_devolucion",
			Header: "Cod Devol.",
		},
        {
			accessor: "cod_usuario",
			Header: "Cod Usuario",
		},
        {
			accessor: "desc_usuario",
			Header: "Prestador",
            Cell: ({row}) => (
                <button  onClick={() => navigate(`/prestadores/detalle/?codPrestador=${row.values.cod_usuario}`)}>
                    {row.values.desc_usuario}
                </button>
            )
		},
        {
			accessor: "personal",
			Header: "Emisor",
		},
        {
			accessor: "fecha_devolucion",
			Header: "Fecha",
		},
        {
			accessor: "monto_devolucion",
			Header: "Monto",
		},
        {
			accessor: "cod_es_manual",
			Header: "Medio",
            Cell: ({row}) => (
                <>{row.values.cod_es_manual == "S" ? "Manual": "Flow"}</>
            )
		},
        {
			accessor: "desc_devolucion",
			Header: "Descripción",
		},
    ];

    if (isLoading) {
		return <Modal_splash estado={true} />;
	}
	if (isError) {
		return <p>Error: {error.message}</p>;
	}

    return (
        <div className="bg-white shadow-lg rounded-sm border border-gray-200 m-2">
			<header className="px-5 py-4">
				<div className="flex flex-row justify-between">
					<h2 className="font-semibold text-gray-800">
						Devoluciones
						<span className="text-gray-400 font-medium ml-5">
							{data.length}
						</span>
					</h2>
				</div>
			</header>
			<div>
				<div className="overflow-x-auto">
					{data.length > 0 && (
						<Table
							data={data}
							COLUMNS={fields}
							hiddenColumns={[
								// "cod_documento"
								"cod_usuario",
							]}
							parentName="Devoluciones"
						/>
					)}
				</div>
			</div>
		</div>
    )
}

export default HistorialDevoluciones;