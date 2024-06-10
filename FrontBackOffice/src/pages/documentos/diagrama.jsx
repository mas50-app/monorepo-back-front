import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { getCambiosEstado } from "../../apis/calls.js";
import { BsArrowReturnRight } from "react-icons/bs";

const DocumentMap = ({ documentStates }) => {
	const location = useLocation();
	const queryParams = new URLSearchParams(location.search);
	const codDocumento = queryParams.get("codDocumento");

	const [cambiosEstado, setCambiosEstado] = useState([]);

	useEffect(() => {
		(async () => {
			await handleGetData();
		})();
	}, []);

	const handleGetData = async () => {
		const resp = await getCambiosEstado(codDocumento);
		if (resp) {
			console.log(resp);
			setCambiosEstado(resp);
		}
	};

	return (
		<div className="flex flex-col ">
			<p>codDocumento: {codDocumento}</p>
			<div className="flex flex-row justify-center space-x-1">
				{cambiosEstado.map((estado, index) => (
					<div
						key={index}
						className="flex flex-col bg-gray-100 border rounded-lg p-4"
					>
						<h3 className="text-lg font-bold mb-2">
							Cambió a {estado.desc_estado_documento}
						</h3>
						<p className="text-gray-600">{estado.fecha_cambio_estado}</p>
						{index !== 0 && <BsArrowReturnRight className="mt-2" />}
					</div>
				))}
			</div>{" "}
		</div>
	);
};

export default DocumentMap;
