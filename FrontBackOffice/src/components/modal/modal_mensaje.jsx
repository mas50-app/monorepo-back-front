import React, { useEffect, useRef } from "react";
import { BsPatchCheck } from "react-icons/bs";
import { MdClose } from "react-icons/md";
import { TbFaceIdError, TbAlertOctagon } from "react-icons/tb";

function Modal_mensaje({ estado, mensaje, tipo, setEstado }) {
	const alertFocus = useRef(null);
	useEffect(() => {
		// hacer que el foco vaya al alerta
		if (estado) {
			alertFocus.current.focus();
		}
	}, []);

	return (
		<div
			ref={alertFocus}
			className={`transition-opacity duration-300 ${
				estado ? "absolute bottom-1 right-2 opacity-100" : "opacity-0 hidden"
			}   animate-bounce rounded-md ${
				tipo == "Error"
					? "bg-red-500"
					: tipo == "Alerta"
					? "bg-yellow-300"
					: "bg-green-50"
			}  p-4 `}
		>
			<div className="flex">
				<div className="flex-shrink-0">
					{tipo == "Error" ? (
						<TbFaceIdError className="h-5 w-5 text-white " aria-hidden="true" />
					) : tipo == "Alerta" ? (
						<TbAlertOctagon className="h-5 w-5 text-white" aria-hidden="true" />
					) : (
						<BsPatchCheck className="h-5 w-5 text-white" aria-hidden="true" />
					)}
				</div>
				<div className="ml-3">
					<p className={`text-sm font-medium  text-white`}>{mensaje}</p>
				</div>
				<div className="ml-auto pl-3">
					<div className="-mx-1.5 -my-1.5">
						<button
							onClick={() => setEstado(false)}
							type="button"
							className={`inline-flex ${
								tipo == "Error"
									? "bg-red-500"
									: tipo == "Alerta"
									? "bg-yellow-300"
									: "bg-green-50"
							}  rounded-md p-1.5    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-green-50 focus:ring-blue-400`}
						>
							<span className="sr-only">Dismiss</span>
							<MdClose className="h-5 w-5" aria-hidden="true" />
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Modal_mensaje;
