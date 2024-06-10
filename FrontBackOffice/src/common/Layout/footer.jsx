import React from "react";

function Footer() {
	return (
		<footer className=" bg-white rounded-lg shadow w-full flex flex-row">
			<span className="block text-sm text-gray-500 text-end  dark:text-gray-400">
				© 2023{" "}
				<a href="#" className="hover:underline">
					Mas Cincuenta™
				</a>
				. Todos los derechos reservados.
			</span>
		</footer>
	);
}

export default Footer;
