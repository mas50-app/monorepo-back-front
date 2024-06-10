import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getTokenData } from "../utils/tokenData.js";
import Cookies from "js-cookie";

export const ProtectedRoute = (props) => {
	const navigate = useNavigate();
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const [autorizado, setAutorizado] = useState(false);

	const checkUserToken = async () => {
		const token = await getTokenData();
		if (token === null) {
			setIsLoggedIn(false);
			Cookies.remove("token");
			return navigate("/");
		}
		/* token.mantenedorUsuarios.jsx.forEach((perm) => {
			if (props.codsPermisos.includes(perm.cod_permiso)) {
				setAutorizado(true);
			}
		}); */
		setIsLoggedIn(true);
	};

	useEffect(() => {
		(async () => {
			await checkUserToken();
		})();
	}, [isLoggedIn]);
	return (
		<React.Fragment>
			{/* {isLoggedIn && autorizado ? props.children : null} */}
			{isLoggedIn ? props.children : null}
		</React.Fragment>
	);
};
